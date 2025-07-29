from langchain.tools import tool
from utils.paper_search import search_arxiv
from utils.summarizer import (
    summarize_paper_with_gemini,
    find_research_gap,
    suggest_methodology_based_on_gap
)

@tool
def paper_search_tool(topic: str) -> str:
    """Search for 5 recent relevant papers on a topic from ArXiv."""
    results = search_arxiv(topic, max_results=5)
    return "\n\n".join([f"Title: {p['title']}\nAuthors: {p['authors']}\nSummary: {p['summary']}" for p in results])

@tool
def summarize_tool(title_and_summary: str) -> str:
    """Summarize a paper’s methods and results given title + summary."""
    return summarize_paper_with_gemini("temp_title", title_and_summary)

@tool
def gap_analysis_tool(papers_text: str) -> str:
    """Analyze a common research gap from a list of paper summaries."""
    fake_paper_list = [{"title": "", "summary": p} for p in papers_text.split("\n\n")]
    return find_research_gap(fake_paper_list)

@tool
def methodology_tool(topic_and_gap: str) -> str:
    """Suggest a methodology and tools for a given topic and identified research gap."""
    topic, gap = topic_and_gap.split("||")
    return suggest_methodology_based_on_gap(topic, gap)
