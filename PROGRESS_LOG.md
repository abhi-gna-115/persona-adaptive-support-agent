# Adsparkx AI Assignment - Progress Log

## Project
Persona-Adaptive Customer Support Agent using LLMs, RAG, and Human Escalation.

---

## Step 1: Understood Assignment
I reviewed the assignment requirements:
- Build an AI customer support agent.
- Detect customer persona.
- Retrieve information from support documents.
- Generate persona-based responses.
- Escalate to human support when needed.
- Provide handoff summary.

Status: Completed

---

## Step 2: Checked Python Environment
Initial Python version used:
- Python 3.9.13

Issue noticed:
- Some Google packages warned that Python 3.9 is no longer fully supported.

Correction:
- Continued using available Python setup temporarily because the deadline is short.

Status: Completed

---

## Step 3: Installed Gemini SDK
Tried using:
- google-generativeai

Issue noticed:
- Package gave deprecation warning.
- It recommended switching to google-genai.

Correction:
- Installed and switched to:
- google-genai

Status: Completed

---

## Step 4: Fixed Python Package Path Issue
Issue:
- google-genai was installed in D:\python
- But the script was running with Python from C:\Users\abhia\AppData\Local\Programs\Python\Python39

Correction:
- Ran the project using:
D:\python\python.exe app.py

Status: Completed

---

## Step 5: Fixed API Key Issues
Issues faced:
- API key expired error.
- Quota error for one Gemini model.
- Model high-demand error for gemini-2.5-flash.

Correction:
- Created a new Gemini API key.
- Switched Gemini model.
- Successfully tested with a working model.

Status: Completed

---

## Step 6: First Successful LLM Response
Test prompt:
"Say hello in one sentence"

Output received:
"Hello there!"

This confirmed:
- Python is working.
- Gemini API key is working.
- Gemini model call is working.
- The project can communicate with an LLM.

Status: Completed

---

## Current Working Command

D:\python\python.exe app.py

---

## Current Working Code Concept

The app connects to Gemini using the google-genai SDK and receives a generated response.

---

## Next Steps
- Install Streamlit, pypdf, FAISS, and sentence-transformers.
- Create knowledge base documents.
- Build document loading.
- Build retrieval logic.
- Add persona detection.
- Add adaptive response generation.
- Add escalation logic.
- Build Streamlit UI.
- Prepare README and demo video.
## Step 7: Knowledge Base Loading Completed

Created 11 support documents under the docs folder.

Documents loaded successfully:
- account_lock.txt
- api_authentication.txt
- billing_issue.txt
- data_export.txt
- login_troubleshooting.txt
- password_reset.txt
- refund_policy.txt
- security_policy.txt
- service_level_agreement.pdf
- subscription_upgrade.txt
- system_status.txt

Issue faced:
The first PDF file was not a real PDF because it was only renamed from text format.

Correction:
Created a proper PDF using Save As PDF.

Status:
Completed.

## Step 8: Retrieval System Implemented

Initial Approach:
- Used simple word matching.

Issue:
- Queries such as "How do I reset my password?" returned incorrect documents.
- Refund queries returned billing documents.

Root Cause:
- Generic word matching gave equal importance to common words.

Correction:
- Implemented domain-specific keyword boosting.
- Added keyword mappings for each support document.
- Combined keyword matching with content matching.

Examples:
Password query -> password_reset.txt
Refund query -> refund_policy.txt
API authentication query -> api_authentication.txt

Status:
Completed.
## Step 9: Package Verification Confusion

Objective:
Verify that required packages were installed successfully.

Packages:
- streamlit
- pypdf
- faiss-cpu
- sentence-transformers

Mistake:
Instead of checking installed packages, I typed:

streamlit
pypdf
faiss-cpu
sentence-transformers

directly into PowerShell.

Result:
- Streamlit executed and displayed its help menu.
- PowerShell attempted to execute pypdf, faiss-cpu, and sentence-transformers as commands.
- CommandNotFoundException errors were shown.

Realization:
Package names are not terminal commands.
Installed packages must be verified using:

python -m pip show package_name

or

python -m pip list

Correction:
Verified package installation correctly using pip.

Status:
Fixed.

Lesson Learned:
There is a difference between:
- Running a command
- Checking whether a package is installed
- Importing a package in Python

This helped improve understanding of Python package management.

## Step 10: Persona Detection Implemented

Objective:
Identify customer persona before generating responses.

Supported Personas:
- Technical Expert
- Frustrated User
- Business Executive

Implementation:
Used keyword-based classification.

Examples:
API, token, logs -> Technical Expert
Frustrated, nothing works -> Frustrated User
Business impact, revenue -> Business Executive

Status:
Completed

Future Improvement:
Replace keyword detection with Gemini-based classification.

## Step 11: End-to-End Persona Adaptive Agent Working

Implemented complete workflow:

User Query
→ Persona Detection
→ Document Retrieval
→ Gemini Response Generation

Test Cases:

1. Frustrated User
Query:
"I am frustrated. I tried everything and cannot reset my password."

