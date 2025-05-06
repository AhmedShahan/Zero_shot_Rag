from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_text
import re

def extract_text_without_tables(pdf_path):
    """
    Extract paragraphs from a PDF file while removing tables.
    Uses unstructured.io for table detection and extraction.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of extracted paragraphs (tables removed)
    """
    try:
        print(f"Processing PDF: {pdf_path}")
        
        # Use unstructured.io to partition the PDF into different element types
        elements = partition_pdf(pdf_path, extract_images_in_pdf=False)
        
        paragraphs = []
        current_paragraph = ""
        
        # Process each element based on its type
        for element in elements:
            element_type = element.category
            
            # Skip tables and table-related elements
            if element_type in ["Table", "TableChunk", "ListItem"]:
                print(f"Skipping table content: {str(element)[:50]}...")
                continue
            
            # Process text elements
            if element_type == "Text" or element_type == "NarrativeText":
                text = str(element).strip()
                
                if not text:
                    continue
                
                # Check if this is a new paragraph
                if current_paragraph:
                    # Heuristic for paragraph breaks
                    if (current_paragraph[-1] in '.!?' and 
                        text and text[0].isupper()):
                        # End current paragraph
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = text
                    else:
                        # Continue current paragraph
                        current_paragraph += " " + text
                else:
                    current_paragraph = text
        
        # Add the last paragraph
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())
        
        # Clean up paragraphs
        cleaned_paragraphs = []
        for para in paragraphs:
            if para:
                # Remove multiple spaces
                cleaned = re.sub(r'\s+', ' ', para).strip()
                # Remove hyphenation
                cleaned = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', cleaned)
                # Fix missing spaces after periods
                cleaned = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', cleaned)
                
                # Only include substantial paragraphs
                if len(cleaned) > 20:
                    cleaned_paragraphs.append(cleaned)
        
        print(f"Extracted {len(cleaned_paragraphs)} paragraphs (tables removed)")
        return cleaned_paragraphs
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []

def save_paragraphs_to_file(paragraphs, output_file="extracted_paragraphs.txt"):
    """Save extracted paragraphs to a text file"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for para in paragraphs:
                f.write(para + "\n\n")
        print(f"Paragraphs saved to {output_file}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your PDF path
    pdf_path = "data/tabletext.pdf"
    
    # Extract paragraphs (removing tables)
    paragraphs = extract_text_without_tables(pdf_path)
    
    # Print extracted paragraphs
    print("\n=== Extracted Paragraphs (Tables Removed) ===")
    for i, para in enumerate(paragraphs, 1):
        print(f"\nParagraph {i}:")
        print(para)
        print("-" * 80)
    
    # Save to file
    save_paragraphs_to_file(paragraphs)

# Note: You need to install unstructured first:
# pip install "unstructured[pdf]"