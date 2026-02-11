import PyPDF2
import sys

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            return text
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_text.py <path_to_pdf_file>")
        sys.exit(1)
    
    pdf_file_path = sys.argv[1]
    extracted_text = extract_text_from_pdf(pdf_file_path)
    print(extracted_text)
