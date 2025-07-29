from langchain.tools import Tool
import fitz #PyMuPDF

def read_pdf_content(path):
    try:
        doc = fitz.open(path)
        text = "\n".join([page.get_text() for page in doc])
        return f"Extracted content from PDF:\n{text[:2000]}"
    exception Exception as e:
        return f"Failed to read PDF: {e}"

pdf_reader_tool = Tool(
    name="PDFReader",
    func=lambda x: read_pdf_content(x),
    description="Use this tool to read and summarize a given PDF file path."
)