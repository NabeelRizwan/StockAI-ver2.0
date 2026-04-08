# 📈 Stock AI — Multi-Agent Trading Simulation System
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

StockAI v2.0 is a local-first research platform for hybrid synthetic US equities market simulation. It combines a FastAPI backend with static HTML frontends for the landing page, research workspace, simulator console, and live-market intelligence layer. Researchers and bot builders can configure persistent runs, inspect agent behavior, evaluate strategy bots, compare experiments, and export research data.

Live deployment: https://stockai-ver2-0.onrender.com/

## 📌 Overview

**Stock AI** is a simulation-based system that models stock market trading using multiple intelligent agents. Each agent represents an independent trader that analyzes market conditions and makes decisions such as **BUY, SELL, or HOLD**.

The project focuses on demonstrating how **AI-driven decision systems** can be applied to financial environments by combining structured reasoning, simulation flow, and modular system design.

Modern AI-based trading systems rely on analyzing large volumes of market data and generating insights or predictions to guide decisions ([AI Tech Suite][1]). This project replicates a simplified version of such systems using agent-based modeling.

---

## What Is Deployed

- A landing page at `/`
- A research workspace at `/workspace`
- A simulator dashboard at `/app`
- A live-market intelligence surface at `/live-market`
- A FastAPI backend serving market, simulation, agents, chat, data, and websocket routes
- Research APIs for runs, scenarios, experiments, datasets, bots, evaluations, jobs, and run-scoped event streams
- Live simulation state including stocks, agents, trades, events, forum activity, loans, financial reports, and persistent run events
- Optional LLM-backed features through provider keys configured in `.env`

## Features

- Multi-agent market simulation with LLM, deterministic, and Python strategy-SDK agents
- Persistent run, scenario, dataset, experiment, bot, evaluation, and job records backed by SQLite
- Session-phase aware market kernel with latency, slippage, market orders, partial fills, and queue-priority matching
- Live stock prices, recent trades, market depth, price history, and run-scoped event tape
- Research workspace for dataset/scenario/bot discovery and experiment comparison
- Simulation lifecycle controls for start, pause, stop, reset, config updates, extension, and run launch
- Agent analytics, explainability summaries, decision logs, custom agent creation, and strategy-bot evaluation
- Exportable structured data for downstream analysis and research bundles
- Static frontend served directly from the FastAPI app for simpler deployment

## 🧠 Core Concept

The system is built around the idea of **autonomous trading agents**, where:

* Each agent simulates a trader
* Decisions are based on market inputs and reasoning logic
* Agents operate independently within a shared environment
* The system evaluates behavior across multiple iterations

---

## ⚙️ Agent Decision Pipeline

Each agent follows a structured workflow:

### 1. Input Processing

Agents receive:

* Stock price data
* Market trends
* External signals (news/events if available)

### 2. Reasoning Layer

* Inputs are analyzed using structured logic / prompt-driven reasoning
* The system simulates human-like decision making
* Contextual understanding is applied before taking action

### 3. Decision Output

Agents generate one of:

* **BUY**
* **SELL**
* **HOLD**

### 4. Execution Layer

* Portfolio is updated
* Balance is adjusted
* Actions are recorded for analysis

---

## 🏗️ System Architecture

The project follows a modular design:

```
Stock AI System
│
├── Agent Layer
│   ├── Decision Logic
│   ├── Action Execution
│
├── Market Layer
│   ├── Stock Data Handling
│   ├── Market Conditions
│
├── Simulation Engine
│   ├── Iteration Loop
│   ├── Agent Coordination
│
├── Logging & Records
│   ├── Trade History
│   ├── Performance Tracking
```

This structure ensures separation of concerns and improves maintainability.

---
## 🧠 AI Agent Workflow (Detailed)

The core of the system is built around intelligent trading agents that follow a structured decision-making pipeline. Each agent simulates a real-world trader by processing inputs, reasoning about market conditions, and executing actions.

### 🔄 End-to-End Workflow

```text
Market Data → Input Processing → Reasoning → Decision → Validation → Execution → Logging
```

### 1. 📥 Input Collection & Preprocessing

Each agent begins by collecting relevant information from the environment:

* Current stock prices
* Historical trends (if available)
* External signals (e.g., news, events)
* Internal state (portfolio, balance, past actions)

The data is structured into a consistent format so that it can be processed efficiently by the agent.

