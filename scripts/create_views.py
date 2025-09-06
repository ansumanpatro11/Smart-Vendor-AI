import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, future=True)
with engine.connect() as conn:
    sql = open('sql/views.sql').read()
    conn.execute(text(sql))
    conn.commit()
print('Views created')