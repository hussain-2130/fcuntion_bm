import fitz  # PyMuPDF
import os
import tempfile
import shutil

def add_highlight_annot(highlights, filepath):
    
    
    doc = fitz.open(filepath)

    # Build full text with page offsets
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    highlights_sorted = sorted(highlights, key=lambda x: x[0], reverse=True)

    for start, end, label in highlights_sorted:
        if start < 0 or end > len(full_text) or start >= end:
            raise ValueError(f"Invalid index range: ({start}, {end})")

        target_str = full_text[start:end].strip()
        if not target_str:
            continue

        found = False
        for page in doc:
            matches = page.search_for(target_str)
            if matches:
                for inst in matches:
                    annot = page.add_highlight_annot(inst)
                    annot.set_info(title=label)
                    annot.update()
                found = True
                break

        if not found:
            print(f"Warning: Text '{target_str}' not found in PDF.")

    # Save to a temporary file, then replace original
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_path = tmp.name

    doc.save(temp_path, garbage=4, deflate=True)
    doc.close()

    shutil.move(temp_path, filepath)  # overwrite original file safely
    return filepath

result_path = add_highlight_annot([
    (3100, 3130, "Point A"),
    (300, 320, "Fact")
], r"C:\Users\HP\Desktop\function_bm\12. Master Services Agreement.pdf")

print("Updated:", result_path)
