from pydantic import BaseModel


class CreateState(BaseModel):
    id: int
    file_name: str
    start_extension: str = 'mp4'
    final_extension: str = 'mkv'
    state: int