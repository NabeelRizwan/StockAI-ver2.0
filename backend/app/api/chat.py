"""Chat endpoint — wraps the chatbot module."""
import logging
from fastapi import APIRouter
from backend.app.state import chat_engine, _init_chat_engine, simulation, market_books, STOCKS
from backend.app.models.types import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger("api.chat")


@router.post("")
async def chat(req: ChatRequest):
    _init_chat_engine()
    from backend.app.state import chat_engine as engine
    if engine is None:
        return {
            "response": "Chat is unavailable — GROQ_API_KEY may not be set.",
            "confidence": "low",
            "suggested_followup": None,
        }

    # Update simulation context
    try:
        prices = {s: (market_books[s].last_price or STOCKS[s].initial_price) for s in STOCKS}
        context = {
            "day": simulation.day,
            "session": simulation.session,
            "is_running": simulation.is_running,
            "prices": {s: round(p, 2) for s, p in prices.items()},
            "total_trades": simulation.total_trade_count,
        }
        engine.context_data = context
    except Exception:
        pass

    try:
        result = engine.process_message(req.message)
        return {
            "response": result.text,
            "confidence": result.confidence,
            "suggested_followup": result.suggested_followup,
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {
            "response": "Sorry, I encountered an error processing your message.",
            "confidence": "low",
            "suggested_followup": None,
        }
