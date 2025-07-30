from langchain.tools import tool
import fitz  # PyMuPDF

@tool
def pdf_reader_tool(file_path: str) -> str:
    """Extracts text from the uploaded PDF for Gemini to read."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text[:4000]  # limit to 4000 chars for model input
    except Exception as e:
        return f"Failed to read PDF: {e}"
