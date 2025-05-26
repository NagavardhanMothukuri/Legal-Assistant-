# Legal-Assistant-
I with my fellow classmate have worked on the project regarding the llama 2 7b model ,how accurately the model works on particular field rather than all fields unlike chatgpt,GPT 


Install all the reuirements from the requirements.txt 

Since its on Flask can run through direct commands like python run.py 


🧠 AI-Powered Legal Assistant (RAG-based)
The AI-Powered Legal Assistant is a sophisticated legal question-answering system designed to provide users with accurate, context-aware responses based on Indian legal documents and statutes. This project leverages Retrieval-Augmented Generation (RAG) using LLaMA2-7B, vector similarity search with ChromaDB, and Neo4j for graph-based legal knowledge representation.

🚀 Project Goals
Assist users with legal queries using a conversational AI.

Extract and understand legal content from large PDFs and court judgments.

Provide reliable responses by combining vector embeddings and graph reasoning.

Make Indian legal resources more accessible through natural language queries.

🧰 Tech Stack
LLM: LLaMA2-7B (Fine-tuned on Indian legal datasets like FALQU, LawyerChat, JEC-QA)

Vector DB: ChromaDB (for semantic retrieval of context)

Graph DB: Neo4j (to represent legal entities, relations, precedents)

Backend: Python (Flask or FastAPI)

Embedding Model: all-MiniLM-L6-v2 / custom legal embeddings

File Handling: PyMuPDF / PDFMiner for text extraction

Frontend (optional): React.js or HTML/CSS/JS interface


🔍 Features
📄 PDF Text Extraction: Upload court rulings or law documents for context-aware analysis.

🔎 RAG Pipeline: Combines semantic search and graph reasoning for precise answers.

🧠 Fine-tuned Legal LLM: Uses a custom-trained LLaMA2-7B model for legal contexts.

🌐 Neo4j Graph Search: Models relationships between laws, cases, and entities.

📚 Hybrid Retrieval: Uses both vector similarity and knowledge graph reasoning.

🗣️ Conversational Interface: Interact with the assistant using natural language.


🧠 Architecture Overview
User Query
   ↓
Vector Embedding + Graph Search
   ↓
Relevant Context + Entity Relations
   ↓
RAG-based Prompt Construction
   ↓
LLaMA2-7B Response Generation
   ↓
Answer Returned to User



📦 Datasets Used
[✔️] FALQU – FAQs and legal questions

[✔️] LawyerChat – Lawyer-customer conversations

[✔️] JEC-QA – Indian judicial Q&A

[✔️] Indian Penal Code, CRPC, Civil Laws (PDFs)

✅ Use Cases
Help users understand their legal rights and obligations.

Provide assistance in drafting legal documents.

Guide individuals through basic legal procedures (e.g., filing FIRs, divorce, tenant rights).

Assist paralegals and junior lawyers with legal research.

📌 Future Improvements
Add multilingual support for regional Indian languages.

Integrate document summarization for uploaded judgments.

Add real-time lawyer consultation feature.

Deploy the assistant via chatbot or WhatsApp interface.

