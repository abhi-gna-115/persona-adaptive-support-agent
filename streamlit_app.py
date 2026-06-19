import os
import json
import streamlit as st
from pypdf import PdfReader
from google import genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

API_KEY = "YOUR_API_KEY"
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

def chunk_documents(documents, chunk_size=500, overlap=100):
    chunks = []

    for doc in documents:
        text = doc["content"]

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "source": doc["source"],
                "content": chunk_text
            })

            start += chunk_size - overlap

    return chunks


@st.cache_resource
def build_vector_store(_documents):
    chunks = chunk_documents(_documents)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    chunk_texts = [chunk["content"] for chunk in chunks]
    embeddings = embedding_model.encode(chunk_texts)

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return embedding_model, index, chunks


embedding_model, vector_index, chunks = build_vector_store(documents)

def detect_persona_old(message):
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

def detect_persona(query):

    prompt = f"""
You are a customer support classifier.

Classify the user into exactly one of these categories:

1. Technical Expert
2. Frustrated User
3. Business Executive
4. General User

Definitions:

- Technical Expert:
Users asking technical questions about APIs, authentication, configurations, integrations, errors, debugging, or implementation details.

- Frustrated User:
Users expressing anger, frustration, dissatisfaction, urgency, or repeated failures.

- Business Executive:
Users asking about business impact, SLAs, costs, downtime, revenue, performance, or strategic concerns.

- General User:
All other normal customer queries.

User Query:
{query}

Return only the category name.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    persona = response.text.strip()

    allowed = [
        "Technical Expert",
        "Frustrated User",
        "Business Executive",
        "General User"
    ]

    if persona not in allowed:
        return "General User"

    return persona



def retrieve(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = vector_index.search(query_embedding, top_k)

    retrieved_chunks = []
    sources = []

    for idx in indices[0]:
        chunk = chunks[idx]
        retrieved_chunks.append(chunk["content"])
        sources.append(chunk["source"])

    combined_content = "\n\n".join(retrieved_chunks)

    best_doc = {
        "source": ", ".join(list(set(sources))),
        "content": combined_content
    }

    confidence_score = float(distances[0][0])

    return best_doc, confidence_score
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

    if score > 1.5:
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
                st.write("Vector Distance:", score)
            if escalate:
                handoff = generate_handoff_summary(user_query, persona, doc, score, reason)

                with st.expander("Internal Escalation Summary"):
                    st.json(handoff)