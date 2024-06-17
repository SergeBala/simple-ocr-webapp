from fastapi import FastAPI, UploadFile, File
import random
import pytesseract
from PIL import Image
import io

def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

app = FastAPI()

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Simulate image processing and generate a numeric employee ID
    employee_id = extract_text_from_image()
    if not (employee_id.isdigit() and len(s) == 3): 
        employee_id = f"{random.randint(100, 999)}"
    return {"employee_id": employee_id}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Image Processing Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)