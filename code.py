import streamlit as st
from textblob import TextBlob
import time


# -------------------------------
# Questions
# -------------------------------
questions = {
    "Tell me about yourself.": ["skills", "education", "experience"],
    "Why should we hire you?": ["skills", "team", "contribute"],
    "What are your strengths?": ["strength", "hardworking", "problem-solving"],
    "Describe a challenge you faced.": ["challenge", "problem", "solution"]
}

# -------------------------------
# FUNCTIONS
# -------------------------------
def check_relevance(answer, keywords):
    match = sum(1 for word in keywords if word in answer.lower())
    return (match / len(keywords)) * 100

def check_confidence(answer):
    sentiment = TextBlob(answer).sentiment.polarity
    return (sentiment + 1) * 50

def grammar_check(answer):
    return str(TextBlob(answer).correct())

def generate_ai_feedback(score):
    if score > 75:
        return "Excellent structured answer with good confidence."
    elif score > 50:
        return "Decent answer, but improve clarity and add more details."
    else:
        return "Weak answer. Try adding examples and structured explanation."

# -------------------------------
# DARK MODE (Optional)
# -------------------------------
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# MENU
# -------------------------------
menu = st.sidebar.selectbox(
    "📂 Navigation",
    ["Home", "Practice Interview", "Results Dashboard" ,"Assistant"]
)

# -------------------------------
# SESSION
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# HOME PAGE
# -------------------------------
if menu == "Home":
    st.markdown("<h1 style='text-align:center;'>🎯 Smart Interview Analyzer PRO+</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:18px;'>Practice interviews with AI feedback, voice input, and performance analytics</p>", unsafe_allow_html=True)
    st.divider()

    # Key Features
    st.subheader("🚀 Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div style='text-align:center;'>🎤 Voice Practice</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Answer questions using your voice like real interviews.</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align:center;'> 🤖 AI Feedback</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Get instant smart feedback on your answers.</p>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='text-align:center;'> 📊 Performance Tracking</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Track your improvement with score analytics.</p>", unsafe_allow_html=True)

    st.divider()

# -------------------------------
#


    # How it works
    st.subheader("⚙️ How It Works")
    st.markdown("""
    1. Go to **Practice Interview**  
    2. Select a question  
    3. Answer using text or voice  
    4. Get instant AI feedback  
    5. Track your progress in Dashboard  
    """)
    st.divider()
    st.success("👉 Use the sidebar to start practicing interviews")

# -------------------------------
# PRACTICE INTERVIEW
# -------------------------------
elif menu == "Practice Interview":

    question = st.selectbox("Choose a question:", list(questions.keys()))

    # Timer
    if st.button("Start Timer (10 sec)"):
        progress = st.progress(0)
        for i in range(10):
            progress.progress((i + 1) * 10)
            time.sleep(1)

    
answer = st.text_area("Enter your answer:")
    # Analyze
    if st.button("Analyze Answer"):

        if answer.strip() == "":
            st.warning("Please enter your answer.")
        else :
            keywords = questions[question]

            relevance = check_relevance(answer, keywords)
            confidence = check_confidence(answer)
            corrected = grammar_check(answer)

            final_score = (relevance * 0.6) + (confidence * 0.4)

            st.session_state.history.append(final_score)

            # RESULTS
            st.subheader("📊 Result")
            col1, col2, col3 = st.columns(3)
            col1.metric("Final Score", round(final_score, 2))
            col2.metric("Relevance", round(relevance, 2))
            col3.metric("Confidence", round(confidence, 2))
            st.progress(int(final_score))

            # AI Feedback
            st.subheader("🤖 AI Feedback")
            st.info(generate_ai_feedback(final_score))

            # Grammar suggestion
            st.subheader("✍️ Improved Answer")
            st.write(corrected)

            # Download report
            report = f"""
Question: {question}
Score: {final_score}
Relevance: {relevance}
Confidence: {confidence}
"""
            st.download_button("📥 Download Report", report, file_name="report.txt")

# -------------------------------
# DASHBOARD
# -------------------------------
elif menu == "Results Dashboard":

    st.header("📊 Performance Dashboard")

    if len(st.session_state.history) > 0:
        st.line_chart(st.session_state.history)

        avg = sum(st.session_state.history) / len(st.session_state.history)
        best = max(st.session_state.history)

        st.metric("Average Score", round(avg, 2))
        st.metric("Best Score", round(best, 2))
    else:
        st.write("No data yet.")

elif menu == "Assistant":
    st.header("💬 Smart Assistant & Daily Vocabulary")

    # --- Chatbot Section ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You:", "")

    if st.button("Send"):
        if user_input.strip() != "":
            # Simple rule-based chatbot
            response = ""
            if "improve" in user_input.lower():
                response = "You can improve by practicing answers daily, reading, and noting keywords."
            elif "vocab" in user_input.lower():
                response = "Check the daily 10 words below and try using them in sentences."
            elif "gesture" in user_input.lower():
                response = "Maintain eye contact, smile naturally, and sit upright while speaking."
            else:
                response = "I can help you improve communication, vocabulary, and interview skills!"

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Assistant", response))

    # Display chat history
    for speaker, text in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Assistant:** {text}")

    st.divider()

    # --- Daily Vocabulary Section ---
    st.subheader("📝 Daily 10 Vocabulary Words")
    import random
    from datetime import date

    # Your vocab list
    all_vocab = ["Eloquent", "Concise", "Persuasive", "Analytical", "Collaborative",
                 "Proactive", "Adaptable", "Meticulous", "Resilient", "Empathetic",
                 "Assertive", "Innovative", "Strategic", "Dynamic", "Observant",
                 "Focused", "Diplomatic", "Organized", "Charismatic", "Resourceful",
                 "Tactful", "Curious", "Intuitive", "Versatile", "Patient",
                 "Decisive", "Energetic", "Optimistic", "Confident", "Responsible"]

    # Seed random by date so words rotate daily
    random.seed(date.today().toordinal())
    daily_vocab = random.sample(all_vocab, 10)

    cols = st.columns(5)
    for i, word in enumerate(daily_vocab):
        with cols[i % 5]:
            st.info(word)
