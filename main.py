from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from pdf2image import convert_from_bytes
import pytesseract
import os
import uvicorn


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()
@app.post("/search-word/")
async def search_word_in_pdf(
    file: UploadFile = File(...),
    search_word: str = Form(...)
):
    pdf_bytes = await file.read()
    images = convert_from_bytes(pdf_bytes)
    matching_pages = []

    for page in images:
        text = pytesseract.image_to_string(page)
        if search_word.lower() in text.lower():
            matching_pages.append(page)
    if matching_pages:
        output_pdf_path = os.path.join(f"matched_pages.pdf")
        matching_pages[0].save(output_pdf_path, save_all=True, append_images=matching_pages[1:])
        return FileResponse(
            output_pdf_path,
            media_type="application/pdf",
            filename=f"matched_pages.pdf"
        )

    else:
        return {"message": f"No pages found containing '{search_word}'."}
