import fitz  # PyMuPDF
import re
import os

def extract_paragraphs_from_pdf(pdf_path):
    """
    Extract paragraphs from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of extracted paragraphs
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return []
        
    # Open the PDF file
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return []
    
    paragraphs = []  # Store extracted paragraphs
    print(f"Processing PDF with {pdf_document.page_count} pages...")
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        print(f"Processing page {page_num + 1}/{pdf_document.page_count}")
            
        # Extract text as blocks for better structure analysis
        blocks = page.get_text("dict")["blocks"]
        
        current_paragraph = ""
        prev_block_type = None
        
        for block in blocks:
            if "lines" not in block:
                continue  # Skip non-text blocks (e.g., images)
                
            block_text = []
            line_lengths = []
            
            for line in block["lines"]:
                line_text = "".join(span["text"] for span in line["spans"]).strip()
                if line_text:
                    block_text.append(line_text)
                    line_lengths.append(len(line_text))
            
            if not block_text:
                continue
                
            # Simple table detection
            is_table = False
            
            # Check for table indicators like | or multiple colons in lines
            if any('|' in line or line.count(':') > 1 for line in block_text):
                is_table = True
                
            # Check for tabular structure (multiple short lines of similar length)
            if len(block_text) > 1 and all(len(line) < 20 for line in block_text):
                is_table = True
            
            if is_table:
                # If we were building a paragraph, end it
                if current_paragraph:
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = ""
                # Skip this table block
                prev_block_type = "table"
                continue
                
            # Process non-table block as potential paragraph
            combined_text = " ".join(block_text).strip()
            
            # Skip very short blocks that are likely headers or noise
            if len(combined_text) < 20 and len(block_text) == 1:
                prev_block_type = "short"
                continue
                
            # Determine if this should be a new paragraph or continue the current one
            if current_paragraph:
                # Simple heuristic: start new paragraph if previous ended with period
                # and this starts with capital letter
                if (current_paragraph[-1] in '.!?' and 
                    combined_text and combined_text[0].isupper()):
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = combined_text
                else:
                    # Continue current paragraph
                    current_paragraph += " " + combined_text
            else:
                current_paragraph = combined_text
                
            prev_block_type = "text"
            
        # Add the last paragraph from the page
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = ""
    
    pdf_document.close()
    
    # Clean paragraphs
    cleaned_paragraphs = []
    for para in paragraphs:
        if para:
            # Remove multiple spaces
            cleaned = re.sub(r'\s+', ' ', para).strip()
            # Remove hyphenation (words broken across lines)
            cleaned = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', cleaned)
            # Fix common OCR issues
            cleaned = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', cleaned)  # Fix missing space after period
            
            # Only add if it's a substantial paragraph
            if len(cleaned) > 20:
                cleaned_paragraphs.append(cleaned)
    
    return cleaned_paragraphs

# Example of how to use
pdf_path = "data/tabletext.pdf"  # Replace with your PDF path
paragraphs = extract_paragraphs_from_pdf(pdf_path)

print("\n=== Extracted Paragraphs ===")
for i, para in enumerate(paragraphs, 1):
    print(f"\nParagraph {i}:")
    print(para)
    print("-" * 80)
print(f"\nTotal paragraphs extracted: {len(paragraphs)}")

# Optional: Save to file
with open("extracted_paragraphs.txt", "w", encoding="utf-8") as f:
    for para in paragraphs:
        f.write(para + "\n\n")