import fitz  # PyMuPDF
import tempfile
import shutil
def add_highlight_annot(highlights, filepath):
    doc = fitz.open(filepath)
    global_offset = 0

    for page_num, page in enumerate(doc):
        text = page.get_text()
        page_length = len(text)
        print(f"\n📃 Page {page_num + 1} | Characters: {global_offset} to {global_offset + page_length}")

        # Filter highlights for this page
        current_page_highlights = []
        for start, end, label in highlights:
            if global_offset <= start < end <= global_offset + page_length:
                current_page_highlights.append((start, end, label))

        print(f"🔍 Found {len(current_page_highlights)} highlights for this page.")

        for start, end, label in current_page_highlights:
            local_start = start - global_offset
            local_end = end - global_offset
            target_text = text[local_start:local_end].strip()

            if not target_text:
                print(f"⚠️ Empty or invalid selection between {local_start}–{local_end} for label '{label}'")
                continue

            matches = page.search_for(target_text)
            print(f"🧩 Trying to highlight '{target_text}' ({start}-{end}) → Matches found: {len(matches)}")

            match_found = False
            for match in matches:
                match_text = page.get_textbox(match).strip()
                match_index = text.find(match_text)

                if match_index == local_start:
                    highlight = page.add_highlight_annot(match)
                    highlight.set_colors(stroke=(1, 1, 0))  # Yellow
                    highlight.set_info(title=label)
                    highlight.update()
                    print(f"✅ Highlighted '{target_text}' on page {page_num + 1} as '{label}'")
                    match_found = True
                    break

            if not match_found:
                print(f"❌ Could not match exact position for: '{target_text}'")

        global_offset += page_length
        return filepath
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
     temp_path = tmp.name

    doc.save(temp_path, garbage=4, deflate=True)
    doc.close()

    shutil.move(temp_path, filepath)  # overwrite original file safely
    return filepath
    # Save updated PDF

highlights = [
   (550,560,"kkkkkkkkkkking")            # 'Machine Learning'
]
add_highlight_annot(highlights, r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf")
