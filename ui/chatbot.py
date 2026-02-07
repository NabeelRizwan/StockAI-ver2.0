"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         StockAI - AI Chatbot Advisor                         ║
║              Market Analysis Assistant powered by LLM Integration            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os
import sys
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Rate limiting
try:
    from utils.rate_limiter import groq_limiter, gemini_limiter, RateLimitExceeded
except ImportError:
    groq_limiter = None
    gemini_limiter = None
    class RateLimitExceeded(Exception): pass

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CHATBOT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

QUICK_QUESTIONS = [
    "Which strategy is performing best?",
    "What's the current market sentiment?",
    "Which stocks should I watch?",
    "Explain the latest market event",
    "Who are the top performing agents?",
    "What's causing the volatility?",
    "Should I buy or sell right now?",
    "Analyze sector performance",
]

SYSTEM_PROMPT = """You are StockAI Advisor, an expert AI assistant for the StockAI Market Simulation platform. 
You help users understand market dynamics, agent behavior, and trading strategies within the simulation.

Your personality:
- Professional but approachable
- Data-driven and analytical
- Clear and concise in explanations
- Use relevant market terminology
- Offer actionable insights when possible

Current simulation context will be provided with each query. Use this data to give relevant, specific answers.
Keep responses concise (2-4 sentences for simple queries, up to a paragraph for complex analysis).
Use emojis sparingly to highlight key points (📈 📉 💡 ⚠️ ✅).
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CHATBOT CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class StockAIAdvisor:
    """AI-powered market advisor chatbot."""
    
    def __init__(self):
        self.groq_client = None
        self.gemini_model = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize LLM clients based on available API keys."""
        # Try Groq first (faster, free tier)
        groq_key = os.getenv("GROQ_API_KEY", "")
        if groq_key and GROQ_AVAILABLE:
            try:
                self.groq_client = Groq(api_key=groq_key)
            except Exception:
                pass
        
        # Try Gemini as fallback
        google_key = os.getenv("GOOGLE_API_KEY", "")
        if google_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=google_key)
                self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception:
                pass
    
    def is_available(self) -> bool:
        """Check if any LLM client is available."""
        return self.groq_client is not None or self.gemini_model is not None
    
    def get_provider_name(self) -> str:
        """Get the name of the active provider."""
        if self.groq_client:
            return "Groq (Llama 3.3)"
        elif self.gemini_model:
            return "Google Gemini"
        return "Unavailable"
    
    def generate_context(self, state: Any) -> str:
        """Generate context string from simulation state."""
        if not state or state.status == "IDLE":
            return "Simulation not yet started. No market data available."
        
        context_parts = []
        
        # Basic simulation info
        context_parts.append(f"📊 Simulation Status: {state.status}")
        context_parts.append(f"📅 Current Day: {state.current_day} / {state.total_days}")
        context_parts.append(f"📈 Volatility Setting: {state.volatility}")
        context_parts.append(f"⚠️ System Risk Level: {state.system_risk}")
        context_parts.append(f"🎭 Market Sentiment: {state.market_sentiment}")
        
        # Stock prices
        if state.stock_a and state.stock_b:
            context_parts.append(f"\n💹 Primary Stocks:")
            context_parts.append(f"  - {state.stock_a.name}: ${state.stock_a.price:.2f} ({state.stock_a.change_percent:+.2f}%)")
            context_parts.append(f"  - {state.stock_b.name}: ${state.stock_b.price:.2f} ({state.stock_b.change_percent:+.2f}%)")
        
        # Extra stocks summary
        if state.extra_stocks:
            context_parts.append(f"\n📦 Extended Market ({len(state.extra_stocks)} stocks):")
            for stock in state.extra_stocks[:5]:  # Top 5
                context_parts.append(f"  - {stock.name}: ${stock.price:.2f} ({stock.change_percent:+.2f}%)")
        
        # Agent summary
        context_parts.append(f"\n🤖 Agents:")
        context_parts.append(f"  - Active: {state.active_agents} / {state.agent_count}")
        bankruptcies = len([a for a in state.agents if a.is_bankrupt])
        if bankruptcies > 0:
            context_parts.append(f"  - Bankruptcies: {bankruptcies}")
        
        # Strategy performance
        strategies = {}
        for agent in state.agents:
            if agent.character not in strategies:
                strategies[agent.character] = []
            strategies[agent.character].append(agent.pnl_percent)
        
        if strategies:
            context_parts.append(f"\n📊 Strategy Performance (Avg P&L):")
            for strategy, pnls in strategies.items():
                avg_pnl = sum(pnls) / len(pnls) if pnls else 0
                context_parts.append(f"  - {strategy}: {avg_pnl:+.2f}%")
        
        # Recent events
        recent_events = [e for e in state.events if e.day <= state.current_day][-3:]
        if recent_events:
            context_parts.append(f"\n📰 Recent Events:")
            for event in recent_events:
                context_parts.append(f"  - Day {event.day}: {event.title} ({event.severity})")
        
        # Top agents
        sorted_agents = sorted(state.agents, key=lambda a: a.pnl_percent, reverse=True)[:3]
        if sorted_agents:
            context_parts.append(f"\n🏆 Top Agents:")
            for i, agent in enumerate(sorted_agents, 1):
                context_parts.append(f"  {i}. {agent.name} ({agent.character}): {agent.pnl_percent:+.2f}%")
        
        return "\n".join(context_parts)
    
    def ask(self, question: str, state: Any) -> str:
        """Send a question to the AI advisor and get a response."""
        if not self.is_available():
            return "⚠️ AI Advisor is not available. Please configure GROQ_API_KEY or GOOGLE_API_KEY in your .env file."
        
        # Build context
        context = self.generate_context(state)
        
        # Build the full prompt
        full_prompt = f"""
{SYSTEM_PROMPT}

--- CURRENT SIMULATION DATA ---
{context}

--- USER QUESTION ---
{question}

Please provide a helpful, data-driven response based on the simulation context above.
"""
        
        try:
            if self.groq_client:
                return self._ask_groq(full_prompt)
            elif self.gemini_model:
                return self._ask_gemini(full_prompt)
        except Exception as e:
            return f"⚠️ Error generating response: {str(e)}"
        
        return "⚠️ No AI provider available."
    
    def _ask_groq(self, prompt: str) -> str:
        """Query Groq API with rate limiting."""
        if not self.groq_client:
            return "⚠️ Groq client not available."
        
        # Apply rate limiting
        if groq_limiter:
            try:
                groq_limiter.acquire()
            except RateLimitExceeded:
                return "⚠️ Rate limit reached. Please wait a moment before asking another question."
        
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        content = response.choices[0].message.content
        return content if content else "No response generated."
    
    def _ask_gemini(self, prompt: str) -> str:
        """Query Google Gemini API with rate limiting."""
        if not self.gemini_model:
            return "⚠️ Gemini model not available."
        
        # Apply rate limiting
        if gemini_limiter:
            try:
                gemini_limiter.acquire()
            except RateLimitExceeded:
                return "⚠️ Rate limit reached. Please wait a moment before asking another question."
        
        response = self.gemini_model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    
    def get_connection_status(self) -> dict:
        """Get the current connection status for display."""
        return {
            "connected": self.groq_client is not None or self.gemini_model is not None,
            "provider": self.get_provider_name(),
            "groq_configured": self.groq_client is not None,
            "gemini_configured": self.gemini_model is not None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# STREAMLIT COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def init_chatbot_state():
    """Initialize chatbot session state."""
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I'm your **StockAI Advisor**. Ask me anything about the market simulation, trading strategies, or agent behavior!",
                "timestamp": datetime.now().strftime("%H:%M")
            }
        ]
    if "chatbot_advisor" not in st.session_state:
        st.session_state.chatbot_advisor = StockAIAdvisor()
    if "chatbot_input" not in st.session_state:
        st.session_state.chatbot_input = ""


