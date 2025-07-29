import streamlit as st
import os
from dotenv import load_dotenv
import requests

from utils.paper_search import search_arxiv
from utils.summarizer import (
    summarize_paper_with_gemini,
    find_research_gap,
    suggest_methodology_based_on_gap
)

# ========== SETUP ==========
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Research Synthesizer", layout="wide", page_icon=":robot_face:")
st.title("🤖 Autonomous Research Synthesizer for Students")

# ========== SIDEBAR FILTERS ==========
with st.sidebar:
    st.header(" Paper Filters")
    subject = st.selectbox(" Subject Area", ["", "cs.AI", "cs.CV", "cs.LG", "cs.CL"])
    year = st.selectbox(" Publication Year", [""] + [str(y) for y in range(2024, 2005, -1)])
    num_papers = st.slider(" Number of Papers", 3, 20, 5)

# ========== TABS ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Topic Clarifier",
    "2️⃣ Search Papers",
    "3️⃣ Gap Analysis",
    "4️⃣ Methodology Suggestion"
])

# ========== TAB 1: TOPIC CLARIFICATION ==========
with tab1:
    st.subheader("🔍 Enter Your Research Topic")
    topic = st.text_input("Enter your topic:")
    
    if st.button(" Explain My Topic"):
        with st.spinner("Gemini is thinking..."):
            url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
            headers = {"Content-Type": "application/json"}
            params = {"key": gemini_api_key}
            data = {
                "contents": [
                    {"parts": [{"text": f"Explain the research topic in simple, beginner-friendly terms: {topic}"}]}
                ]
            }

            response = requests.post(url, headers=headers, params=params, json=data)
            if response.status_code == 200:
                explanation = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.success(" Simplified Explanation:")
                st.markdown(explanation)
            else:
                st.error(f" Gemini API failed ({response.status_code})")

# ========== TAB 2: PAPER SEARCH ==========
with tab2:
    st.subheader(" Relevant Papers from ArXiv")
    
    if st.button("🔎 Search Papers"):
        with st.spinner("Searching ArXiv..."):
            papers = search_arxiv(
                topic,
                max_results=num_papers,
                subject_filter=subject if subject else None,
                year_filter=year if year else None
            )
            st.session_state["papers"] = papers
            st.session_state["topic"] = topic

    if "papers" in st.session_state and st.session_state["papers"]:
        st.success(f"Showing {len(st.session_state['papers'])} result(s) for: *{st.session_state['topic']}*")

        for paper in st.session_state["papers"]:
            st.markdown(f"### 🔸 **{paper['title']}**", unsafe_allow_html=True)
            st.markdown(f"**Authors:** {paper['authors']}")
            st.markdown(f"**Summary:** {paper['summary']}")
            st.markdown(f"[Read Paper]({paper['link']})", unsafe_allow_html=True)

            with st.expander(" Gemini Summary (Method, Results, Conclusion)"):
                summary = summarize_paper_with_gemini(paper['title'], paper['summary'])
                st.markdown(summary)

            st.markdown("---")

# ========== TAB 3: GAP ANALYSIS ==========
with tab3:
    st.subheader(" Common Research Gap")

    if "papers" in st.session_state and st.session_state["papers"]:
        if st.button(" Analyze Research Gap"):
            with st.spinner("Analyzing research gaps..."):
                gap = find_research_gap(st.session_state["papers"])
                st.session_state["gap"] = gap
                st.markdown("### 🔍 Gap Identified")
                st.markdown(gap)
    else:
        st.info(" Please search for papers in Tab 2 first.")

# ========== TAB 4: METHODOLOGY SUGGESTION ==========
with tab4:
    st.subheader("🛠️ Recommended Methodology and Tools")

    if "gap" in st.session_state:
        if st.button(" Suggest Methodology Based on Gap"):
            with st.spinner("Generating suggestions..."):
                suggestion = suggest_methodology_based_on_gap(
                    st.session_state["topic"],
                    st.session_state["gap"]
                )
                st.markdown(suggestion)
    else:
        st.info(" Please analyze a gap in Tab 3 first.")
