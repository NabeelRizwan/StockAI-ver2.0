"""Simulation control endpoints."""
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.app.state import simulation, agents, _build_world
from backend.app.models.types import SimulationConfig

router = APIRouter(prefix="/simulation", tags=["simulation"])
logger = logging.getLogger("api.simulation")


@router.get("/status")
async def get_status():
    from backend.app.state import market_books, STOCKS
    return {
        "is_running": simulation.is_running,
        "is_paused": simulation.is_paused,
        "day": simulation.day,
        "session": simulation.session,
        "total_days": simulation.total_days,
        "total_trades": simulation.total_trade_count,
        "active_agents": sum(1 for a in agents if a.status == "active"),
        "stocks": {
            s: {"name": STOCKS[s].name, "price": market_books[s].last_price or STOCKS[s].initial_price}
            for s in STOCKS
        },
    }


@router.post("/start")
async def start_simulation(background_tasks: BackgroundTasks):
    if simulation.is_running and not simulation.is_paused:
        return {"message": "Simulation already running"}
    if simulation.is_paused:
        simulation.is_paused = False
        return {"message": "Simulation resumed"}
    # Auto-reset if previous run completed
    if simulation.day >= simulation.total_days and not simulation.is_running:
        _build_world()
        logger.info("Auto-reset after completed simulation")
    from backend.app.state import simulation as sim
    background_tasks.add_task(sim.run_simulation)
    return {"message": "Simulation started", "agents": len(agents), "days": simulation.total_days}


@router.post("/pause")
async def pause_simulation():
    if not simulation.is_running:
        return {"message": "Simulation not running"}
    simulation.is_paused = True
    return {"message": "Simulation paused"}


@router.post("/stop")
async def stop_simulation():
    simulation.is_running = False
    simulation.is_paused = False
    return {"message": "Simulation stopped"}


@router.post("/reset")
async def reset_simulation():
    simulation.is_running = False
    simulation.is_paused = False
    _build_world()
    return {"message": "Simulation reset"}


@router.post("/config")
async def update_config(cfg: SimulationConfig):
    if simulation.is_running:
        raise HTTPException(400, "Stop simulation before changing config")
    _build_world(config=cfg.model_dump())
    return {"message": "Configuration updated", "config": cfg.model_dump()}


@router.get("/snapshots")
async def list_snapshots():
    """List available day snapshots."""
    return [{"day": s.day, "trades": s.total_trades, "events": s.events_count}
            for s in simulation.snapshots]


@router.get("/snapshots/{day}")
async def get_snapshot(day: int):
    """Get full state snapshot for a specific day."""
    for s in simulation.snapshots:
        if s.day == day:
            return s.model_dump()
    raise HTTPException(404, f"No snapshot for day {day}")
