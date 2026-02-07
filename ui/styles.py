"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         StockAI - Premium CSS Styles                         ║
║              Modular styling for the Market Simulation Platform              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# CSS Variables and Design Tokens
CSS_VARIABLES = """
:root {
    /* Backgrounds */
    --bg-primary: #06060a;
    --bg-secondary: #0c0c12;
    --bg-tertiary: #12121a;
    --bg-card: rgba(22, 22, 32, 0.8);
    --bg-card-solid: #161620;
    --bg-card-hover: rgba(30, 30, 44, 0.9);
    --bg-glass: rgba(255, 255, 255, 0.03);
    
    /* Text */
    --text-primary: #f8fafc;
    --text-secondary: #a1a1aa;
    --text-muted: #71717a;
    --text-dim: #52525b;
    
    /* Accent Colors */
    --accent-green: #10b981;
    --accent-green-dim: rgba(16, 185, 129, 0.15);
    --accent-red: #ef4444;
    --accent-red-dim: rgba(239, 68, 68, 0.15);
    --accent-blue: #3b82f6;
    --accent-blue-dim: rgba(59, 130, 246, 0.15);
    --accent-purple: #8b5cf6;
    --accent-purple-dim: rgba(139, 92, 246, 0.15);
    --accent-yellow: #f59e0b;
    --accent-yellow-dim: rgba(245, 158, 11, 0.15);
    --accent-cyan: #06b6d4;
    --accent-pink: #ec4899;
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, #10b981 0%, #3b82f6 50%, #8b5cf6 100%);
    --gradient-green: linear-gradient(135deg, #10b981 0%, #059669 100%);
    --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
    --gradient-warm: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
    --gradient-dark: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    
    /* Borders */
    --border-subtle: rgba(255, 255, 255, 0.06);
    --border-light: rgba(255, 255, 255, 0.1);
    --border-medium: rgba(255, 255, 255, 0.15);
    
    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
    --shadow-glow-green: 0 0 40px rgba(16, 185, 129, 0.3);
    --shadow-glow-blue: 0 0 40px rgba(59, 130, 246, 0.3);
    --shadow-glow-purple: 0 0 40px rgba(139, 92, 246, 0.3);
    
    /* Spacing */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;
}
"""

# Chatbot-specific styles
CHATBOT_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   AI CHATBOT ADVISOR
   ═══════════════════════════════════════════════════════════════════════════════ */
.chatbot-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 16px;
}

.chatbot-header {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 12px;
}

.chatbot-header-icon {
    width: 40px;
    height: 40px;
    background: var(--gradient-purple);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.chatbot-header-text h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
}

.chatbot-header-text p {
    margin: 2px 0 0 0;
    font-size: 12px;
    color: var(--text-muted);
}

.chatbot-messages {
    max-height: 400px;
    overflow-y: auto;
    padding: 16px;
}

.chat-message {
    margin-bottom: 16px;
    display: flex;
    gap: 12px;
}

.chat-message.user {
    flex-direction: row-reverse;
}

.chat-avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.chat-avatar.ai {
    background: var(--gradient-purple);
}

.chat-avatar.user {
    background: var(--gradient-blue);
}

.chat-bubble {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: var(--radius-md);
    font-size: 14px;
    line-height: 1.6;
}

.chat-bubble.ai {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--border-subtle);
}

.chat-bubble.user {
    background: var(--accent-blue-dim);
    color: var(--text-primary);
    border: 1px solid rgba(59, 130, 246, 0.3);
}

.chat-input-container {
    padding: 16px;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    gap: 12px;
}

.quick-questions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 12px 16px;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-glass);
}

