import streamlit as st
import os
import requests
import tempfile
from dotenv import load_dotenv

from agent import agent
from utils.paper_search import search_arxiv
from utils.summarizer import (
    summarize_paper_with_gemini,
    find_research_gap,
    suggest_methodology_based_on_gap
)

# ========== SETUP ==========
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup Streamlit App Title
st.set_page_config(page_title="AI Research Helper", page_icon="🤖")
st.title("🎓 Autonomous Research Synthesizer for Students")
st.markdown("Use Gemini AI to understand topics, find papers, and get research insights.")

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📘 Topic Explainer", "📄 Paper Finder", "🔍 Gap & Methodology", "🧠 Research Agent", "📄 Upload PDF"])

# ========== TAB 1: Topic Explainer ==========
with tab1:
    st.header("🔍 Understand Your Research Topic")
    topic = st.text_input("Enter your research topic:")

    if st.button("Explain My Topic"):
        if topic:
            with st.spinner("Gemini is thinking..."):
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                headers = {"Content-Type": "application/json"}
                params = {"key": gemini_api_key}
                data = {
                    "contents": [
                        {"parts": [{"text": f"Explain the research topic in simple, beginner-friendly terms: {topic}"}]}
                    ]
                }

                response = requests.post(url, headers=headers, params=params, json=data)
                if response.status_code == 200:
                    try:
                        result = response.json()
                        explanation = result['candidates'][0]['content']['parts'][0]['text']
                        st.success("Simplified Explanation:")
                        st.markdown(explanation)
                    except Exception as e:
                        st.error("Failed to parse Gemini response.")
                        st.write(response.json())
                else:
                    st.error(f"Gemini API failed ({response.status_code})")
        else:
            st.warning("Please enter a topic first.")

# ========== TAB 2: Paper Search ==========
with tab2:
    st.header("📄 Search Relevant Research Papers")
    source = st.selectbox("Paper source:", ["ArXiv", "Semantic Scholar"])
    with st.form("search_form"):
        topic = st.text_input("Topic for paper search:")
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Subject area (optional):", ["", "cs.AI", "cs.CV", "cs.LG", "cs.CL"])
        with col2:
            year = st.selectbox("Year (optional):", [""] + [str(y) for y in range(2024, 2005, -1)])
        num_papers = st.slider("How many papers to retrieve?", 3, 20, 5)
        submitted = st.form_submit_button("🔎 Search Papers")

    if submitted and topic:
        with st.spinner("Searching {source}..."):
            if source == "ArXiv":
                papers = search_arxiv(
                    topic, max_results=num_papers,
                    subject_filter=subject or None,
                    year_filter=year or None
                )
            else:
                from utils.semantic_scholar import search_semantic_scholar
                papers = search_semantic_scholar(topic, limit=num_papers)

            st.session_state["papers"] = papers
            st.session_state["topic"] = topic

    if "papers" in st.session_state and st.session_state["papers"]:
        st.success(f"Showing {len(st.session_state['papers'])} result(s) for: *{st.session_state['topic']}*")
        for paper in st.session_state["papers"]:
            st.markdown(f"### 🔸 **{paper['title']}**", unsafe_allow_html=True)
            st.markdown(f"**Authors:** {paper['authors']}")
            st.markdown(f"**Summary:** {paper['summary']}")
            st.markdown(f"[Read Paper]({paper['link']})", unsafe_allow_html=True)

            with st.expander("Gemini Summary (Method, Results, Conclusion)"):
                gemini_summary = summarize_paper_with_gemini(paper['title'], paper['summary'])
                st.markdown(gemini_summary)
            st.markdown("---")

# ========== TAB 3: Gap Analysis + Methodology ==========
with tab3:
    st.header("🔍 Analyze Research Gaps + Get Methodology Suggestions")

    if "papers" in st.session_state and st.session_state["papers"]:
        if st.button(" Analyze Common Research Gap"):
            with st.spinner("Gemini analyzing gap..."):
                gap_analysis = find_research_gap(st.session_state["papers"])
                st.markdown("###  Identified Research Gap")
                st.markdown(gap_analysis)
                st.session_state["gap_analysis"] = gap_analysis

        if "gap_analysis" in st.session_state:
            if st.button(" Suggest Methodology & Tools"):
                with st.spinner("Gemini generating suggestions..."):
                    method_suggestion = suggest_methodology_based_on_gap(
                        st.session_state["topic"],
                        st.session_state["gap_analysis"]
                    )
                    st.markdown("### 🛠 Recommended Methods and Tools")
                    st.markdown(method_suggestion)
    else:
        st.info("⚠️ Please search papers in the 'Paper Finder' tab first.")

# ========== TAB 4: LANGCHAIN AGENT SECTION ==========
with tab4:
    st.header("🧠 Chat with Research Agent")

    query = st.text_input("Ask your research assistant:", placeholder="e.g., 'Find papers on LLMs and suggest methodology'")

    if st.button("Run Agent") and query:
        with st.spinner("Thinking..."):
            response = agent.run(query)
            st.success("Agent Response:")
            st.markdown(response)


# ========== TAB 5:AGENTIC AI TAB ==========

with tab5:
    
    st.header("📎 Upload PDF for Gemini Agent to Read")

    st.warning("For best results, upload short or relevant excerpts from your PDF (max 5–10 pages recommended).")

    uploaded_pdf = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])

    if uploaded_pdf is not None:
        # Save to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            temp_pdf_path = tmp_file.name
        st.success(" PDF uploaded successfully.")

        # Let user now query about it
        user_query = st.text_input("Ask something about the uploaded PDF (e.g., 'Summarize methods')")

        if st.button("Run Agent on PDF") and user_query:
            with st.spinner("Agent is analyzing..."):
                # Add the PDF path into the query if needed
                full_query = f"{user_query}. The PDF is located at: {temp_pdf_path}"
                response = agent.run(full_query)
                st.markdown("### 🤖 Agent Response")
                st.markdown(response)
