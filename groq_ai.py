import streamlit as st
from groq import Groq

# Groq API Configuration
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = ""

bot_name = "Crystaline"

# Initialize Groq client
def get_groq_client():
    api_key = GROQ_API_KEY or st.session_state.get("groq_api_key", "")
    if api_key:
        return Groq(api_key=api_key)
    return None

# Get response from Groq
def get_response(prompt):
    client = get_groq_client()
    if not client:
        return "⚠️ Please enter your Groq API key in the sidebar to start chatting."
    
    try:
        # Get chat history for context
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        
        # Add conversation history (last 10 messages for context)
        for msg in st.session_state.messages[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nPlease check your API key and try again."

# Page configuration
st.set_page_config(
    page_title=f"Chat with {bot_name}",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "theme_style" not in st.session_state:
    st.session_state.theme_style = "cyberpunk"
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""

# Theme configurations
themes = {
    "cyberpunk": {
        "primary": "#00f0ff",
        "secondary": "#ff00ff",
        "bg_gradient": "linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%)",
        "card_bg": "rgba(26, 26, 46, 0.8)",
        "text": "#e0e0ff",
        "user_bubble": "linear-gradient(135deg, #00f0ff 0%, #ff00ff 100%)",
        "bot_bubble": "rgba(26, 26, 46, 0.9)",
        "glow": "0 0 20px rgba(0, 240, 255, 0.5)",
    },
    "gradient": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "card_bg": "rgba(255, 255, 255, 0.95)",
        "text": "#2d3748",
        "user_bubble": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "bot_bubble": "rgba(255, 255, 255, 0.95)",
        "glow": "0 4px 20px rgba(102, 126, 234, 0.3)",
    },
    "terminal": {
        "primary": "#00ff00",
        "secondary": "#00aa00",
        "bg_gradient": "linear-gradient(135deg, #000000 0%, #0a0a0a 100%)",
        "card_bg": "rgba(0, 20, 0, 0.9)",
        "text": "#00ff00",
        "user_bubble": "linear-gradient(135deg, #00ff00 0%, #00aa00 100%)",
        "bot_bubble": "rgba(0, 20, 0, 0.9)",
        "glow": "0 0 10px rgba(0, 255, 0, 0.5)",
    },
    "bubble": {
        "primary": "#25D366",
        "secondary": "#128C7E",
        "bg_gradient": "linear-gradient(135deg, #ece5dd 0%, #d9d9d9 100%)",
        "card_bg": "rgba(255, 255, 255, 0.95)",
        "text": "#303030",
        "user_bubble": "linear-gradient(135deg, #25D366 0%, #128C7E 100%)",
        "bot_bubble": "rgba(255, 255, 255, 0.95)",
        "glow": "0 2px 10px rgba(0, 0, 0, 0.1)",
    },
    "professional": {
        "primary": "#3b82f6",
        "secondary": "#8b5cf6",
        "bg_gradient": "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
        "card_bg": "rgba(30, 41, 59, 0.9)",
        "text": "#e2e8f0",
        "user_bubble": "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
        "bot_bubble": "rgba(30, 41, 59, 0.9)",
        "glow": "0 4px 15px rgba(59, 130, 246, 0.2)",
    }
}

current_theme = themes[st.session_state.theme_style]

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    .stApp {{
        background: {current_theme['bg_gradient']};
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    #MainMenu, footer {{visibility: hidden;}}
    
    [data-testid="stSidebar"] {{
        background: {current_theme['card_bg']};
        backdrop-filter: blur(10px);
        border-right: 2px solid {current_theme['primary']};
        box-shadow: {current_theme['glow']};
    }}
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {current_theme['primary']};
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px {current_theme['primary']};
    }}
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{
        color: {current_theme['text']};
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: bold;
        color: {current_theme['primary']};
        text-shadow: 0 0 15px {current_theme['primary']};
        font-family: 'Orbitron', sans-serif;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {current_theme['text']};
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stButton button {{
        background: linear-gradient(135deg, {current_theme['primary']} 0%, {current_theme['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: {current_theme['glow']};
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 30px {current_theme['primary']};
    }}
    
    .stRadio label {{
        color: {current_theme['text']};
        font-weight: 500;
    }}
    
    hr {{
        border-color: {current_theme['primary']};
        opacity: 0.3;
        margin: 1.5rem 0;
    }}
    
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.2);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {current_theme['primary']};
        border-radius: 5px;
        box-shadow: 0 0 10px {current_theme['primary']};
    }}
    
    .header-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: {current_theme['primary']};
        text-align: center;
        text-shadow: 0 0 20px {current_theme['primary']};
        animation: pulse 2s ease-in-out infinite;
        margin-bottom: 2rem;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    .status-dot {{
        height: 12px;
        width: 12px;
        background-color: {current_theme['primary']};
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 10px {current_theme['primary']};
        animation: pulse 1.5s ease-in-out infinite;
    }}
    
    .stChatInput {{
        background: {current_theme['card_bg']};
        border-radius: 25px;
        padding: 1rem;
        box-shadow: {current_theme['glow']};
        border: 2px solid {current_theme['primary']};
        backdrop-filter: blur(10px);
    }}
    
    .stChatInput textarea {{
        background: transparent;
        color: {current_theme['text']};
        border: none;
        font-size: 1rem;
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    /* Custom chat bubbles */
    .chat-container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }}
    
    .message-row {{
        display: flex;
        margin: 1rem 0;
        animation: slideIn 0.3s ease-out;
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .message-row.user {{
        justify-content: flex-end;
    }}
    
    .message-row.assistant {{
        justify-content: flex-start;
    }}
    
    .message-bubble {{
        max-width: 70%;
        padding: 1rem 1.3rem;
        border-radius: 18px;
        box-shadow: {current_theme['glow']};
        position: relative;
    }}
    
    .message-bubble.user {{
        background: {current_theme['user_bubble']};
        color: white;
        border-radius: 18px 18px 4px 18px;
        margin-left: 3rem;
    }}
    
    .message-bubble.assistant {{
        background: {current_theme['bot_bubble']};
        color: {current_theme['text']};
        border: 2px solid {current_theme['primary']};
        border-radius: 18px 18px 18px 4px;
        backdrop-filter: blur(10px);
        margin-right: 3rem;
    }}
    
    .message-content {{
        line-height: 1.6;
        margin: 0;
        word-wrap: break-word;
    }}
    
    .message-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        background: {current_theme['primary']};
        color: white;
        box-shadow: 0 0 10px {current_theme['primary']};
        flex-shrink: 0;
    }}
    
    .message-row.user .message-avatar {{
        margin-left: 0.75rem;
    }}
    
    .message-row.assistant .message-avatar {{
        margin-right: 0.75rem;
    }}
    
    .message-time {{
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 0.3rem;
        text-align: right;
    }}
    
    .message-row.assistant .message-time {{
        text-align: left;
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f'<h1>{bot_name}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p><span class="status-dot"></span>Online & Ready</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Key Management
    st.markdown("### 🔑 API Settings")
    if st.session_state.groq_api_key or GROQ_API_KEY:
        st.success("✅ API Key Active")
        if st.button("🔄 Change API Key", use_container_width=True):
            st.session_state.groq_api_key = ""
            st.rerun()
    else:
        api_key_input = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your free API key from https://console.groq.com"
        )
        if st.button("💾 Save Key", use_container_width=True):
            if api_key_input:
                st.session_state.groq_api_key = api_key_input
                st.success("✅ Saved!")
                st.rerun()
    
    st.markdown("---")
    
    # Theme selector
    st.markdown("### 🎨 Choose Your Vibe")
    theme_options = {
        "🌌 Cyberpunk": "cyberpunk",
        "🌈 Gradient Dream": "gradient",
        "💻 Retro Terminal": "terminal",
        "💬 Bubble Chat": "bubble",
        "📊 Professional": "professional"
    }
    
    selected_theme = st.radio(
        "Theme",
        options=list(theme_options.keys()),
        index=list(theme_options.values()).index(st.session_state.theme_style),
        label_visibility="collapsed"
    )
    
    if theme_options[selected_theme] != st.session_state.theme_style:
        st.session_state.theme_style = theme_options[selected_theme]
        st.rerun()
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", st.session_state.total_messages)
    with col2:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Your Msgs", user_msgs)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_messages = 0
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
        if st.session_state.messages:
            chat_export = "\n\n".join([
                f"{m['role'].upper()}: {m['content']}" 
                for m in st.session_state.messages
            ])
            st.download_button(
                "Download Chat",
                chat_export,
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Try different themes!
    - Export your conversations
    - Clear chat anytime
    - Stats update live
    """)

# Main chat area
if not st.session_state.messages:
    # Welcome screen
    st.markdown(f'<div class="header-title">{bot_name}</div>', unsafe_allow_html=True)
    
    st.markdown("###What can I help you with?")
    
    suggestions = [
        {"icon": "🧠", "title": "Explain Concepts", "desc": "Learn about complex topics"},
        {"icon": "💻", "title": "Code Solutions", "desc": "Get help with programming"},
        {"icon": "✍️", "title": "Creative Writing", "desc": "Generate stories and content"},
        {"icon": "📊", "title": "Data Analysis", "desc": "Analyze and visualize data"},
        {"icon": "🎨", "title": "Design Ideas", "desc": "Creative project concepts"},
        {"icon": "🔬", "title": "Research Help", "desc": "Dive deep into topics"}
    ]
    
    col1, col2, col3 = st.columns(3)
    
    for idx, suggestion in enumerate(suggestions):
        with [col1, col2, col3][idx % 3]:
            if st.button(
                f"{suggestion['icon']} {suggestion['title']}\n{suggestion['desc']}", 
                key=f"sug_{idx}",
                use_container_width=True
            ):
                prompt = f"Help me with: {suggestion['title']}"
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })
                response = get_response(prompt)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                st.session_state.total_messages += 2
                st.rerun()

else:
    # Display messages with custom HTML bubbles
    import html
    
    for message in st.session_state.messages:
        role = message["role"]
        content = html.escape(message["content"]).replace('\n', '<br>')
        avatar = "👤" if role == "user" else "🤖"
        
        if role == "user":
            chat_html = f'''
            <div class="message-row user">
                <div class="message-bubble user">
                    <div class="message-content">{content}</div>
                </div>
                <div class="message-avatar">{avatar}</div>
            </div>
            '''
        else:
            chat_html = f'''
            <div class="message-row assistant">
                <div class="message-avatar">{avatar}</div>
                <div class="message-bubble assistant">
                    <div class="message-content">{content}</div>
                </div>
            </div>
            '''
        
        st.markdown(chat_html, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input(f"Message {bot_name}..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    st.session_state.total_messages += 1
    
    # Get bot response
    response = get_response(prompt)
    
    # Add bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    st.session_state.total_messages += 1
    
    st.rerun()
