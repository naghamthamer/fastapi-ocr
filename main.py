from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pdf2image import convert_from_bytes
import pytesseract
import os

app = FastAPI()

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    images = convert_from_bytes(pdf_bytes)

    # استخراج النصوص من جميع الصفحات (OCR)
    full_text = ""
    for page in images:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    # حفظ كل الصفحات في PDF جديد (اختياري)
    output_pdf_path = "processed_file.pdf"
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])

    return FileResponse(output_pdf_path, media_type="application/pdf", filename="processed_file.pdf")