def render_chatbot_sidebar(engine_state: Any):
    """Render the chatbot in the sidebar."""
    init_chatbot_state()
    advisor = st.session_state.chatbot_advisor
    
    with st.sidebar:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                ">🤖</div>
                <div>
                    <h3 style="margin: 0; font-size: 16px; font-weight: 700; color: #f8fafc;">AI Advisor</h3>
                    <p style="margin: 2px 0 0 0; font-size: 11px; color: #71717a;">""" + advisor.get_provider_name() + """</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Messages container
        messages_container = st.container()
        
        with messages_container:
            for msg in st.session_state.chatbot_messages[-10:]:  # Show last 10 messages
                if msg["role"] == "assistant":
                    st.markdown(f"""
                    <div style="
                        background: rgba(18, 18, 26, 0.8);
                        border: 1px solid rgba(255, 255, 255, 0.06);
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 8px;
                    ">
                        <div style="font-size: 13px; color: #a1a1aa; line-height: 1.5;">{msg["content"]}</div>
                        <div style="font-size: 10px; color: #52525b; margin-top: 6px;">{msg.get("timestamp", "")}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        background: rgba(59, 130, 246, 0.15);
                        border: 1px solid rgba(59, 130, 246, 0.3);
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 8px;
                        margin-left: 20px;
                    ">
                        <div style="font-size: 13px; color: #f8fafc; line-height: 1.5;">{msg["content"]}</div>
                        <div style="font-size: 10px; color: #52525b; margin-top: 6px; text-align: right;">{msg.get("timestamp", "")}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Quick questions
        st.markdown("##### 💡 Quick Questions")
        cols = st.columns(2)
        for i, q in enumerate(QUICK_QUESTIONS[:4]):
            with cols[i % 2]:
                if st.button(q[:20] + "..." if len(q) > 20 else q, key=f"quick_q_{i}", width='stretch'):
                    handle_chat_input(q, advisor, engine_state)
                    st.rerun()
        
        # Input
        user_input = st.text_input(
            "Ask anything...",
            key="chat_input_field",
            placeholder="Type your question here...",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Send", key="send_chat", width='stretch'):
                if user_input:
                    handle_chat_input(user_input, advisor, engine_state)
                    st.rerun()
        with col1:
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.chatbot_messages = [st.session_state.chatbot_messages[0]]
                st.rerun()


def handle_chat_input(question: str, advisor: StockAIAdvisor, state: Any):
    """Handle a chat input and generate response with streaming effect."""
    timestamp = datetime.now().strftime("%H:%M")
    
    # Check connection status
    status = advisor.get_connection_status()
    if not status["connected"]:
        st.session_state.chatbot_messages.append({
            "role": "user",
            "content": question,
            "timestamp": timestamp
        })
        st.session_state.chatbot_messages.append({
            "role": "assistant",
            "content": "⚠️ **No AI Provider Connected**\n\nPlease set up an API key to enable AI responses:\n- `GROQ_API_KEY` for Groq (free tier available)\n- `GOOGLE_API_KEY` for Google Gemini",
            "timestamp": datetime.now().strftime("%H:%M")
        })
        return
    
    # Add user message
    st.session_state.chatbot_messages.append({
        "role": "user",
        "content": question,
        "timestamp": timestamp
    })
    
    # Generate response with visual feedback
    with st.spinner("🤔 Thinking..."):
        response = advisor.ask(question, state)
    
    # Add assistant response
    st.session_state.chatbot_messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M")
    })


def render_floating_chatbot(engine_state: Any):
    """Render a floating 3D glass orb with particle animation that opens a chat dialog."""
    import streamlit.components.v1 as components
    
    init_chatbot_state()
    advisor = st.session_state.chatbot_advisor
    
    # Initialize chat open state
    if "chat_orb_open" not in st.session_state:
        st.session_state.chat_orb_open = False
    
    # Get connection status
    status = advisor.get_connection_status()
    is_connected = status["connected"]
    
    # Inject the 3D glass orb with particle animation into parent document
    components.html("""
    <script>
    (function() {
        const parentDoc = window.parent.document;
        
        // Remove existing orb if present
        const existingOrb = parentDoc.getElementById('stockai-glass-orb');
        const existingStyles = parentDoc.getElementById('stockai-orb-styles');
        if (existingOrb) existingOrb.remove();
        if (existingStyles) existingStyles.remove();
        
        // Inject comprehensive styles
        const styleEl = parentDoc.createElement('style');
        styleEl.id = 'stockai-orb-styles';
        styleEl.textContent = `
            @keyframes float-gentle {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-12px); }
            }
            @keyframes rotate-slow {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes particle-1 {
                0% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                100% { transform: translate(30px, -30px) scale(0.3); opacity: 0; }
            }
            @keyframes particle-2 {
                0% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                100% { transform: translate(-35px, -20px) scale(0.3); opacity: 0; }
            }
            @keyframes particle-3 {
                0% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                100% { transform: translate(25px, 28px) scale(0.3); opacity: 0; }
            }
            @keyframes particle-4 {
                0% { transform: translate(0, 0) scale(1); opacity: 0.8; }
                100% { transform: translate(-28px, 32px) scale(0.3); opacity: 0; }
            }
            @keyframes glow-pulse {
                0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.2), inset -2px -2px 8px rgba(0, 0, 0, 0.3), inset 2px 2px 8px rgba(255, 255, 255, 0.2); }
                50% { box-shadow: 0 0 35px rgba(139, 92, 246, 0.6), 0 0 60px rgba(59, 130, 246, 0.35), inset -2px -2px 8px rgba(0, 0, 0, 0.3), inset 2px 2px 8px rgba(255, 255, 255, 0.25); }
            }
            
            #stockai-glass-orb {
                position: fixed !important;
                bottom: 24px !important;
                right: 24px !important;
                width: 72px !important;
                height: 72px !important;
                border-radius: 50% !important;
                cursor: pointer !important;
                z-index: 2147483647 !important;
                background: radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 15%, rgba(139, 92, 246, 0.2) 40%, rgba(59, 130, 246, 0.1) 60%, transparent 70%), linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(59, 130, 246, 0.25) 50%, rgba(16, 185, 129, 0.15) 100%) !important;
                border: 2px solid rgba(255, 255, 255, 0.3) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                animation: float-gentle 4s ease-in-out infinite, glow-pulse 3s ease-in-out infinite !important;
                overflow: hidden !important;
                box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.2), inset -2px -2px 8px rgba(0, 0, 0, 0.3), inset 2px 2px 8px rgba(255, 255, 255, 0.2) !important;
            }
            
            #stockai-glass-orb::before {
                content: '' !important;
                position: absolute !important;
                top: 12% !important;
                left: 18% !important;
                width: 24px !important;
                height: 24px !important;
                background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), transparent) !important;
                border-radius: 50% !important;
                pointer-events: none !important;
                z-index: 1 !important;
            }
            
            #stockai-glass-orb:hover {
                transform: scale(1.15) translateY(-6px) !important;
                animation: none !important;
                box-shadow: 0 8px 32px rgba(139, 92, 246, 0.7), 0 0 60px rgba(59, 130, 246, 0.5), inset -2px -2px 8px rgba(0, 0, 0, 0.3), inset 2px 2px 12px rgba(255, 255, 255, 0.3) !important;
            }
            
            .orb-content {
                position: absolute !important;
                width: 100% !important;
                height: 100% !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                z-index: 10 !important;
            }
            
            .orb-icon {
                font-size: 32px !important;
                filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
            }
            
            .particle {
                position: absolute !important;
                border-radius: 50% !important;
                pointer-events: none !important;
            }
            
            .particle-1 {
                width: 6px !important;
                height: 6px !important;
                background: #a78bfa !important;
                top: 50% !important;
                left: 50% !important;
                animation: particle-1 2s ease-out infinite !important;
            }
            
            .particle-2 {
                width: 5px !important;
                height: 5px !important;
                background: #3b82f6 !important;
                top: 50% !important;
                left: 50% !important;
                animation: particle-2 2.5s ease-out 0.3s infinite !important;
            }
            
            .particle-3 {
                width: 6px !important;
                height: 6px !important;
                background: #10b981 !important;
                top: 50% !important;
                left: 50% !important;
                animation: particle-3 2.2s ease-out 0.6s infinite !important;
            }
            
            .particle-4 {
                width: 5px !important;
                height: 5px !important;
                background: #06b6d4 !important;
                top: 50% !important;
                left: 50% !important;
                animation: particle-4 2.7s ease-out 0.9s infinite !important;
            }
        `;
        parentDoc.head.appendChild(styleEl);
        
        // Create the floating glass orb
        const orb = parentDoc.createElement('div');
        orb.id = 'stockai-glass-orb';
        orb.innerHTML = `
            <div class="particle particle-1"></div>
            <div class="particle particle-2"></div>
            <div class="particle particle-3"></div>
            <div class="particle particle-4"></div>
            <div class="orb-content">
                <span class="orb-icon">�</span>
            </div>
        `;
        
        // Click handler to trigger chat
        orb.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            // Find and click the hidden Streamlit button
            const buttons = parentDoc.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.getAttribute('data-testid') === 'stBaseButton-secondary' && 
                    btn.textContent.includes('STOCKAI_ORB_TRIGGER')) {
                    btn.click();
                    return;
                }
            }
        };
        
        parentDoc.body.appendChild(orb);
    })();
    </script>
    """, height=0)
    
    # Hidden button to trigger the dialog via Streamlit state
    st.markdown("""
    <style>
    .stockai-hidden-trigger { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([20, 1])
    with col2:
        if st.button("STOCKAI_ORB_TRIGGER", key="stockai_orb_btn", help="Open AI Assistant"):
            st.session_state.chat_orb_open = True
            st.rerun()
    
    # Show the dialog when open
    if st.session_state.chat_orb_open:
        _show_chat_dialog(advisor, engine_state)


@st.dialog("💬 AI Market Advisor", width="large")
def _show_chat_dialog(advisor, engine_state):
    """Show the chat dialog with messaging-style bubbles."""
    status = advisor.get_connection_status()
    status_color = "#10b981" if status["connected"] else "#ef4444"
    status_text = status["provider"] if status["connected"] else "Not Connected"
    
    # Enhanced header with status
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; padding: 0 0 12px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 24px;">🤖</span>
            <div>
                <p style="margin: 0; font-size: 16px; font-weight: 600; color: #f8fafc;">AI Market Advisor</p>
                <p style="margin: 2px 0 0 0; font-size: 12px; color: #71717a;">Powered by {status_text}</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px; padding: 6px 12px; background: rgba(16, 185, 129, 0.15); border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.3);">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></div>
            <span style="font-size: 12px; color: {status_color}; font-weight: 500;">
                {"Connected" if status["connected"] else "Offline"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Messages container with custom styling
    st.markdown("""
    <style>
    .chat-messages {
        height: 280px;
        overflow-y: auto;
        padding: 12px 0;
        margin-bottom: 16px;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.15) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 14px;
        padding: 12px 14px;
        margin: 8px 0 8px 32px;
        word-wrap: break-word;
        color: #f8fafc;
        font-size: 14px;
        line-height: 1.4;
    }
    .chat-bubble-ai {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
        padding: 12px 14px;
        margin: 8px 32px 8px 0;
        word-wrap: break-word;
        color: #f8fafc;
        font-size: 14px;
        line-height: 1.4;
    }
    </style>
    <div class="chat-messages">
    """, unsafe_allow_html=True)
    
    # Render messages as bubbles
    for msg in st.session_state.chatbot_messages:
        if msg["role"] == "assistant":
            st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("**💡 Quick Questions**")
    qcols = st.columns(2)
    quick_qs = [
        ("📈 Best Strategy", "Which strategy is performing best right now?"),
        ("📊 Market Sentiment", "What's the current market sentiment based on our data?"),
        ("🏆 Top Agents", "Who are the top 3 performing agents?"),
        ("⚡ Volatility", "What factors are causing the current volatility?"),
    ]
    for i, (label, full_q) in enumerate(quick_qs):
        with qcols[i % 2]:
            if st.button(label, key=f"dlg_q_{i}", use_container_width=True):
                handle_chat_input(full_q, advisor, engine_state)
                st.rerun()
    
    # Chat input area
    st.markdown("---")
    user_input = st.text_input(
        "Message",
        key="dialog_chat_input",
        placeholder="Ask anything about the simulation...",
        label_visibility="collapsed"
    )
    
    # Action buttons
    cols = st.columns([3, 1, 1])
    with cols[1]:
        if st.button("🚀 Send", key="dialog_send", use_container_width=True, type="primary"):
            if user_input:
                handle_chat_input(user_input, advisor, engine_state)
                st.rerun()
    with cols[2]:
        if st.button("✕ Close", key="dialog_close", use_container_width=True):
            st.session_state.chat_orb_open = False
            st.rerun()


def render_chatbot_main(engine_state: Any):
    """Render a full chatbot interface in the main area."""
    init_chatbot_state()
    advisor = st.session_state.chatbot_advisor
    
    st.markdown("""
    <div style="
        background: rgba(22, 22, 32, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 20px;
    ">
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        ">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="
                    width: 56px;
                    height: 56px;
                    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
                    border-radius: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 28px;
                    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
                ">🤖</div>
                <div>
                    <h2 style="margin: 0; font-size: 24px; font-weight: 800; color: #f8fafc;">AI Market Advisor</h2>
                    <p style="margin: 4px 0 0 0; font-size: 14px; color: #a1a1aa;">
                        Powered by """ + advisor.get_provider_name() + """ • Ask anything about the simulation
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Messages
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### 💬 Conversation")
        for msg in st.session_state.chatbot_messages:
            if msg["role"] == "assistant":
                st.info(msg["content"])
            else:
                st.success(msg["content"])
        
        # Input
        user_input = st.text_area(
            "Your question",
            height=80,
            placeholder="Ask about market trends, strategies, agents, or any aspect of the simulation..."
        )
        
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            if st.button("🚀 Send", width='stretch'):
                if user_input:
                    handle_chat_input(user_input, advisor, engine_state)
                    st.rerun()
        with c2:
            if st.button("🗑️ Clear", width='stretch'):
                st.session_state.chatbot_messages = [st.session_state.chatbot_messages[0]]
                st.rerun()
    
    with col2:
        st.markdown("##### 💡 Quick Questions")
        for q in QUICK_QUESTIONS:
            if st.button(q, key=f"main_q_{q}", width='stretch'):
                handle_chat_input(q, advisor, engine_state)
                st.rerun()
        
        st.markdown("---")
        st.markdown("##### 📊 Current Context")
        context = advisor.generate_context(engine_state)
        st.text_area("Simulation Data", context, height=200, disabled=True)
