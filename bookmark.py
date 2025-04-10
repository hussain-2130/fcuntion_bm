import fitz  # PyMuPDF
import fitz  # PyMuPDF

def add_highlight_annot(pdf_path, highlights):
    doc = fitz.open(pdf_path)
    global_offset = 0

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text()
        page_length = len(page_text)
        print(f"📃 Page {page_num} | Characters: {global_offset} to {global_offset + page_length}")

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
            print(f"🧩 Looking for: '{expected_text}' ({start}-{end})")

            matches = page.search_for(expected_text)
            if matches:
                for match in matches:
                    page.add_highlight_annot(match).set_info(title=label)
                print(f"✅ Highlighted '{label}' with {len(matches)} part(s)")
            else:
                print(f"❌ Could not find match for: '{expected_text}'")

        global_offset += page_length

    output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"\n✅ Highlighting complete. File saved at: {output_path}")


   




pdf_path = r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf"
highlights = [
    (1000, 1760,"mumbaimumbai"),
]

add_highlight_annot(pdf_path, highlights)
