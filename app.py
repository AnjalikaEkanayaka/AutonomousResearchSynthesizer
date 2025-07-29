import streamlit as st
import os
from dotenv import load_dotenv
import requests

from utils.paper_search import search_arxiv
from utils.summarizer import summarize_paper_with_gemini, find_research_gap

# Load environment variables from .env file
load_dotenv()
# Read Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

#Setup Streamlit App Title
st.set_page_config(page_title="AI Research Helper", page_icon=":robot_face:")
st.title("Autonomous Research Synthesizer for Students")
st.markdown("Type your research topic and get a simple explanation powered by Gemini AI.")

#Text Input
topic = st.text_input("🔍 Enter your research topic here:")

#When button is clicked
if st.button("Explain My Topic") and topic:
    #Show Loading spinner
    with st.spinner("Thinking..."):
        #Send Request to Gemini
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "key": gemini_api_key
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Explain the research topic in simple, beginner-friendly terms: {topic}"
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            try:
                result = response.json()
                explanation = result['candidates'][0]['content']['parts'][0]['text']
                st.success(" Here’s your simplified explanation:")
                st.write(explanation)
            except Exception as e:
                st.error(f" Got response but couldn't extract text. Error: {e}")
                st.write(response.json())
        else:
            st.error(f" Gemini API request failed with status code {response.status_code}")
            st.write(response.text)

st.subheader(" Relevant Research Papers from ArXiv")

st.markdown("###  Optional Filters")

subject = st.selectbox(" Select subject area (optional)", options=["", "cs.AI", "cs.CV", "cs.LG", "cs.CL"])
year = st.selectbox(" Select publication year (optional)", options=[""] + [str(y) for y in range(2024, 2005, -1)])
num_papers = st.slider(" How many papers to retrieve?", min_value=3, max_value=20, value=5, step=1)

if st.button("Search Papers"):
    with st.spinner("Searching papers..."):
        papers = search_arxiv(topic, max_results=num_papers,
                              subject_filter=subject if subject else None,
                              year_filter=year if year else None)
        st.session_state["papers"] = papers
        st.session_state["topic"] = topic
        if len(papers) < num_papers:
            st.warning(f"Only {len(papers)} result(s) found for your filters. Try removing filters or increasing paper count.")

            st.info(f"Showing {len(papers)} result(s) for: *{topic}*")


if "papers" in st.session_state and st.session_state["papers"]:
    papers = st.session_state["papers"]
    topic = st.session_state["topic"]

    st.info(f"Showing {len(papers)} result(s) for: *{topic}*")

    for paper in papers:
        st.markdown(f"### 🔸 **{paper['title']}**", unsafe_allow_html=True)
        st.markdown(f"**Authors:** {paper['authors']}")
        st.markdown(f"**Summary:** {paper['summary']}")
        st.markdown(f"[Read Paper]({paper['link']})", unsafe_allow_html=True)
        st.markdown("---")

        with st.expander(" Gemini Summary (Method, Results, Conclusion)"):
            gemini_summary = summarize_paper_with_gemini(paper['title'], paper['summary'])
            st.markdown(gemini_summary)

    if st.button(" Analyze Common Research Gap Across These Papers"):
        with st.spinner("Asking Gemini to analyze gaps..."):
            gap_analysis = find_research_gap(papers)
            st.markdown("###  Common Research Gap Identified")
            st.markdown(gap_analysis)

