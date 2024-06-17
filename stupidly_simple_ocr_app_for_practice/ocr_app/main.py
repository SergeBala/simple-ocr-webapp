from fastapi import FastAPI, UploadFile, File, HTTPException
from ocr_app.ocr_utils import extract_text_from_image
import os
import requests
import base64

app = FastAPI()

IMGBB_API_KEY = "insert the key here"
EXPIRATION_TIME = 120

def print_and_return(msg):
    print(msg)
    return {"message": msg}

@app.get("/")
async def root(name: str = ""):
    return {"message": "Welcome to the OCR API"}

# @app.post("/ocr")
# async def ocr(file: UploadFile=File(...)):
#     text = extract_text_from_image(await file.read())
#     return {"filename": file.filename, "text": text}

@app.post("/ocr")
async def ocr(file_name, file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text_from_image(file_bytes)

        base64_image = base64.b64encode(file_bytes).decode('utf-8')
        # Upload the image to imgbb
        imgbb_url = upload_to_imgbb(file_name, base64_image)

        return {"filename": file.filename, "text": text, "imgbb_url": imgbb_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def upload_to_imgbb(filename: str, file_bytes: bytes) -> str:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": file_bytes,
        "name": filename,
        "expiration": EXPIRATION_TIME
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data['data']['url']
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to upload image to imgbb")

@app.post("/write")
async def write_to_file(file_name: str, file_content: str="You content could be here"):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user_files', file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(file_content)
        log_info = f"File '{file_name}' created and written to successfully."
        return print_and_return(log_info)
    except IOError as e:
        log_info = f"An I/O error occurred while writing to the file: {e}"
        return print_and_return(log_info)
    except Exception as e:
        log_info = f"An unexpected error occurred: {e}"
        return print_and_return(log_info)
    
@app.post("/read")
async def read_file(file_name_read):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user_files', file_name_read)
    try: 
        with open (file_path, 'r') as file:
            content = file.read()
    except IOError as e:
        log_info = f"An I/O error occurred while reading from the file: {e}"
        return print_and_return(log_info)
    except Exception as e:
        log_info = f"An unexpected error occurred: {e}"
        return print_and_return(log_info)
    if content == "":
        return print_and_return(f"File {file_name_read} is empty!")
    print(f"Successfully read the following content from file {file_name_read}:")
    return print_and_return(content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
