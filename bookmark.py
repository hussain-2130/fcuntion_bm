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
            print(f"🧩 Trying to highlight '{expected_text}' ({start}-{end})")

            matches = page.search_for(expected_text)
            print(f"matches{matches}")
            found_exact = False
            for match in matches:
           

                for i in range(len(page_text) - len(expected_text) + 1):
                    candidate = page_text[i:i+len(expected_text)]

                    if candidate == expected_text and i == local_start:
                        print(f"matched candidate {match}" )

                        highlight = page.add_highlight_annot(match)
                        highlight.set_info(title=label)
                        found_exact = True
                        print(f"✅ Highlighted '{label}'")
                        break
                if found_exact:
                    break

            if not found_exact:
                print(f"❌ Could not match exact position for: '{expected_text}'")

        global_offset += page_length

    output_path = pdf_path.replace(".pdf", "_highlighted.pdf")
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
    print(f"\n✅ Highlighting complete. File saved at: {output_path}")





pdf_path = r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf"
highlights = [
    (0, 760,"zzzzzzzzzzzzzzz"),
    (100, 110, "FACT"),
    (300, 320, "POINT A")
]

add_highlight_annot(pdf_path, highlights)