Result:
- Persona: Frustrated User
- Source: password_reset.txt
- Response tone: empathetic

2. Technical Expert
Query:
"Can you explain the API authentication failure and token issue?"

Result:
- Persona: Technical Expert
- Source: api_authentication.txt
- Response tone: technical

3. Business Executive
Query:
"What is the business impact if system downtime exceeds SLA?"

Result:
- Persona: Business Executive
- Source: system_status.txt
- Response tone: business-focused

Status:
Completed.
User: I want a refund for duplicate charges.

Detected Persona: General User
Retrieved Source: billing_issue.txt
Retrieval Score: 7

Agent Response:
According to our billing support guide, situations involving duplicate charges and refund requests are to be escalated.

This issue may require assistance from a human support specialist.
Escalation Status: Required
Escalation Reason: Sensitive issue detected: refund

Human Handoff Summary:
{
    "persona": "General User",
    "issue": "I want a refund for duplicate charges.",
    "retrieved_document": "billing_issue.txt",
    "retrieval_score": 7,
    "escalation_reason": "Sensitive issue detected: refund",
    "attempted_action": "Retrieved relevant knowledge base content and generated support response",  
    "recommended_next_step": "Human support agent should review the case and contact the user."      
}

--------------------------------------------------

User: exit
PS D:\python\My-first-task> 
## Step 13: Escalation Response Improved

Improvement:
When escalation is required, the agent response now clearly informs the user that the issue may require assistance from a human support specialist.

Test Query:
"I want a refund for duplicate charges."

Result:
- Persona: General User
- Source: billing_issue.txt
- Escalation Status: Required
- Human handoff summary displayed in clean JSON format

Status:
Completed.

## Step 15: Streamlit UI Polishing and Design Decisions

After completing the basic Streamlit UI, tested the application in the browser.

### Issue 1: Greeting Message Handling

Test Query:
"hi"

Initial Result:
The app showed:
"No relevant document found. Escalation required."

Problem:
A greeting is not a support issue and should not trigger document retrieval or escalation.

Root Cause:
The system was sending every user message directly into the retrieval pipeline.
Since "hi" does not match any support document, retrieval failed.

Correction:
Added a greeting detection function.

Implemented:
- hi
- hello
- hey
- good morning
- good afternoon
- good evening

If a greeting is detected, the app responds with a welcome message and stops the pipeline using st.stop().

Lesson Learned:
Not every user input should go through the RAG pipeline. Some inputs like greetings should be handled separately before retrieval.

Status:
Completed.

---

## Step 16: Debugged st.stop() Indentation Issue

Issue:
After adding greeting handling, the app gave response only once and did not work properly for the next request.

Root Cause:
st.stop() was not placed with the correct indentation.

Correction:
Fixed indentation so st.stop() runs only for greeting messages and does not block normal support queries.

Status:
Completed.

---

## Step 17: Internal Handoff Summary Display Decision

Question Raised:
Why are we showing the human handoff summary to the customer?

Observation:
In a real production system, the customer should not see internal data such as:
- Retrieval score
- Escalation reason
- Retrieved document name
- Internal recommendation

Reason:
The handoff summary is meant for the human support agent, not the customer.

Assignment Decision:
For this assignment, the handoff summary is still displayed because it demonstrates that the required human handoff feature is implemented.

Improvement:
Changed the display from a normal visible section to a collapsible section.

Updated Label:
"Internal Escalation Summary"

Implementation:
Used Streamlit expander:

with st.expander("Internal Escalation Summary"):
    st.json(handoff)

Status:
Completed.

---

## Step 18: Discussed Rule-Based Logic vs LLM-Based Logic

Question Raised:
Since Gemini is already being used, why are keywords used for persona detection and greeting handling?

Understanding:
Gemini can classify personas and detect greetings, but each Gemini call costs tokens, increases latency, and adds more failure points.

Current Approach:
Used rule-based logic for:
- Persona detection
- Greeting detection
- Basic escalation checks

Reason:
This is faster, cheaper, easier to debug, and reliable for assignment submission.

Possible Future Improvement:
Replace separate rule-based functions with an LLM-based analyzer that returns structured output such as:

{
  "persona": "Frustrated User",
  "intent": "Password Reset",
  "is_greeting": false,
  "needs_escalation": false
}

Lesson Learned:
Good AI applications often combine deterministic code with LLM intelligence instead of using the LLM for everything.

Status:
Documented as future improvement.

---

## Step 19: UI Card Design Improvement

Issue:
The source file name was getting cut in the UI when shown using st.metric.
Example:
refund_policy.txt appeared as refund_poli...

Problem:
st.metric is not ideal for longer text values like file names.

Correction:
Replaced st.metric cards with custom HTML/CSS cards.

Improvements:
- Added rounded corners
- Reduced font size
- Added background color
- Allowed long file names to wrap properly
- Made the UI cleaner and more professional

Status:
Completed.

---

## Step 20: Retrieval Score Display Decision

Question Raised:
What does Retrieval Score mean and should it be shown to the user?