### 2. 🧠 Contextual Understanding

Before making a decision, the agent builds context:

* Identifies whether the market is **bullish, bearish, or neutral**
* Evaluates recent price movements
* Considers external signals that may impact price behavior

This step ensures that decisions are not random but grounded in observable conditions.

### 3. 🤖 Reasoning Layer (AI / Prompt-Driven Logic)

The reasoning layer is the core intelligence of the agent:

#### Inputs Transformation

* Inputs are transformed into structured prompts or logical conditions

#### Decision Factors

* Risk vs reward
* Market momentum
* Current portfolio exposure

#### Example Reasoning

* “Price is rising steadily → potential buy opportunity”
* “Negative sentiment detected → consider selling”

### 4. ⚖️ Decision Generation

Based on reasoning, the agent produces a structured decision:

* **BUY** → Invest in stock
* **SELL** → Liquidate holdings
* **HOLD** → Take no action

The decision is generated in a consistent format to ensure it can be processed reliably by the system.

### 5. ✅ Decision Validation

Before execution, decisions are validated against constraints:

* Available balance (for BUY)
* Portfolio holdings (for SELL)
* Risk limits or exposure thresholds

This step prevents unrealistic or invalid actions.

### 6. 💼 Execution Layer

Validated decisions are executed:

* Portfolio is updated
* Balance is adjusted
* Trade details are recorded

This step reflects the actual impact of agent decisions within the simulation.

### 7. 📊 Logging & Tracking

All actions are logged for analysis:

* Decision taken (BUY/SELL/HOLD)
* Input conditions at the time of decision
* Resulting portfolio changes

#### Purpose

* Performance evaluation
* Debugging
* Behavioral analysis of agents

### 8. 🔁 Iterative Learning Behavior (Simulation Loop)

The system runs in multiple iterations:

* Agents continuously receive updated market data
* Decisions evolve based on previous outcomes
* Behavior becomes more consistent over time

This iterative process simulates real trading environments where decisions are made repeatedly under changing conditions.

### 🎯 Key Characteristics of the Agent System

* **Autonomous** → Each agent acts independently
* **State-aware** → Decisions consider past actions and current portfolio
* **Context-driven** → Based on market conditions and signals
* **Modular** → Easy to extend or improve reasoning logic
* **Deterministic Output** → Structured BUY/SELL/HOLD decisions


## 🚀 Features

* Multi-agent trading simulation
* AI-inspired decision-making system
* Modular architecture for extensibility
* Simulation of real-world trading scenarios
* Logging of agent behavior and performance
* Clear agent interaction workflow

---

## 🛠️ Tech Stack

* **Language:** Python
* **Concepts:**

  * Agent-based systems
  * Simulation modeling
  * AI/LLM-inspired reasoning
* **Libraries (typical):**

  * Pandas / NumPy (data handling)
  * Standard Python modules

---

## 📂 Project Structure

```
.
├── agent.py          # Core agent behavior and decision logic
├── stock.py          # Market data handling
├── main.py           # Simulation entry point
├── secretary.py      # Coordination between agents
├── record.py         # Logging and tracking results
├── prompt/           # Prompt templates for reasoning
```

---

## 🔄 Simulation Flow

1. Initialize agents and environment
2. Load market data
3. Run multiple trading iterations
4. Agents analyze → decide → execute
5. Record actions and update state
6. Generate final summary

---

## 📊 Output

The system provides:

* Agent-level decisions (BUY / SELL / HOLD)
* Trading logs
* Performance tracking
* Final simulation results

---

## 🚀 My Contributions

* Worked on **AI agent decision logic and reasoning flow**
* Contributed to understanding and structuring the **agent pipeline (input → reasoning → action)**
* Improved clarity of how agents simulate **real-world trading behavior**
* Added documentation to explain **agent architecture and system design**
* Assisted in improving overall **code readability and structure**

---

## ⚠️ Note

This project was developed collaboratively.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## 🔮 Future Improvements

* Integration with real-time market data APIs
* Advanced risk management strategies
* More sophisticated agent reasoning models
* Visualization dashboards for performance
* Enhanced multi-agent interaction strategies

---

## 👥 Credits

* Team: Nabeel Rizwan, Riyan Ozair , Mohammed Sami

---

## 📜 Disclaimer

This project is for educational and simulation purposes only.
It does not provide financial advice or guarantee trading performance.

---