.quick-question {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-full);
    padding: 8px 16px;
    font-size: 12px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-question:hover {
    background: var(--bg-card-hover);
    border-color: var(--accent-purple);
    color: var(--text-primary);
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 8px 0;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: var(--accent-purple);
    border-radius: 50%;
    animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 100% { opacity: 0.3; transform: translateY(0); }
    50% { opacity: 1; transform: translateY(-4px); }
}
"""

# Stock cards styles
STOCK_CARD_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   STOCK CARDS - Enhanced with Sector Colors
   ═══════════════════════════════════════════════════════════════════════════════ */
.stock-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.stock-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    opacity: 0.8;
}

.stock-card:hover {
    transform: translateY(-4px);
    border-color: var(--border-medium);
    box-shadow: var(--shadow-lg);
}

.stock-card.sector-tech::before { background: linear-gradient(90deg, #3b82f6, #8b5cf6); }
.stock-card.sector-energy::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }
.stock-card.sector-retail::before { background: linear-gradient(90deg, #f59e0b, #22c55e); }
.stock-card.sector-crypto::before { background: linear-gradient(90deg, #f59e0b, #eab308); }
.stock-card.sector-automotive::before { background: linear-gradient(90deg, #ef4444, #f97316); }
.stock-card.sector-entertainment::before { background: linear-gradient(90deg, #dc2626, #ec4899); }
.stock-card.sector-ai::before { background: linear-gradient(90deg, #8b5cf6, #06b6d4); }
.stock-card.sector-semiconductors::before { background: linear-gradient(90deg, #84cc16, #22c55e); }
.stock-card.sector-finance::before { background: linear-gradient(90deg, #0ea5e9, #3b82f6); }

.stock-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.stock-name {
    display: flex;
    align-items: center;
    gap: 10px;
}

.stock-emoji {
    font-size: 28px;
}

.stock-ticker {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
}

.stock-sector {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: var(--radius-full);
    background: var(--bg-glass);
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stock-price {
    font-size: 32px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.stock-change {
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.stock-change.positive {
    color: var(--accent-green);
}

.stock-change.negative {
    color: var(--accent-red);
}

.stock-description {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 12px;
    line-height: 1.5;
}

.stock-mini-chart {
    margin-top: 16px;
    height: 60px;
    background: var(--bg-glass);
    border-radius: var(--radius-sm);
    overflow: hidden;
}
"""

# News ticker styles
NEWS_TICKER_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   NEWS TICKER
   ═══════════════════════════════════════════════════════════════════════════════ */
.news-ticker-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 20px;
}

.news-ticker-header {
    padding: 12px 20px;
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.15), rgba(245, 158, 11, 0.15));
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-yellow);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.news-ticker {
    overflow: hidden;
    white-space: nowrap;
    padding: 12px 0;
}

.news-ticker-content {
    display: inline-block;
    animation: ticker 60s linear infinite;
}

.news-ticker-content:hover {
    animation-play-state: paused;
}

.news-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 40px;
    color: var(--text-secondary);
    font-size: 14px;
}

.news-item .severity-high { color: var(--accent-red); }
.news-item .severity-medium { color: var(--accent-yellow); }
.news-item .severity-low { color: var(--accent-green); }

.news-item .stock-mention {
    background: var(--accent-blue-dim);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    color: var(--accent-blue);
    font-weight: 600;
}

@keyframes ticker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
"""

# Loading and notification styles
NOTIFICATION_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   LOADING & NOTIFICATIONS
   ═══════════════════════════════════════════════════════════════════════════════ */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(6, 6, 10, 0.8);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid var(--border-subtle);
    border-top-color: var(--accent-green);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.toast-notification {
    position: fixed;
    bottom: 24px;
    right: 24px;
    padding: 16px 24px;
    border-radius: var(--radius-md);
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: slideIn 0.3s ease-out;
    z-index: 1001;
    box-shadow: var(--shadow-lg);
}

.toast-notification.success {
    background: var(--accent-green-dim);
    border: 1px solid var(--accent-green);
    color: var(--accent-green);
}

.toast-notification.error {
    background: var(--accent-red-dim);
    border: 1px solid var(--accent-red);
    color: var(--accent-red);
}

.toast-notification.info {
    background: var(--accent-blue-dim);
    border: 1px solid var(--accent-blue);
    color: var(--accent-blue);
}

.toast-notification.warning {
    background: var(--accent-yellow-dim);
    border: 1px solid var(--accent-yellow);
    color: var(--accent-yellow);
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Tooltip styles */
.tooltip-container {
    position: relative;
    display: inline-block;
}

.tooltip-content {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--bg-card-solid);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-size: 12px;
    color: var(--text-secondary);
    white-space: nowrap;
    z-index: 100;
    transition: all 0.2s ease;
    margin-bottom: 8px;
}

.tooltip-container:hover .tooltip-content {
    visibility: visible;
    opacity: 1;
}
"""

