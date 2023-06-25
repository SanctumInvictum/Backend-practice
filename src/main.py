from fastapi import FastAPI, UploadFile, Depends, HTTPException
import s3_Yandex as s3
from models import states
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase import get_async_session
from Converter import converter as converter_router
from Kafka import router as kafka_router
import uuid


# Создаем экземляр приложения
app = FastAPI()

app.include_router(converter_router.router)
app.include_router(kafka_router.route)


# Эндпоинт с POST-запросом для прикрепления файла
@app.post("/file/upload-file")
async def upload_file(file: UploadFile, final_ext: str, session: AsyncSession = Depends(get_async_session)):
    file_id = str(uuid.uuid4())
    try:
        stmt = insert(states).values(id=file_id, file_name=file.filename, start_extension=file.filename.split('.')[-1], final_extension=final_ext, state=0)
        await session.execute(stmt)
        await session.commit()
        s3.upload(file=file.file, object_name='upload/'+file.filename)
        kafkaProducer.produce_data(topic='test-topic2', data=file_id)
        return {"status": 200, "data": file_id}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


# uvicorn main:app --reload
# Эндпоинт с GET-запросом для чтения данных о состоянии конвертации файла
@app.get("/check/{file_id}")
async def check_state(file_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = states.select().where(states.c.id == file_id)
        result = await session.execute(query)
        status = result.fetchone()[-1]
        match status:
            case 0:
                return {'status': 200, 'response': "Файл успешно загружен"}
            case 1:
                return {'status': 200, 'response': "Идет обработка"}
            case _:
                return {'status': 500, 'response': "Неверное состояние файла"}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

# Эндпоинт с GET-запросом для получения переконвертированного файла из S3
@app.get("/download/{file_name}")
async def download_file(file_id: str, session: AsyncSession = Depends(get_async_session)):
    query = states.select().where(states.c.id == file_id)
    result = await session.execute(query)
    file_name = result.fetchone()[1]
    s3.download('download/{}'.format(file_name), 'converter/Converted_files/{}'.format(file_name))
    return {"status": 200, "data": file_name}

