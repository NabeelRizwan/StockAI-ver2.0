import asyncio
import logging
import random
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set

from backend.app.agents.behavioral_agent import BaseAgent
from backend.app.core.analytics import (
    compute_index_level,
    compute_market_analytics,
    compute_sector_indices,
)
from backend.app.models.types import (
    DaySnapshot,
    FinancialReport,
    ForumMessage,
    LOAN_TERMS,
    MarketEvent,
    Order,
    REPORT_DAYS,
    Loan,
)

logger = logging.getLogger("simulation.loop")

EVENT_TEMPLATES = [
    {"title": "Interest Rate Decision", "type": "monetary_policy", "severity": "HIGH", "impact_range": (-0.03, 0.03)},
    {"title": "Quarterly Earnings Report", "type": "earnings", "severity": "MEDIUM", "impact_range": (-0.02, 0.02)},
    {"title": "Trade Policy Announcement", "type": "policy", "severity": "HIGH", "impact_range": (-0.025, 0.025)},
    {"title": "Market Sentiment Shift", "type": "sentiment", "severity": "MEDIUM", "impact_range": (-0.015, 0.015)},
    {"title": "Product Launch News", "type": "corporate", "severity": "LOW", "impact_range": (-0.005, 0.01)},
    {"title": "Analyst Downgrade", "type": "analyst", "severity": "MEDIUM", "impact_range": (-0.02, 0.005)},
    {"title": "Social Media Buzz", "type": "social", "severity": "LOW", "impact_range": (-0.01, 0.015)},
    {"title": "Economic Data Release", "type": "macro", "severity": "MEDIUM", "impact_range": (-0.015, 0.015)},
    {"title": "M&A Announcement", "type": "corporate", "severity": "HIGH", "impact_range": (-0.01, 0.04)},
    {"title": "Regulatory Change", "type": "regulation", "severity": "HIGH", "impact_range": (-0.03, 0.01)},
]

VOLATILITY_MAP = {"Low": 0.005, "Medium": 0.015, "High": 0.03, "Extreme": 0.05}

SECTOR_NAMES = ["Tech", "Energy", "Finance", "Auto", "Retail", "Entertainment"]

SECTOR_CORR = {
    ("Tech", "Tech"): 1.0,
    ("Tech", "Energy"): 0.15,
    ("Tech", "Finance"): 0.30,
    ("Tech", "Auto"): 0.35,
    ("Tech", "Retail"): 0.25,
    ("Tech", "Entertainment"): 0.40,
    ("Energy", "Energy"): 1.0,
    ("Energy", "Finance"): 0.25,
    ("Energy", "Auto"): 0.30,
    ("Energy", "Retail"): 0.15,
    ("Energy", "Entertainment"): 0.10,
    ("Finance", "Finance"): 1.0,
    ("Finance", "Auto"): 0.20,
    ("Finance", "Retail"): 0.35,
    ("Finance", "Entertainment"): 0.20,
    ("Auto", "Auto"): 1.0,
    ("Auto", "Retail"): 0.20,
    ("Auto", "Entertainment"): 0.15,
    ("Retail", "Retail"): 1.0,
    ("Retail", "Entertainment"): 0.30,
    ("Entertainment", "Entertainment"): 1.0,
}

REGIME_LIBRARY = {
    "risk_on": {
        "headline": "Risk-on expansion",
        "sector_bias": {"Tech": 0.8, "Entertainment": 0.4, "Finance": 0.2},
        "event_bias": {"sentiment", "corporate", "social"},
        "vol_multiplier": 1.0,
    },
    "risk_off": {
        "headline": "Risk-off defensive rotation",
        "sector_bias": {"Tech": -0.5, "Energy": 0.1, "Retail": -0.3, "Finance": -0.2},
        "event_bias": {"macro", "policy", "regulation"},
        "vol_multiplier": 1.2,
    },
    "inflation_shock": {
        "headline": "Inflation shock repricing",
        "sector_bias": {"Energy": 0.7, "Retail": -0.5, "Tech": -0.2, "Auto": -0.4},
        "event_bias": {"macro", "monetary_policy"},
        "vol_multiplier": 1.35,
    },
    "policy_tightening": {
        "headline": "Policy tightening",
        "sector_bias": {"Finance": 0.4, "Tech": -0.4, "Auto": -0.25},
        "event_bias": {"monetary_policy", "policy", "regulation"},
        "vol_multiplier": 1.15,
    },
    "earnings_repricing": {
        "headline": "Earnings repricing",
        "sector_bias": {"Tech": 0.5, "Entertainment": 0.2, "Retail": -0.1},
        "event_bias": {"earnings", "analyst", "corporate"},
        "vol_multiplier": 1.1,
    },
    "sector_rotation": {
        "headline": "Cross-sector rotation",
        "sector_bias": {"Finance": 0.3, "Energy": 0.3, "Tech": -0.2, "Entertainment": -0.2},
        "event_bias": {"sentiment", "macro", "analyst"},
        "vol_multiplier": 1.05,
    },
}

