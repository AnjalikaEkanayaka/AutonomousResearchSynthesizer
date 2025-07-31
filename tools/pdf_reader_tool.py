from langchain.tools import tool
import fitz  # PyMuPDF

@tool
def pdf_reader_tool(file_path: str) -> str:
    """
    Extracts and returns the first 4000 characters of text from the uploaded PDF.
    This helps avoid token limit errors when sending to Gemini.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            return "⚠️ No readable text found in the PDF. Please try a different file."

        if len(text) > 4000:
            return text[:4000] + "\n\n⚠️ Note: Only the first 4000 characters were used to avoid API overload."

        return text
    except Exception as e:
        return f" Failed to read PDF: {e}"
