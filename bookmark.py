import fitz  # PyMuPDF

def add_highlight_annot(pdf_path, highlights):
    doc = fitz.open(pdf_path)
    global_offset = 0
    
    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text()
        page_length = len(page_text)
        print(f"📃 Page {page_num} | Characters: {global_offset} to {global_offset + page_length}")
        
        # Filter highlights for this page
        current_page_highlights = [
            (start, end, label)
            for start, end, label in highlights
            if global_offset <= start < end <= global_offset + page_length
        ]
        print(f"🔍 Found {len(current_page_highlights)} highlights for this page.")
        
        for start, end, label in current_page_highlights:
            local_start = start - global_offset
            local_end = end - global_offset
            expected_text = page_text[local_start:local_end]
            print(f"🧩 Trying to highlight '{expected_text[:30]}...' ({start}-{end})")
            
            # For large text blocks, we need to handle them differently
            # Break the text into smaller chunks that PyMuPDF can handle
            chunk_size = 50  # Adjust chunk size as needed
            highlighted_something = False
            
            # Process the text in chunks
            for chunk_start in range(local_start, local_end, chunk_size):
                chunk_end = min(chunk_start + chunk_size, local_end)
                chunk_text = page_text[chunk_start:chunk_end]
                
                if not chunk_text.strip():  # Skip empty chunks
                    continue
                
                # Find this chunk on the page
                matches = page.search_for(chunk_text)
                
                if matches:
                    # Apply highlight to each match
                    for rect in matches:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_info(title=f"{label} (part)")
                        highlight.update()
                        highlighted_something = True
                        print(f"✅ Highlighted chunk: '{chunk_text[:20]}...'")
                else:
                    # If exact chunk not found, try word by word highlighting
                    words = chunk_text.split()
                    for word in words:
                        if len(word) < 3:  # Skip very short words
                            continue
                        word_matches = page.search_for(word)
                        for rect in word_matches:
                            highlight = page.add_highlight_annot(rect)
                            highlight.set_info(title=f"{label} (word)")
                            highlight.update()
                            highlighted_something = True
            
            if highlighted_something:
                print(f"✅ Highlighted full range for '{label}'")
            else:
                print(f"❌ Could not highlight text range for: '{expected_text[:30]}...'")
        
        global_offset += page_length
    
    output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"\n✅ Highlighting complete. File saved at: {output_path}")

pdf_path = r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf"
highlights = [
  
    (640, 660, "CSK")
]
add_highlight_annot(pdf_path, highlights)

