from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_hello():
    return "Hello world!"


@app.post("/upload/file")
def upload_file(file: UploadFile):
    pass


@app.get("/check/{file_id}")
def check_state(file_id: str):
    pass

@app.get("/download/{file_id}")
def download_file(file_id: str):


"""
uvicorn main:app --reload
"""