CIRCUIT_BREAKER_PCT = 0.10
LLM_BATCH_SIZE = 5
LLM_BATCH_DELAY = 2.0


def _corr(s1: str, s2: str) -> float:
    return SECTOR_CORR.get((s1, s2), SECTOR_CORR.get((s2, s1), 0.0))


class SimulationLoop:
    def __init__(self, agents: List[BaseAgent], order_books: Dict, stock_meta: Dict):
        self.agents = agents
        self.order_books = order_books
        self.stock_meta = stock_meta

        self.is_running = False
        self.is_paused = False
        self.day = 0
        self.session = 0
        self.total_days = 30
        self.sessions_per_day = 3
        self._run_id = 0

        self.speed = 2.0
        self.volatility = "Medium"
        self.event_intensity = 5
        self.use_llm = True
        self.enable_loans = True
        self.regime_sensitivity = 1.0
        self.benchmark_mode = "equal_weight"
        self.analytics_detail = "professional"

        self.all_trades = []
        self.events: List[MarketEvent] = []
        self.forum_messages: List[ForumMessage] = []
        self.financial_reports: List[FinancialReport] = []
        self.price_history: Dict[str, list] = {s: [] for s in order_books}
        self.total_trade_count = 0
        self.halted_stocks: Set[str] = set()
        self.snapshots: List[DaySnapshot] = []

        self.ws_broadcast = None
        self._session_open: Dict[str, float] = {}
        self.base_prices = {s: getattr(m, "initial_price", 100.0) for s, m in stock_meta.items()}
        self.current_regime = "risk_on"
        self.current_regime_profile = REGIME_LIBRARY[self.current_regime]
        self.regime_history: List[Dict] = [{"day": 0, "regime": self.current_regime, "headline": self.current_regime_profile["headline"]}]
        self.benchmark_history: List[Dict] = [{"day": 0, "session": 0, "value": 100.0}]
        self.sector_index_history: List[Dict] = []
        self.market_metrics_history: List[Dict] = []
        self.turnover = 0.0
        self.market_sentiment = "neutral"
        self.session_risk = "Normal"
        self._session_trade_notional = 0.0

    def configure(self, cfg: dict):
        self.total_days = cfg.get("num_days", self.total_days)
        self.volatility = str(cfg.get("volatility", self.volatility)).title()
        self.event_intensity = cfg.get("event_intensity", self.event_intensity)
        self.use_llm = cfg.get("use_llm", self.use_llm)
        self.speed = cfg.get("speed", self.speed)
        self.enable_loans = cfg.get("enable_loans", self.enable_loans)
        self.regime_sensitivity = cfg.get("regime_sensitivity", self.regime_sensitivity)
        self.benchmark_mode = cfg.get("benchmark_mode", self.benchmark_mode)
        self.analytics_detail = cfg.get("analytics_detail", self.analytics_detail)

    def _roll_regime(self, day: int):
        if day == 1 or (day - 1) % 6 == 0:
            self.current_regime = random.choice(list(REGIME_LIBRARY.keys()))
            self.current_regime_profile = REGIME_LIBRARY[self.current_regime]
            self.regime_history.append({
                "day": day,
                "regime": self.current_regime,
                "headline": self.current_regime_profile["headline"],
            })

    def _sector_of(self, symbol: str) -> str:
        meta = self.stock_meta.get(symbol)
        return meta.sector if meta else "Tech"

    def _generate_sector_drifts(self, event_impact_by_sector: Dict[str, float]) -> Dict[str, float]:
        raw = {}
        for sector in SECTOR_NAMES:
            regime_bias = self.current_regime_profile.get("sector_bias", {}).get(sector, 0.0) * self.regime_sensitivity
            raw[sector] = random.gauss(0, 1) + event_impact_by_sector.get(sector, 0.0) * 20 + regime_bias

        blended = {}
        for sector in SECTOR_NAMES:
            val = raw[sector]
            for other in SECTOR_NAMES:
                if other != sector:
                    val += raw[other] * _corr(sector, other) * 0.3
            blended[sector] = val
        return blended

    def _calculate_trend(self, symbol: str, window: int = 6) -> str:
        history = self.price_history.get(symbol, [])
        if len(history) < 2:
            return "Neutral"
        recent = history[-window:]
        change = (recent[-1]["price"] - recent[0]["price"]) / recent[0]["price"]
        if change > 0.01:
            return "Bullish"
        if change < -0.01:
            return "Bearish"
        return "Neutral"

    def _apply_correlated_walk(self, sector_drifts: Dict[str, float]):
        vol = VOLATILITY_MAP.get(self.volatility, 0.015) * self.current_regime_profile.get("vol_multiplier", 1.0)
        for symbol, book in self.order_books.items():
            if symbol in self.halted_stocks:
                continue
            meta = self.stock_meta.get(symbol)
            vm = meta.volatility_multiplier if meta else 1.0
            sector = self._sector_of(symbol)
            current = book.last_price or (meta.initial_price if meta else 100.0)
            drift = sector_drifts.get(sector, 0.0) * vol * 0.5
            noise = random.gauss(0, vol * vm)
            new_price = round(max(1.0, current * (1 + drift + noise)), 2)
            book.update_price(new_price, self.day, self.session)
            self.price_history.setdefault(symbol, []).append({
                "time": datetime.now().isoformat(),
                "price": new_price,
                "day": self.day,
                "session": self.session,
            })

    def _check_circuit_breakers(self) -> List[MarketEvent]:
        events = []
        for symbol, book in self.order_books.items():
            if symbol in self.halted_stocks:
                continue
            open_price = self._session_open.get(symbol)
            if not open_price:
                continue
            current = book.last_price or open_price
            move = abs(current - open_price) / open_price
            if move >= CIRCUIT_BREAKER_PCT:
                self.halted_stocks.add(symbol)
                direction = "up" if current > open_price else "down"
                events.append(MarketEvent(
                    id=str(uuid.uuid4()),
                    day=self.day,
                    session=self.session,
                    title=f"Circuit Breaker: {symbol}",
                    description=f"{symbol} halted after {move:.1%} move {direction} in session {self.session}.",
                    severity="HIGH",
                    event_type="circuit_breaker",
                    impact_pct=0.0,
                    affected_stocks=[symbol],
                ))
        return events

    def _generate_events(self, day: int) -> List[MarketEvent]:
        events = []
        if day == max(1, int(self.total_days * 0.25)):
            events.append(MarketEvent(
                id=str(uuid.uuid4()),
                day=day,
                title="Interest Rate Decision",
                description="Central bank announces rate decision - markets brace for impact.",
                severity="HIGH",
                event_type="monetary_policy",
                impact_pct=random.uniform(-0.03, 0.03),
            ))
        if day == max(1, int(self.total_days * 0.5)):
            events.append(MarketEvent(
                id=str(uuid.uuid4()),
                day=day,
                title="Earnings Season Begins",
                description="Major companies report quarterly earnings.",
                severity="HIGH",
                event_type="earnings",
                impact_pct=random.uniform(-0.02, 0.02),
            ))
        if random.random() < (self.event_intensity / 15.0):
            preferred = self.current_regime_profile.get("event_bias", set())
            preferred_events = [tmpl for tmpl in EVENT_TEMPLATES if tmpl["type"] in preferred]
            tmpl = random.choice(preferred_events or EVENT_TEMPLATES)
            sector = random.choice(SECTOR_NAMES)
            affected = [s for s, m in self.stock_meta.items() if m.sector == sector]
            events.append(MarketEvent(
                id=str(uuid.uuid4()),
                day=day,
                title=tmpl["title"],
                description=f"Day {day}: {tmpl['title']} - {sector} sector impacted within {self.current_regime_profile['headline'].lower()}.",
                severity=tmpl["severity"],
                event_type=tmpl["type"],
                impact_pct=random.uniform(*tmpl["impact_range"]),
                affected_stocks=affected,
            ))
        return events

    def _event_impact_by_sector(self, events: List[MarketEvent]) -> Dict[str, float]:
        impacts: Dict[str, float] = {}
        for event in events:
            if event.affected_stocks:
                for sym in event.affected_stocks:
                    sector = self._sector_of(sym)
                    impacts[sector] = impacts.get(sector, 0.0) + event.impact_pct
            else:
                for sector in SECTOR_NAMES:
                    impacts[sector] = impacts.get(sector, 0.0) + event.impact_pct
        return impacts

    def _generate_financial_reports(self, day: int) -> Optional[Dict[str, Dict]]:
        if day not in REPORT_DAYS:
            return None
        quarter = REPORT_DAYS.index(day) + 1
        report_data: Dict[str, Dict] = {}
        for symbol in self.stock_meta:
            rev_growth = random.uniform(-0.10, 0.25)
            margin = random.uniform(0.05, 0.40)
            profit = random.uniform(-50, 200)
            cash_flow = random.uniform(-30, 150)
            sentiment = max(-1.0, min(1.0, (0.5 if rev_growth > 0 else -0.5) + (0.5 if profit > 0 else -0.5) + random.uniform(-0.2, 0.2)))
            report = FinancialReport(
                stock_symbol=symbol,
                day=day,
                quarter=quarter,
                revenue_growth=round(rev_growth, 3),
                gross_margin=round(margin, 3),
                net_profit_millions=round(profit, 1),
                cash_flow_millions=round(cash_flow, 1),
                sentiment_score=round(sentiment, 2),
            )
            self.financial_reports.append(report)
            report_data[symbol] = {
                "revenue": profit * 1_000_000 / max(0.01, margin),
                "profit": profit * 1_000_000,
                "margin": margin,
            }
        return report_data

    def _process_loans(self, day: int):
        if not self.enable_loans:
            return
        prices = {s: (b.last_price or 100.0) for s, b in self.order_books.items()}
        for agent in self.agents:
            if agent.status == "bankrupt":
                continue
            agent.process_loan_repayment(day, prices)
            if random.random() < agent._char.get("loan_prob", 0.2) and len(agent.loans) < 3:
                term_info = random.choice(LOAN_TERMS)
                amount = round(random.uniform(10000, 50000), 2)
                agent.add_loan(Loan(
                    id=str(uuid.uuid4()),
                    agent_id=str(agent.id),
                    amount=amount,
                    interest_rate=term_info["rate"],
                    term_days=term_info["term_days"],
                    start_day=day,
                    due_day=day + term_info["term_days"],
                    remaining=amount,
                ))

    def _generate_forum_posts(self, day: int):
        active_agents = [a for a in self.agents if a.status == "active"]
        if not active_agents:
            return
        prices = {s: (b.last_price or 100.0) for s, b in self.order_books.items()}
        for agent in random.sample(active_agents, min(3, len(active_agents))):
            init = agent._initial_total_value(prices)
            pnl_pct = (agent.pnl / init * 100) if init else 0
            if pnl_pct > 5:
                sentiment = "bullish"
                pool = [
                    f"Benchmark leadership looks durable in {self.current_regime}.",
                    f"Up {pnl_pct:.1f}% and still leaning into winners.",
                    "Breadth is supportive; staying constructive.",
                ]
            elif pnl_pct < -5:
                sentiment = "bearish"
                pool = [
                    f"Drawdown control matters in {self.current_regime}.",
                    "Reducing exposure until regime conditions stabilize.",
                    "Risk budget is tighter than expected today.",
                ]
            else:
                sentiment = "neutral"
                pool = [
                    "Positioning stays balanced while conviction is mixed.",
                    "Waiting for cleaner catalyst alignment before resizing.",
                    "No need to force risk when dispersion is doing the work.",
                ]
            self.forum_messages.append(ForumMessage(
                agent_id=str(agent.id),
                agent_name=agent.persona.get("name", f"Trader {agent.id}"),
                message=random.choice(pool),
                sentiment=sentiment,
                day=day,
            ))

    def _take_snapshot(self):
        prices = {s: (b.last_price or 100.0) for s, b in self.order_books.items()}
        summaries = [a.get_snapshot(prices) for a in self.agents]
        self.snapshots.append(DaySnapshot(
            day=self.day,
            prices=prices,
            agent_summaries=summaries,
            total_trades=self.total_trade_count,
            events_count=len([e for e in self.events if e.day == self.day]),
        ))

    def _update_market_analytics(self):
        current_prices = {s: (b.last_price or self.base_prices.get(s, 100.0)) for s, b in self.order_books.items()}
        benchmark_value = compute_index_level(current_prices, self.base_prices)
        self.benchmark_history.append({"day": self.day, "session": self.session, "value": benchmark_value})
        self.sector_index_history.append({
            "day": self.day,
            "session": self.session,
            "indices": compute_sector_indices(current_prices, self.stock_meta, self.base_prices),
        })
        current_notional = 0.0
        for sym, price in current_prices.items():
            current_notional += price * sum(agent.wallet["holdings"].get(sym, 0) for agent in self.agents)
        self.turnover = self._session_trade_notional / max(current_notional, 1.0)
        analytics = compute_market_analytics(self, current_prices, self.stock_meta)
        self.market_sentiment = analytics["market_sentiment"]
        self.session_risk = "Elevated" if analytics["realized_vol_pct"] > 18 or analytics["benchmark"]["drawdown_pct"] > 5 else "Normal"
        self.market_metrics_history.append({"day": self.day, "session": self.session, **analytics})

    async def step(self, market_state: Dict, news: str):
        active_agents = [a for a in self.agents if a.status == "active"]
        results = []
        if self.use_llm:
            llm_agents = [a for a in active_agents if a.agent_kind == "llm"]
            rule_agents = [a for a in active_agents if a.agent_kind == "rule"]
            for agent in rule_agents:
                try:
                    results.append(agent.demo_act(market_state))
                except Exception as exc:
                    logger.error("Rule agent %s error: %s", agent.id, exc)
            for i in range(0, len(llm_agents), LLM_BATCH_SIZE):
                batch = llm_agents[i:i + LLM_BATCH_SIZE]
                results.extend(await asyncio.gather(*[a.act(market_state, news) for a in batch], return_exceptions=True))
                if i + LLM_BATCH_SIZE < len(llm_agents):
                    await asyncio.sleep(LLM_BATCH_DELAY)
        else:
            for agent in active_agents:
                try:
                    results.append(agent.demo_act(market_state) if hasattr(agent, "demo_act") else None)
                except Exception as exc:
                    logger.error("Agent %s error: %s", agent.id, exc)

        for res in results:
            if isinstance(res, BaseException):
                logger.error("Agent error: %s", res)
                continue
            if res is not None and isinstance(res, Order) and res.stock_symbol not in self.halted_stocks:
                trades = self.order_books[res.stock_symbol].add_order(res) if res.stock_symbol in self.order_books else []
                if trades:
                    self._process_trades(trades)
                    self.all_trades.extend(trades)
                    self.total_trade_count += len(trades)

    def _process_trades(self, trades):
        agent_map = {str(a.id): a for a in self.agents}
        for trade in trades:
            buyer = agent_map.get(trade.buyer_agent_id)
            seller = agent_map.get(trade.seller_agent_id)
            cost = round(trade.price * trade.quantity, 2)
            if buyer and buyer.wallet["cash"] >= cost:
                buyer.wallet["cash"] -= cost
                buyer.wallet["holdings"][trade.stock_symbol] = buyer.wallet["holdings"].get(trade.stock_symbol, 0) + trade.quantity
            if seller:
                seller.wallet["cash"] += cost
                seller.wallet["holdings"][trade.stock_symbol] = max(0, seller.wallet["holdings"].get(trade.stock_symbol, 0) - trade.quantity)
            self._session_trade_notional += cost

    async def run_simulation(self, steps: Optional[int] = None):
        self._run_id += 1
        my_run_id = self._run_id
        self.is_running = True
        self.is_paused = False
        total_steps = steps or (self.total_days * self.sessions_per_day)
        start_step = self.day * self.sessions_per_day

        try:
            for step_i in range(start_step, total_steps):
                if not self.is_running or self._run_id != my_run_id:
                    break
                while self.is_paused:
                    await asyncio.sleep(0.5)
                    if not self.is_running:
                        return

                self.day = (step_i // self.sessions_per_day) + 1
                self.session = (step_i % self.sessions_per_day) + 1
                day_events = []

                try:
                    if self.session == 1:
                        self.halted_stocks.clear()
                        self._roll_regime(self.day)
                    self._session_open = {s: (b.last_price or 100.0) for s, b in self.order_books.items()}
                    self._session_trade_notional = 0.0

                    report_data = None
                    if self.session == 1:
                        day_events = self._generate_events(self.day)
                        self.events.extend(day_events)
                        self._process_loans(self.day)
                        report_data = self._generate_financial_reports(self.day)

                    sector_impacts = self._event_impact_by_sector(day_events)
                    sector_drifts = self._generate_sector_drifts(sector_impacts)
                    self._apply_correlated_walk(sector_drifts)

                    cb_events = self._check_circuit_breakers()
                    if cb_events:
                        self.events.extend(cb_events)
                        day_events.extend(cb_events)

                    prices = {s: (b.last_price or 100.0) for s, b in self.order_books.items()}
                    trends = {s: self._calculate_trend(s) for s in self.order_books}
                    bullish = sum(1 for t in trends.values() if t == "Bullish")
                    bearish = sum(1 for t in trends.values() if t == "Bearish")
                    self.market_sentiment = "bullish" if bullish > bearish else ("bearish" if bearish > bullish else "neutral")
                    self._update_market_analytics()
                    benchmark_value = self.benchmark_history[-1]["value"] if self.benchmark_history else 100.0
                    breadth_ratio = self.market_metrics_history[-1]["breadth"]["breadth_ratio"] if self.market_metrics_history else 0.5

                    market_state = {
                        "day": self.day,
                        "session": self.session,
                        "time": f"{9 + self.session}:30:00",
                        "prices": prices,
                        "trends": trends,
                        "sentiment": self.market_sentiment,
                        "volume_level": "High" if day_events else "Normal",
                        "is_high_volume": bool(day_events),
                        "timestamp": datetime.now(),
                        "events": [{"title": e.title, "severity": e.severity} for e in day_events],
                        "halted": self.halted_stocks,
                        "financial_report": report_data,
                        "regime": self.current_regime,
                        "regime_headline": self.current_regime_profile["headline"],
                        "benchmark_return_pct": benchmark_value - 100.0,
                        "breadth_ratio": breadth_ratio,
                    }
                    news = "; ".join(f"{e.title} ({e.severity})" for e in day_events) if day_events else "Market is stable. No major events."
                    await self.step(market_state, news)

                    for agent in self.agents:
                        agent._regime_performance[self.current_regime] = {"portfolio_value": agent.total_value}

                    if self.session == self.sessions_per_day:
                        self._generate_forum_posts(self.day)
                        self._take_snapshot()
                except Exception as exc:
                    logger.error("Step %s (day %s session %s) error: %s", step_i, self.day, self.session, exc, exc_info=True)

                if self.ws_broadcast:
                    try:
                        await self.ws_broadcast({
                            "type": "tick",
                            "day": self.day,
                            "session": self.session,
                            "prices": {s: (b.last_price or 100.0) for s, b in self.order_books.items()},
                            "trades": self.total_trade_count,
                            "agents": len([a for a in self.agents if a.status == "active"]),
                            "halted": list(self.halted_stocks),
                            "events": [{"title": e.title, "severity": e.severity} for e in day_events],
                            "regime": self.current_regime,
                            "benchmark": self.benchmark_history[-1] if self.benchmark_history else {"value": 100.0},
                        })
                    except Exception:
                        pass

                await asyncio.sleep(self.speed)
        finally:
            if self._run_id != my_run_id:
                return
            self.is_running = False
            if self.ws_broadcast:
                try:
                    await self.ws_broadcast({
                        "type": "complete",
                        "day": self.day,
                        "total_days": self.total_days,
                    })
                except Exception:
                    pass
