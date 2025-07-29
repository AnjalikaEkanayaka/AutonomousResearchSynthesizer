import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=5, subject_filter=None, year_filter=None):
    search_query = f"all:{query}"
    if subject_filter:
        search_query += f"+AND+cat:{subject_filter}"

    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={max_results}"

    response = requests.get(url)
    papers = []

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            published = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            pub_year = published[:4]

            if year_filter and pub_year != str(year_filter):
                continue  # skip this paper

            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text.strip()
                       for author in entry.findall('{http://www.w3.org/2005/Atom}author')]

            papers.append({
                'title': title,
                'summary': summary,
                'link': link,
                'authors': ', '.join(authors)
            })

        return papers