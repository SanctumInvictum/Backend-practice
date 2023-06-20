
# uvicorn main:app --reload
from fastapi import FastAPI, UploadFile
import s3_Yandex as s3

# Создаем экземляр приложения
app = FastAPI()


# Эндпоинт с POST-запросом для прикрепления файла
@app.post("/file/upload-file")
async def upload_file(file: UploadFile):
    s3.upload(file=file.file, object_name='upload/'+file.filename)
    return {"status": 200, "data": file.filename}


# Эндпоинт с GET-запросом для чтения данных о состоянии конвертации файла
@app.get("/check/{file_name}")
async def check_state(file_name: str):
    return {"status": 200, "data": file_name}


# Эндпоинт с GET-запросом для получения переконвертированного файла из S3
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    s3.download('download/'+file_name)
    return {"status": 200, "data": file_name}

