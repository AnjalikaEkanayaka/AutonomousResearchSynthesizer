import requests

def search_semantic_scholar(topic, max_results=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": topic,
        "limit": max_results,
        "fields": "title,authors,abstract,url"
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        papers = response.json().get("data", [])
        return [
            {
                "title": paper["title"],
                "authors": ", ".join([author["name"] for author in paper.get("authors", [])]),
                "summary": paper.get("abstract", "No abstract available."),
                "link": paper.get("url", "")
            }
            for paper in papers
        ]
    else:
        print(" Semantic Scholar API failed:", response.status_code, response.text)
        return []
