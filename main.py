import requests
from fastapi import FastAPI, Form
from pdf2image import convert_from_bytes
import pytesseract
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.post("/search-word-url/")
async def search_word_in_pdf_url(
    file_url: str = Form(...),
    search_word: str = Form(...)
):
    # جلب الملف من SharePoint
    response = requests.get(file_url)
    pdf_bytes = response.content

    # تحويل PDF إلى صور
    images = convert_from_bytes(pdf_bytes)
    matching_pages = []

    for page in images:
        text = pytesseract.image_to_string(page)
        if search_word.lower() in text.lower():
            matching_pages.append(page)

    if matching_pages:
        output_pdf_path = "matched_pages.pdf"
        matching_pages[0].save(output_pdf_path, save_all=True, append_images=matching_pages[1:])
        return FileResponse(output_pdf_path, media_type="application/pdf", filename="matched_pages.pdf")
    else:
        return {"message": f"No pages found containing '{search_word}'."}
