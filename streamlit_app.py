import os
import json
import streamlit as st
from pypdf import PdfReader
from google import genai

API_KEY = "YOUR_GEMINI_API_KEY"
DOCS_FOLDER = "docs"

client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Persona-Adaptive Support Agent", page_icon="🤖")

st.title("🤖 Persona-Adaptive Customer Support Agent")
st.write("LLM-powered support assistant with persona detection, retrieval, adaptive response, and escalation.")
with st.sidebar:
    st.header("Project Information")
    st.write("Persona-Adaptive Customer Support Agent")
    st.write("Powered by Gemini AI")
    st.write("Features:")
    st.write("✅ Persona Detection")
    st.write("✅ Document Retrieval")
    st.write("✅ Adaptive Responses")
    st.write("✅ Escalation Logic")
    st.write("✅ Human Handoff Summary")
documents = []


def load_documents():
    docs = []

    for file in os.listdir(DOCS_FOLDER):
        path = os.path.join(DOCS_FOLDER, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"source": file, "content": text})

        elif file.endswith(".pdf"):
            reader = PdfReader(path)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            docs.append({"source": file, "content": text})

    return docs


documents = load_documents()


def detect_persona(message):
    text = message.lower()

    technical_keywords = ["api", "authentication", "token", "configuration", "logs", "error", "endpoint", "debug", "server"]
    frustrated_keywords = ["angry", "frustrated", "nothing works", "terrible", "hate", "worst", "urgent", "annoyed", "fed up"]
    business_keywords = ["business", "operations", "impact", "revenue", "customer", "timeline", "executive", "resolution"]

    for word in technical_keywords:
        if word in text:
            return "Technical Expert"

    for word in frustrated_keywords:
        if word in text:
            return "Frustrated User"

    for word in business_keywords:
        if word in text:
            return "Business Executive"

    return "General User"


def retrieve(query):
    query = query.lower()

    keyword_map = {
        "password_reset.txt": ["password", "reset", "forgot password", "reset link"],
        "account_lock.txt": ["account locked", "locked", "lock", "failed login"],
        "refund_policy.txt": ["refund", "money back", "cancel refund"],
        "billing_issue.txt": ["billing", "payment", "invoice", "duplicate charge", "charged"],
        "api_authentication.txt": ["api", "authentication", "token", "authorization", "api key"],
        "login_troubleshooting.txt": ["login", "log in", "browser", "cache", "cookies"],
        "subscription_upgrade.txt": ["upgrade", "subscription", "plan", "premium"],
        "data_export.txt": ["export", "csv", "excel", "json", "data"],
        "security_policy.txt": ["security", "unauthorized", "breach", "mfa", "multi-factor"],
        "system_status.txt": ["downtime", "maintenance", "status", "slow", "unavailable"],
        "service_level_agreement.pdf": ["sla", "response time", "uptime", "critical issue"]
    }

    best_doc = None
    best_score = 0

    for doc in documents:
        filename = doc["source"]
        content = doc["content"].lower()
        score = 0

        for keyword in keyword_map.get(filename, []):
            if keyword in query:
                score += 5

        for word in query.split():
            if len(word) > 3 and word in content:
                score += 1

        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc, best_score


def should_escalate(user_query, score):
    text = user_query.lower()

    sensitive_keywords = [
        "refund", "legal", "lawsuit", "billing dispute",
        "unauthorized", "breach", "hacked", "account compromise",
        "duplicate charge", "payment failed"
    ]

    if score < 3:
        return True, "Low retrieval confidence"

    for keyword in sensitive_keywords:
        if keyword in text:
            return True, f"Sensitive issue detected: {keyword}"

    return False, "No escalation required"


def generate_handoff_summary(user_query, persona, doc, score, reason):
    return {
        "persona": persona,
        "issue": user_query,
        "retrieved_document": doc["source"] if doc else "None",
        "retrieval_score": score,
        "escalation_reason": reason,
        "attempted_action": "Retrieved relevant knowledge base content and generated support response",
        "recommended_next_step": "Human support agent should review the case and contact the user."
    }

def is_greeting(text):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    return text.lower().strip() in greetings
def generate_response(user_query, persona, retrieved_doc, escalate):
    escalation_note = ""

    if escalate:
        escalation_note = "Also mention that this issue may require assistance from a human support specialist."

    prompt = f"""
You are a persona-adaptive customer support agent.

Detected Persona: {persona}

User Query:
{user_query}

Retrieved Knowledge Base Content:
{retrieved_doc["content"]}

Instructions:
- Answer only using the retrieved knowledge base content.
- Do not make up information.
- Mention practical steps clearly.
- If persona is Technical Expert, give technical and detailed explanation.
- If persona is Frustrated User, be empathetic, simple, and reassuring.
- If persona is Business Executive, be concise and impact-focused.
- Keep the answer helpful and professional.
{escalation_note}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


user_query = st.text_area("Enter customer message:")

if st.button("Generate Response"):
    if is_greeting(user_query):

        st.success(
            "Hello! How can I help you today?\n\n"
            "I can assist with password resets, billing issues, "
            "API authentication, subscriptions, security questions, "
            "and more."
        )

        st.stop()
    if user_query.strip() == "":
        st.warning("Please enter a customer message.")
    else:
        persona = detect_persona(user_query)
        doc, score = retrieve(user_query)

        if doc is None:
            st.error("No relevant document found. Escalation required.")
        else:
            escalate, reason = should_escalate(user_query, score)
            answer = generate_response(user_query, persona, doc, escalate)

            st.markdown("""
            <style>
            .info-card {
                background-color: #1e1e2f;
                padding: 14px 16px;
                border-radius: 12px;
                border: 1px solid #34344a;
                min-height: 88px;
            }
            .info-label {
                font-size: 13px;
                color: #b8b8c7;
                margin-bottom: 6px;
            }
            .info-value {
                font-size: 18px;
                font-weight: 600;
                color: #ffffff;
                word-break: break-word;
            }
            </style>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="info-label">Persona</div>
                        <div class="info-value">{persona}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="info-label">Retrieved Source</div>
                        <div class="info-value">{doc["source"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.subheader("Agent Response")
            st.write(answer)

            st.subheader("Escalation Status")
            if escalate:
                st.error("Required")
            else:
                st.success("Not Required")

            st.write("Reason:", reason)
            with st.expander("Internal Debug Information"):
                st.write("Retrieval Score:", score)
            if escalate:
                handoff = generate_handoff_summary(user_query, persona, doc, score, reason)

                with st.expander("Internal Escalation Summary"):
                    st.json(handoff)