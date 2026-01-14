import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=GOOGLE_API_KEY, temperature=0)

PROMPT = """
You are given DB schema and a user question. Produce a safe SELECT-only SQL query (no mutations).\nSchema:\n{schema}\nQuestion:\n{question}\nRespond with ONLY the SQL query, no markdown formatting or explanations.
"""

def run_nl_analytics_query(question: str):
    try:
        schema = "products(product_id, name, price, cost_price, stock_quantity), bills(bill_id, user_id, total_amount, created_at), bill_items(bill_item_id, bill_id, product_id, quantity, price_per_unit, subtotal)"
        prompt = PromptTemplate(input_variables=['schema','question'], template=PROMPT)
        chain = LLMChain(llm=llm, prompt=prompt)
        sql = chain.run({'schema': schema, 'question': question}).strip().rstrip(';')
        
        # Remove markdown code blocks if present
        if sql.startswith('```'):
            sql = sql.replace('```sql', '').replace('```', '').strip()
        
        if not sql or not sql.lower().strip().startswith('select'):
            return {'error':'Only SELECT queries allowed', 'sql': sql}
        
        engine = create_engine(DATABASE_URL, future=True)
        with engine.connect() as conn:
            res = conn.execute(text(sql))
            rows = [dict(r._mapping) for r in res]
        return {'success': True, 'sql': sql, 'rows': rows, 'count': len(rows)}
    except Exception as e:
        return {'error': str(e), 'sql': sql if 'sql' in locals() else None}
