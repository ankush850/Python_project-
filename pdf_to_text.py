import PyPDF2
import os
import sys

def create_temp_dir(directory="temp"):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    return os.path.realpath(directory)

def get_file_paths():
    pdf_path = input("Enter the full path of your PDF file (use backslash for directories): ").strip()
    txt_path = input("Enter the full path of your output TXT file (leave empty to save in temp folder): ").strip()
    return pdf_path, txt_path

def validate_pdf_path(pdf_path):
    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file '{pdf_path}' does not exist.")
        sys.exit(1)
    if not pdf_path.lower().endswith(".pdf"):
        print("Error: The input file is not a PDF.")
        sys.exit(1)

def build_txt_path(pdf_path, txt_path, base_dir):
    if txt_path == "":
        base_name = os.path.basename(pdf_path)
        txt_name = os.path.splitext(base_name)[0] + ".txt"
        txt_path = os.path.join(base_dir, txt_name)
    return txt_path

def extract_text_from_pdf(pdf_path):
    text_content = []
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            if text:
                text_content.append(text)
    return "\n".join(text_content)

def save_text_to_file(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def main():
    base_dir = create_temp_dir()
    print(f"Text files will be saved in: {base_dir}")

    pdf_path, txt_path = get_file_paths()
    validate_pdf_path(pdf_path)
    txt_path = build_txt_path(pdf_path, txt_path, base_dir)

    print(f"Extracting text from: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text.strip() == "":
        print("Warning: No text was extracted from the PDF.")
    else:
        print(f"Extracted text length: {len(extracted_text)} characters")

    save_text_to_file(extracted_text, txt_path)
    print(f"Text saved to: {txt_path}")

if __name__ == "__main__":
    main()