# Floating Chat Orb Widget
FLOATING_ORB_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   FLOATING CHAT ORB WIDGET
   ═══════════════════════════════════════════════════════════════════════════════ */

/* Chat Orb Button */
.chat-orb-btn {
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    width: 64px !important;
    height: 64px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 50%, #06b6d4 100%) !important;
    border: none !important;
    cursor: pointer !important;
    z-index: 99999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 
        0 4px 20px rgba(139, 92, 246, 0.4),
        0 8px 40px rgba(59, 130, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 0 !important;
    min-height: 64px !important;
}

.chat-orb-btn:hover {
    transform: scale(1.1) translateY(-4px) !important;
    box-shadow: 
        0 8px 32px rgba(139, 92, 246, 0.5),
        0 16px 64px rgba(59, 130, 246, 0.4) !important;
}

.chat-orb-btn::before {
    content: '' !important;
    position: absolute !important;
    top: -50% !important;
    left: -50% !important;
    width: 200% !important;
    height: 200% !important;
    background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 60%) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}

.chat-orb-btn:hover::before { opacity: 1 !important; }

/* Pulse animation */
@keyframes orb-pulse {
    0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
    70% { box-shadow: 0 0 0 20px rgba(139, 92, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
}

.chat-orb-btn.pulse {
    animation: orb-pulse 2s infinite !important;
}

/* Floating Chat Window */
.floating-chat-window {
    position: fixed;
    bottom: 110px;
    right: 30px;
    width: 380px;
    max-height: 520px;
    background: rgba(12, 12, 18, 0.95);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 
        0 24px 80px rgba(0, 0, 0, 0.6),
        0 8px 32px rgba(139, 92, 246, 0.15);
    overflow: hidden;
    z-index: 99998;
    animation: chatWindowSlideIn 0.3s ease-out;
}

@keyframes chatWindowSlideIn {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.floating-chat-header {
    padding: 20px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.floating-chat-header-info {
    display: flex;
    align-items: center;
    gap: 14px;
}

.floating-chat-avatar {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.floating-chat-title {
    margin: 0;
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
}

.floating-chat-subtitle {
    margin: 2px 0 0 0;
    font-size: 12px;
    color: #71717a;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse-status 2s ease infinite;
}

@keyframes pulse-status {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.floating-chat-close {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #a1a1aa;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    transition: all 0.2s ease;
}

.floating-chat-close:hover {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
}

.floating-chat-messages {
    height: 280px;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.floating-chat-messages::-webkit-scrollbar { width: 4px; }
.floating-chat-messages::-webkit-scrollbar-track { background: transparent; }
.floating-chat-messages::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }

.floating-chat-message {
    display: flex;
    gap: 10px;
    animation: messageIn 0.3s ease;
}

@keyframes messageIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.floating-chat-message.user { flex-direction: row-reverse; }

.floating-msg-avatar {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.floating-msg-avatar.ai { background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); }
.floating-msg-avatar.user { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }

.floating-chat-bubble {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.5;
}

.floating-chat-bubble.ai {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #e4e4e7;
    border-bottom-left-radius: 4px;
}

.floating-chat-bubble.user {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #f8fafc;
    border-bottom-right-radius: 4px;
}

.floating-chat-time {
    font-size: 10px;
    color: #52525b;
    margin-top: 6px;
}

.floating-chat-quick {
    padding: 12px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.floating-quick-btn {
    padding: 8px 14px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    color: #a1a1aa;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.floating-quick-btn:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.3);
    color: #c4b5fd;
}

.floating-chat-input-area {
    padding: 16px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    gap: 12px;
    align-items: center;
}

.floating-chat-footer {
    padding: 10px 20px;
    text-align: center;
    font-size: 11px;
    color: #52525b;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}

/* Responsive */
@media (max-width: 480px) {
    .chat-orb-btn { bottom: 20px !important; right: 20px !important; width: 56px !important; height: 56px !important; min-height: 56px !important; }
    .floating-chat-window { width: calc(100vw - 40px); max-width: 380px; bottom: 90px; right: 20px; }
}
"""

# Mobile responsive styles
MOBILE_STYLES = """
/* ═══════════════════════════════════════════════════════════════════════════════
   MOBILE RESPONSIVE STYLES
   ═══════════════════════════════════════════════════════════════════════════════ */

/* Tablet breakpoint */
@media (max-width: 992px) {
    .metric-card { padding: 18px !important; }
    .metric-value { font-size: 28px !important; }
    .section-title { font-size: 22px !important; }
}

/* Mobile breakpoint */
@media (max-width: 768px) {
    /* Metric cards */
    .metric-card { 
        padding: 16px !important; 
        margin-bottom: 12px !important;
    }
    .metric-value { font-size: 24px !important; }
    .metric-icon { font-size: 20px !important; }
    .metric-label { font-size: 12px !important; }
    
    /* Section titles */
    .section-title { font-size: 20px !important; }
    .section-subtitle { font-size: 13px !important; }
    
    /* Info cards */
    .info-card { padding: 16px !important; }
    
    /* Agent rows */
    .agent-row { 
        padding: 12px !important; 
        flex-wrap: wrap; 
        gap: 8px;
    }
    .agent-pnl { 
        margin-top: 8px; 
        width: 100%; 
        text-align: left; 
    }
    .agent-rank { font-size: 16px !important; }
    
    /* Charts - ensure they're not cut off */
    .js-plotly-plot { min-height: 280px !important; }
    
    /* Status badges */
    .status-badge { 
        padding: 4px 10px !important; 
        font-size: 11px !important; 
    }
    
    /* News ticker */
    .news-ticker { font-size: 13px !important; }
    .news-ticker-item { padding: 0 20px !important; }
}

/* Small mobile breakpoint */
@media (max-width: 480px) {
    /* Extra small screens */
    .metric-card { 
        padding: 12px !important; 
        margin-bottom: 8px !important; 
    }
    .metric-value { font-size: 20px !important; }
    .metric-label { font-size: 11px !important; }
    .metric-icon { font-size: 18px !important; }
    
    /* Section titles */
    .section-title { font-size: 18px !important; }
    .section-subtitle { font-size: 12px !important; }
    
    /* Info cards more compact */
    .info-card { 
        padding: 12px !important; 
        border-radius: 10px !important;
    }
    
    /* Agent rows stack vertically */
    .agent-row {
        flex-direction: column;
        align-items: flex-start !important;
    }
    .agent-info { margin-bottom: 8px; }
    
    /* Reduce chart heights on mobile */
    .js-plotly-plot { min-height: 220px !important; }
    
    /* Reduce padding */
    .stApp > header { padding: 0.5rem !important; }
    
    /* News ticker smaller */
    .news-ticker { font-size: 12px !important; }
    
    /* Empty states */
    .empty-state-icon { font-size: 48px !important; }
    .empty-state-title { font-size: 18px !important; }
}

/* Touch-friendly buttons and controls */
@media (hover: none) and (pointer: coarse) {
    button, .stButton > button {
        min-height: 44px !important;
        min-width: 44px !important;
    }
    
    /* Larger touch targets */
    .stSelectbox > div > div,
    .stSlider > div > div {
        min-height: 44px !important;
    }
    
    /* Better spacing for touch */
    .stTabs [data-baseweb="tab"] {
        padding: 12px 16px !important;
    }
}

/* Landscape mobile */
@media (max-height: 500px) and (orientation: landscape) {
    .metric-card { padding: 10px !important; }
    .metric-value { font-size: 18px !important; }
    .section-title { font-size: 16px !important; margin-bottom: 8px !important; }
}

/* High DPI screens */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .metric-card, .info-card {
        border-width: 0.5px !important;
    }
}
"""


def get_all_styles():
    """Return all CSS styles combined."""
    return f"""
<style>
{CSS_VARIABLES}
{CHATBOT_STYLES}
{STOCK_CARD_STYLES}
{NEWS_TICKER_STYLES}
{NOTIFICATION_STYLES}
{FLOATING_ORB_STYLES}
{MOBILE_STYLES}
</style>
"""
