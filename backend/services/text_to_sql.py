import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

db = SQLDatabase.from_uri(DATABASE_URL)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
sql_chain = create_sql_query_chain(llm, db)

SAFE_PREFIXES = ("select", "with")

def _is_safe_sql(sql: str) -> bool:
    if not sql:
        return False
    return sql.strip().lower().startswith(SAFE_PREFIXES)

def run_nl_analytics_query(nl_query: str):
    try:
        generated = sql_chain.invoke({"question": nl_query})
        sql = (generated or "").strip().strip(';')
        if not _is_safe_sql(sql):
            return {"error":"Only SELECT/CTE queries allowed", "sql": sql}
        engine = create_engine(DATABASE_URL, future=True)
        with engine.connect() as conn:
            res = conn.execute(text(sql))
            rows = [dict(r._mapping) for r in res]
        return {"sql": sql, "rows": rows}
    except Exception as e:
        return {"error": str(e)}
