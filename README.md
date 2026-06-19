# Persona-Adaptive Customer Support Agent

## Project Overview

The Persona-Adaptive Customer Support Agent is an AI-powered customer support system that provides intelligent, context-aware responses to customer queries. The system adapts its responses based on the detected user persona and retrieves relevant information from a knowledge base to generate accurate and personalized support responses.

The application is developed using Python, Streamlit, and Google's Gemini API.

---

## Features

### 1. Persona Detection

The system automatically identifies the user's persona based on the query.

Supported personas:

* Technical Expert
* Frustrated User
* Business Executive
* General User

---

### 2. Knowledge Base Retrieval

The system retrieves relevant information from a custom knowledge base containing support documents in TXT and PDF formats.

Supported document formats:

* TXT
* PDF

---

### 3. Adaptive Response Generation

Responses are generated using the Gemini Large Language Model and adapted according to the detected user persona.

Examples:

* Technical users receive detailed technical explanations.
* Frustrated users receive empathetic responses.
* Business executives receive concise business-oriented responses.

---

### 4. Escalation Logic

The system automatically identifies situations requiring human intervention.

Examples:

* Refund requests
* Billing disputes
* Security breaches
* Unauthorized access issues
* Low retrieval confidence

---

### 5. Human Handoff Summary

When escalation is required, the system generates an internal handoff summary containing:

* User persona
* User issue
* Retrieved document
* Escalation reason
* Recommended next steps

---

### 6. Greeting Handling

The system handles greetings such as:

* Hi
* Hello
* Hey
* Good Morning
* Good Evening

without invoking the retrieval pipeline.

---

## System Architecture

```text
User
   ↓
Streamlit User Interface
   ↓
Greeting Detection
   ↓
Persona Detection
   ↓
Document Retrieval Engine
   ↓
Gemini API
   ↓
Adaptive Response Generation
   ↓
Escalation Logic
   ↓
Human Handoff Summary
```

---

## Project Structure

```text
My-first-task/
│
├── docs/
│   ├── account_lock.txt
│   ├── api_authentication.txt
│   ├── billing_issue.txt
│   ├── data_export.txt
│   ├── login_troubleshooting.txt
│   ├── password_reset.txt
│   ├── refund_policy.txt
│   ├── security_policy.txt
│   ├── service_level_agreement.pdf
│   ├── subscription_upgrade.txt
│   └── system_status.txt
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── PROGRESS_LOG.md
```

---

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* PyPDF
* HTML/CSS
* Large Language Models (LLMs)

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd My-first-task
```

### Install Dependencies

```bash
pip install streamlit
pip install google-genai
pip install pypdf
```

---

## Configure Gemini API Key

Replace the API key inside:

```python
streamlit_app.py
```

with your own Gemini API key.

Example:

```python
API_KEY = "YOUR_API_KEY"
```

---

## Running the Application

```bash
streamlit run streamlit_app.py
```

---

## Example Queries

### Greeting

```text
Hi
```

### Technical Query

```text
Can you explain API authentication failure and token issues?
```

### Frustrated User Query

```text
I am frustrated. I cannot reset my password.
```

### Business Query

```text
What is the business impact if system downtime exceeds SLA?
```

### Escalation Query

```text
I want a refund for duplicate charges.
```

---

## Future Improvements

* Integrate vector databases such as FAISS or ChromaDB.
* Replace keyword-based retrieval with embedding-based retrieval.
* Implement LLM-based persona detection.
* Add user feedback collection.
* Integrate ticketing systems for automated escalation.
* Add conversation memory.

---

## Author

Developed by sai Abhinay as part of an AI Support Agent assignment.
