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
            print(f"🧩 Trying to highlight '{expected_text}' ({start}-{end})")
            
            # Get all instances of the text on the page
            text_instances = page.search_for(expected_text)
            
            # Find the correct instance that matches our exact position
            if text_instances:
                # Get words with positions to verify correct instance
                words = page.get_text("words")
                current_pos = 0
                word_positions = []
                
                # Build position mapping
                for word in words:
                    word_text = word[4]
                    word_len = len(word_text)
                    word_positions.append((current_pos, current_pos + word_len, fitz.Rect(word[:4])))
                    current_pos += word_len + 1  # +1 for space
                
                # Find words that contain our target position
                for instance_rect in text_instances:
                    # Check if this rectangle corresponds to text at our position
                    is_correct_instance = False
                    
                    for word_start, word_end, word_rect in word_positions:
                        # If word overlaps with our target position
                        if (word_start <= local_start < word_end or 
                            word_start < local_end <= word_end or
                            (local_start <= word_start and word_end <= local_end)):
                            
                            # Check if this word's rectangle intersects with our instance
                            if word_rect.intersects(instance_rect):
                                is_correct_instance = True
                                break
                    
                    if is_correct_instance:
                        # Create highlight annotation
                        highlight = page.add_highlight_annot(instance_rect)
                        highlight.set_info(title=label)
                        highlight.update()
                        print(f"✅ Highlighted '{label}' at exact position")
                        break
                else:
                    print(f"❌ Could not find correct instance for: '{expected_text}'")
            else:
                print(f"❌ No matches found for: '{expected_text}'")
        
        global_offset += page_length
    
    output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"\n✅ Highlighting complete. File saved at: {output_path}")

pdf_path = r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf"
highlights = [
    
    (700, 1576, "SRH")
]
add_highlight_annot(pdf_path, highlights)