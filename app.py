import streamlit as st
import random
import time

# --- FRONTEND: Page Setup ---
st.set_page_config(page_title="RPS Grandmaster", page_icon="🏆", layout="wide")

# Expert-Level CSS with Level Glow and MASSIVE Gestures
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
        background-size: 400% 400%;
        animation: gradient 12s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-title {
        font-size: 60px !important;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .level-badge {
        text-align: center;
        padding: 10px;
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid #FFD700;
        border-radius: 50px;
        width: 250px;
        margin: 0 auto 30px auto;
        font-weight: bold;
        color: #FFD700;
    }
    /* MASSIVE GESTURE STYLE */
    .giant-emoji {
        font-size: 150px !important;
        text-align: center;
        display: block;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 6em;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        color: white;
        font-size: 22px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.5s;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 0 20px rgba(245, 87, 108, 0.6);
        transform: translateY(-10px);
    }
    /* Sidebar Reset Button fix */
    .stSidebar .stButton>button {
        height: 3em;
        font-size: 16px;
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid red;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND: Initialize ---
if 'user_score' not in st.session_state: st.session_state.user_score = 0
if 'cpu_score' not in st.session_state: st.session_state.cpu_score = 0
if 'history' not in st.session_state: st.session_state.history = []

# Rank Logic
wins = st.session_state.user_score
if wins < 3: rank = "🌱 NOVICE"
elif wins < 7: rank = "⚔️ WARRIOR"
elif wins < 12: rank = "🛡️ ELITE"
elif wins < 20: rank = "🔥 MASTER"
else: rank = "👑 GRANDMASTER"

st.markdown("<h1 class='main-title'>RPS GRANDMASTER</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='level-badge'>CURRENT RANK: {rank}</div>", unsafe_allow_html=True)

# --- SIDEBAR: Stats ---
with st.sidebar:
    st.markdown("## 📊 ARENA STATISTICS")
    st.divider()
    st.metric("YOUR WINS", st.session_state.user_score)
    st.metric("CPU WINS", st.session_state.cpu_score)
    st.progress(min(wins / 20, 1.0), text=f"Progress to Grandmaster")
    
    st.write("---")
    if st.button("🚨 FORFEIT & RESET"):
        st.session_state.user_score = 0
        st.session_state.cpu_score = 0
        st.session_state.history = []
        st.rerun()

# --- MAIN GAME ---
st.markdown("<h3 style='text-align: center;'>Deploy your move:</h3>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

options = ["Rock", "Paper", "Scissors"]
icons = {"Rock": "✊", "Paper": "✋", "Scissors": "✌️"}
user_choice = None

with c1:
    if st.button("✊\nROCK"): user_choice = "Rock"
with c2:
    if st.button("✋\nPAPER"): user_choice = "Paper"
with c3:
    if st.button("✌️\nSCISSORS"): user_choice = "Scissors"

if user_choice:
    computer_choice = random.choice(options)
    
    # Cinematic Delay
    with st.empty():
        for i in range(3, 0, -1):
            st.markdown(f"<h1 style='text-align: center;'>{i}...</h1>", unsafe_allow_html=True)
            time.sleep(0.3)
        st.empty()

    # MASSIVE Result Display
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown(f"<div class='giant-emoji'>{icons[user_choice]}</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>YOU</h3>", unsafe_allow_html=True)
    with res_col2:
        st.markdown(f"<div class='giant-emoji'>{icons[computer_choice]}</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>CPU</h3>", unsafe_allow_html=True)

    if user_choice == computer_choice:
        st.warning("🤝 A PERFECT STALEMATE!")
        result = "Draw"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #FFD700;'>✨ GLORIOUS VICTORY! ✨</h1>", unsafe_allow_html=True)
        st.session_state.user_score += 1
        result = "Win"
    else:
        st.error("💀 DEFEATED BY THE MACHINE!")
        st.session_state.cpu_score += 1
        result = "Loss"
    
    st.session_state.history.append(f"{result}: {icons[user_choice]} vs {icons[computer_choice]}")

# --- RECENT LOGS ---
if st.session_state.history:
    st.write("---")
    with st.expander("📜 VIEW BATTLE LOGS"):
        for entry in reversed(st.session_state.history[-10:]):
            st.write(entry)