from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

conversion = Table(
    'states',
    metadata,
    Column('id', String),
    Column('file_name', String, nullable=False),
    Column('start_extension', String, nullable=False),
    Column('final_extension', String, nullable=False),
    Column('state', Integer)
)