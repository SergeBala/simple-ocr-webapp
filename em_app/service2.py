from fastapi import FastAPI, UploadFile, File, HTTPException
import random
import pytesseract
from PIL import Image
import io

#this is just a placeholder little way of actually processing the image, just for fun! it only works on screenshots of text
def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    if text and text[-1] == '/n':
        text = text[:-1]
    return text

app = FastAPI()

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        employee_id  = extract_text_from_image(file_bytes)
        print(f"Here's what service2 managed to read from the id photo:{employee_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not (employee_id.isdigit() and len(employee_id) == 3):
        employee_id = f"{random.randint(100, 999)}"
    return {"employee_id": employee_id}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Image Processing Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)