import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file, preserving paragraph structure.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of extracted paragraphs
    """
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        print(f"Processing PDF with {pdf_document.page_count} pages...")
        
        paragraphs = []
        current_paragraph = ""
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            print(f"Processing page {page_num + 1}/{pdf_document.page_count}")
            
            # Extract text blocks
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" not in block:
                    continue  # Skip non-text blocks
                
                # Extract text from all lines in this block
                block_text = []
                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    if line_text:
                        block_text.append(line_text)
                
                # Join lines with spaces
                if block_text:
                    text = " ".join(block_text)
                    
                    # If we have text already in current paragraph
                    if current_paragraph:
                        # Simple rule: new paragraph if current ends with period and new starts with capital
                        if (current_paragraph[-1] in '.!?' and 
                            text and text[0].isupper()):
                            # Save current paragraph and start new one
                            paragraphs.append(current_paragraph.strip())
                            current_paragraph = text
                        else:
                            # Continue current paragraph
                            current_paragraph += " " + text
                    else:
                        # Start new paragraph
                        current_paragraph = text
            
            # End paragraph at page boundary if not empty
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""
        
        pdf_document.close()
        
        # Clean up paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            if para:
                # Remove multiple spaces
                cleaned = re.sub(r'\s+', ' ', para).strip()
                # Remove hyphenation (words broken across lines)
                cleaned = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', cleaned)
                # Fix missing spaces after periods
                cleaned = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', cleaned)
                
                # Only add if not too short
                if len(cleaned) > 10:
                    cleaned_paragraphs.append(cleaned)
        
        return cleaned_paragraphs
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []

# Example usage
pdf_path = "data/tabletext.pdf"  # Replace with your PDF path
paragraphs = extract_text_from_pdf(pdf_path)

print("\n=== Extracted Text ===")
for i, para in enumerate(paragraphs, 1):
    print(f"\nParagraph {i}:")
    print(para)
    print("-" * 80)
print(f"\nTotal paragraphs extracted: {len(paragraphs)}")

# Save to file
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    for para in paragraphs:
        f.write(para + "\n\n")