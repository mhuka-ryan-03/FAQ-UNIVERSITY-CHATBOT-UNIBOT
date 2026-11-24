
import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UniBot - University FAQ",
    page_icon="🎓",
    layout="centered"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #eef2f7;
}

/* Main heading */
.title {
    text-align: center;
    color: #183153 !important;
    font-size: 38px;
    font-weight: bold;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #475569 !important;
    font-size: 16px;
}

/* Chat message cards */
.stChatMessage {
    background-color: #ffffff !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 14px !important;
    padding: 15px !important;
    margin-bottom: 12px !important;
}

/* Chat text */
.stChatMessage p,
.stChatMessage span,
.stChatMessage li {
    color: #1e293b !important;
    font-size: 16px !important;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #e2e8f0 !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #183153 !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {
    color: #1e293b !important;
}

/* Main headings */
h1, h2, h3 {
    color: #183153 !important;
}

/* Information box */
.stAlert {
    background-color: #dbeafe !important;
}

/* Bottom chat area */
div[data-testid="stBottom"] {
    background-color: #eef2f7 !important;
}

div[data-testid="stBottomBlockContainer"] {
    background-color: #eef2f7 !important;
}

/* Chat input */
.stChatInput,
[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
}

.stChatInput textarea {
    color: #1e293b !important;
    background-color: #ffffff !important;
}

/* Placeholder */
.stChatInput textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Top header */
header[data-testid="stHeader"] {
    background-color: #eef2f7 !important;
}

/* Buttons */
.stButton button {
    border-radius: 9px;
    border: 1px solid #cbd5e1;
    color: #183153;
}

.stButton button:hover {
    border-color: #2563eb;
    color: #2563eb;
}

</style>
""", unsafe_allow_html=True)


# ---------------- KNOWLEDGE BASE ----------------
faq_data = {

    "admission": {
        "keywords": [
            "admission", "apply", "application",
            "enroll", "enrollment", "entry"
        ],
        "answer": (
            "Students can apply for admission by submitting "
            "an application form and the required academic "
            "documents to the university admissions office."
        )
    },

    "fees": {
        "keywords": [
            "fee", "fees", "tuition", "payment", "pay", "cost"
        ],
        "answer": (
            "Tuition fees vary depending on the programme. "
            "Please contact the university finance office "
            "for the latest fee structure and payment information."
        )
    },

    "examinations": {
        "keywords": [
            "exam", "exams", "examination", "test",
            "semester", "timetable"
        ],
        "answer": (
            "Examination dates and timetables are normally "
            "communicated through the university academic "
            "portal and notice boards."
        )
    },

    "library": {
        "keywords": [
            "library", "book", "books", "reading", "study"
        ],
        "answer": (
            "The university library provides students with "
            "books, study spaces and academic learning resources."
        )
    },

    "courses": {
        "keywords": [
            "course", "courses", "programme", "program",
            "degree", "study"
        ],
        "answer": (
            "The university offers various undergraduate and "
            "postgraduate programmes across different academic "
            "departments. Please visit the admissions office "
            "for the full list."
        )
    },

    "hostel": {
        "keywords": [
            "hostel", "accommodation", "room",
            "housing", "residence"
        ],
        "answer": (
            "Students interested in university accommodation "
            "should contact the hostel or student affairs "
            "office to check availability and application procedures."
        )
    },

    "location": {
        "keywords": [
            "location", "located", "address",
            "campus", "directions"
        ],
        "answer": (
            "The university is located on its main campus. "
            "Please check the official university website "
            "for the exact address and directions."
        )
    },

    "contact": {
        "keywords": [
            "contact", "phone", "email",
            "number", "office", "help"
        ],
        "answer": (
            "You can contact the university administration "
            "or relevant department through the official "
            "university website."
        )
    },

    "attendance": {
        "keywords": [
            "attendance", "absent", "absence",
            "classes", "class"
        ],
        "answer": (
            "Students are expected to attend their scheduled "
            "classes and comply with the university attendance "
            "requirements."
        )
    },

    "results": {
        "keywords": [
            "result", "results", "grades",
            "marks", "score", "cgpa"
        ],
        "answer": (
            "Examination results are generally released "
            "through the student portal after the university "
            "completes the assessment process."
        )
    },

    "scholarships": {
        "keywords": [
            "scholarship", "scholarships",
            "financial", "aid", "funding"
        ],
        "answer": (
            "Students can contact the scholarships or student "
            "affairs office to learn about available scholarships, "
            "eligibility criteria and application deadlines."
        )
    },

    "wifi": {
        "keywords": [
            "wifi", "wi-fi", "internet", "network"
        ],
        "answer": (
            "Students can contact the university IT support "
            "department for campus Wi-Fi access and assistance "
            "with connectivity issues."
        )
    }
}


# ---------------- CHATBOT LOGIC ----------------
def get_response(user_question):

    question = user_question.lower().strip()
    question = re.sub(r"[^a-zA-Z\s]", "", question)

    words = question.split()

    # Greetings
    greetings = [
        "hello", "hi", "hey",
        "good morning", "good afternoon"
    ]

    if question in greetings or question.startswith(
        ("hello ", "hi ", "hey ")
    ):
        return (
            "Hello! 👋 Welcome to UniBot. "
            "I'm here to answer your university-related "
            "questions. How can I help you?"
        )

    # Goodbye
    if any(word in ["bye", "goodbye", "exit"] for word in words):
        return (
            "Goodbye! 👋 Have a great day "
            "and good luck with your studies!"
        )

    # Thank you
    if any(word in ["thank", "thanks"] for word in words):
        return (
            "You're welcome! 😊 Feel free to ask me "
            "any other university-related questions."
        )

    # Find best keyword match
    best_category = None
    best_score = 0

    for category, data in faq_data.items():

        score = 0

        for keyword in data["keywords"]:

            if keyword in words:
                score += 1

        if score > best_score:
            best_score = score
            best_category = category

    # Return matching answer
    if best_category is not None:
        return faq_data[best_category]["answer"]

    # Fallback response
    return (
        "I'm sorry, I don't have information about that "
        "question yet. Please try asking about admissions, "
        "fees, examinations, courses, library, hostel, "
        "attendance, results, scholarships or Wi-Fi."
    )


# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">🎓 UniBot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'University Frequently Asked Questions Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("🤖 About UniBot")

    st.write(
        "UniBot is a simple chatbot designed to help "
        "students find answers to common university questions."
    )

    st.divider()

    st.subheader("Topics I can answer")

    topics = [
        "Admissions",
        "Tuition Fees",
        "Examinations",
        "Courses",
        "Library",
        "Hostel",
        "Attendance",
        "Results",
        "Scholarships",
        "Wi-Fi"
    ]

    for topic in topics:
        st.write(f"• {topic}")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- WELCOME MESSAGE ----------------
if len(st.session_state.messages) == 0:

    st.info(
        "👋 Hello! I'm UniBot. Ask me anything about "
        "university services, admissions, fees or academics."
    )

    st.subheader("Try asking:")

    sample_questions = [
        "How do I apply for admission?",
        "How much are tuition fees?",
        "When are examinations?",
        "Where is the library?",
        "How can I get Wi-Fi?"
    ]

    for question in sample_questions:

        if st.button(question, use_container_width=True):

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            response = get_response(question)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()


# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask a university question...")

if user_input:

    # Store user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate chatbot response
    response = get_response(user_input)

    # Store chatbot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
