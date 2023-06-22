from pydantic import BaseModel


class ConversionCreate(BaseModel):
    id: int
    file_name: str
    start_extension: str = 'mp4'
    final_extension: str = 'mkv'
    state: int