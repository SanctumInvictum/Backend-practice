from fastapi import FastAPI, UploadFile, Depends
import s3_Yandex as s3
from models import states
from schemas import OperationCreate
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase import get_async_session
import uuid

# Создаем экземляр приложения
app = FastAPI()


# Эндпоинт с POST-запросом для прикрепления файла
@app.post("/file/upload-file")
async def upload_file(file: UploadFile, final_ext: str, session: AsyncSession = Depends(get_async_session)):
    file_id = str(uuid.uuid4())
    stmt = insert(states).values(id=file_id, file_name=file.filename, start_extension=file.filename.split('.')[-1], final_extension=final_ext, state=0)
    await session.execute(stmt)
    await session.commit()
    s3.upload(file=file.file, object_name='upload/'+file.filename)
    return {"status": 200, "data": file_id}

# uvicorn main:app --reload
# Эндпоинт с GET-запросом для чтения данных о состоянии конвертации файла
@app.get("/check/{file_id}")
async def check_state(file_id: str, session: AsyncSession = Depends(get_async_session)):
    query = states.select().where(states.c.id == file_id)
    result = await session.execute(query)
    status = result.fetchone()[-1]
    match status:
        case 0:
            return {'status': 200, 'response': "Файл успешно загружен"}
        case 1:
            return {'status': 200, 'response': "Вы находитесь в очереди"}
        case 2:
            return {'status': 200, 'response': "Идет обработка"}
        case 3:
            return {'status': 200,
                    'response': f"Вы можете получить свои данные http://127.0.0.1:8000/download/{file_id}"}
        case 4:
            return {'status': 200, 'response': "Файл уже удален"}
        case _:
            return {'status': 500, 'response': "Неверное состояние файла"}


# Эндпоинт с GET-запросом для получения переконвертированного файла из S3
@app.get("/download/{file_id}")
async def download_file(file_name: str):
    s3.download('download/'+file_name)
    return {"status": 200, "data": file_name}

