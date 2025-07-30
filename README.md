# 🤖 Autonomous Research Synthesizer for Students

An AI-powered agentic web application that assists students with academic research by combining Gemini LLM, LangChain agents, ArXiv/Semantic Scholar search, and PDF understanding. It simplifies complex topics, finds and summarizes papers, analyzes research gaps, suggests methods, and chats with uploaded PDFs.

---

##  Key Features

###  AI Research Agent
- Built with **LangChain + Gemini**
- Supports **multi-turn memory**
- Can **search**, **summarize**, **analyze gaps**, **recommend methods**, and **read PDFs**
- Accepts open-ended queries like:  
  _“Find papers on transformers in NLP and suggest a good research methodology”_

###  Topic Explainer
- Simplifies research topics using Gemini
- Beginner-friendly explanations

###  Paper Search
- Searches papers using:
  -  ArXiv API 
  -  Semantic Scholar API 
- Summarizes papers (methodology, results, conclusion) using Gemini

### 🔬 Research Gap + Methodology
- Identifies gaps from summaries of multiple papers
- Suggests tools, methods, and techniques suitable for student research

###  PDF Chat Integration
- Upload your own research paper (PDF)
- LangChain reads + extracts text
- Ask questions about the paper using the same agent interface

---

##  Tech Stack

- **Frontend**: Streamlit
- **LLM**: Gemini 1.5 Flash (via Google Generative AI API)
- **Agent Framework**: LangChain (Conversational Agent with memory)
- **Search Tools**: ArXiv API, Semantic Scholar API
- **PDF Reader**: PyMuPDF
- **Language**: Python 3.10+

---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AutonomousResearchSynthesizer.git
cd AutonomousResearchSynthesizer