Understanding:
Retrieval Score is an internal confidence value calculated by the custom retrieval logic.
It increases when query keywords match document-specific keywords or document content.

Meaning:
Higher score means the retrieved document is more likely to be relevant to the user query.

Design Decision:
Retrieval Score is useful for debugging and evaluator review, but not useful for normal customers.

Correction:
Removed Retrieval Score from the main UI.
Moved it into an internal debug section.

Implementation:
Used Streamlit expander:

with st.expander("Internal Debug Information"):
    st.write("Retrieval Score:", score)

Status:
Completed.

---

## Current Application Status

Completed Features:
- Gemini API integration
- Knowledge base with 11 documents
- At least one PDF support document
- Document loading for TXT and PDF
- Persona detection
- Retrieval system
- Adaptive response generation
- Escalation logic
- Human handoff summary
- Streamlit web UI
- Greeting handling
- Internal debug section
- Internal escalation summary section
- UI polish using custom cards

Pending:
- README.md
- Architecture explanation
- Setup instructions
- Example queries
- Known limitations
- Demo video
- GitHub upload

## Step 21: Migration from Keyword-Based Retrieval to Vector-Based RAG

Objective:
Improve document retrieval accuracy by replacing keyword matching with semantic search.

Problem with Previous Approach:
The initial implementation used keyword-based matching, which failed when users expressed queries using different words than those present in the support documents.

Example:
User Query:
"How can I recover access to my account?"

The keyword-based system could fail to retrieve password reset documents because the exact keyword "password" might not appear in the query.

Solution:
Implemented a vector-based Retrieval Augmented Generation (RAG) pipeline.

Implementation Steps:

1. Loaded all support documents.
2. Split documents into fixed-size chunks with overlap.
3. Generated embeddings for each chunk using the SentenceTransformers model:
   all-MiniLM-L6-v2
4. Stored embeddings in a FAISS vector database.
5. Converted user queries into embeddings.
6. Retrieved top-k semantically similar chunks using vector similarity search.

Technologies Used:

* SentenceTransformers
* FAISS
* NumPy

Outcome:
The system can now retrieve relevant information even when the user's wording differs from the document content.

Status:
Completed.

---

## Step 22: Document Chunking Strategy

Objective:
Prepare large documents for efficient semantic retrieval.

Implementation:
Implemented fixed-size chunking with overlap.

Configuration:

* Chunk Size: 500 characters
* Overlap: 100 characters

Reason:
Chunking enables the system to retrieve only relevant portions of documents instead of passing entire documents to the LLM.

Benefits:

* Improved retrieval precision
* Reduced context size
* Better response quality

Status:
Completed.

---

## Step 23: Embedding Generation

Objective:
Convert document text into numerical vector representations.

Implementation:
Used SentenceTransformers embedding model:

all-MiniLM-L6-v2

Process:

* Generated embeddings for every document chunk.
* Converted embeddings to NumPy arrays.
* Stored embeddings for semantic similarity search.

Reason:
Embeddings capture semantic meaning instead of relying on exact keyword matches.

Status:
Completed.

---

## Step 24: FAISS Vector Database Integration

Objective:
Store and search document embeddings efficiently.

Implementation:
Integrated Facebook AI Similarity Search (FAISS).

Database Type:
IndexFlatL2

Workflow:

1. Store document embeddings.
2. Embed user query.
3. Perform nearest-neighbor search.
4. Retrieve top-k relevant chunks.

Reason:
FAISS provides fast and scalable similarity search for vector embeddings.

Status:
Completed.

---

## Step 25: LLM-Based Persona Detection

Objective:
Improve persona classification accuracy.

Previous Approach:
Rule-based persona detection using manually defined keywords.

Limitations:

* Limited flexibility.
* Could miss implicit user emotions or intent.

New Approach:
Used Gemini LLM to classify users into one of the following personas:

* Technical Expert
* Frustrated User
* Business Executive
* General User

Implementation:
A dedicated prompt is sent to Gemini requesting classification into exactly one supported persona.

Benefits:

* Better understanding of user intent.
* More adaptive responses.
* Reduced dependence on manually maintained keyword lists.

Status:
Completed.

---

## Step 26: Architecture and Documentation Enhancement

Completed:

* Updated README.md.
* Updated system architecture.
* Added architecture diagram.
* Updated technologies section.
* Updated installation instructions.
* Added requirements.txt.
* Added future improvements section.
* Added example queries.

Repository:
https://github.com/abhi-gna-115/persona-adaptive-support-agent

Status:
Completed.

---

## Final Project Architecture

User
↓
Streamlit User Interface
↓
Greeting Detection
↓
Gemini Persona Detection
↓
Document Loader
↓
Document Chunking
↓
Embedding Generation (all-MiniLM-L6-v2)
↓
FAISS Vector Database
↓
Top-K Semantic Retrieval
↓
Gemini Response Generation
↓
Escalation Logic
↓
Human Handoff Summary
↓
Final Response

Project Status:
Submission Ready.
