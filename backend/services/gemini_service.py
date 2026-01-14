import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from backend.models.models import Product

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class ParsedItem(BaseModel):
    product_name: str = Field(...)
    quantity: int = Field(...)
    price_per_unit: float = Field(...)

class ParsedBill(BaseModel):
    items: List[ParsedItem] = Field(...)
    total_amount: float = Field(...)

parser = PydanticOutputParser(pydantic_object=ParsedBill)

def parse_bill_text_and_map(text: str, db):
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=GOOGLE_API_KEY, temperature=0)
    prompt = PromptTemplate(template='''Extract structured bill items from the following text and return JSON following format instructions.\n\n{format_instructions}\n\nBill:\n{text}\n''',
                            input_variables=['text'],
                            partial_variables={'format_instructions': parser.get_format_instructions()})
    resp = llm.invoke(prompt.format(text=text))
    parsed = parser.parse(resp.content)
    mapped_items = []
    for it in parsed.items:
        # try exact match then substring
        prod = db.query(Product).filter(Product.name.ilike(it.product_name)).first()
        if not prod:
            prod = db.query(Product).filter(Product.name.ilike(f"%{it.product_name}%")).first()
        if not prod:
            raise ValueError(f"Product '{it.product_name}' not found in catalog")
        mapped_items.append({'product_id': prod.product_id, 'quantity': it.quantity, 'price_per_unit': it.price_per_unit})
    total = parsed.total_amount or sum(i['quantity']*i['price_per_unit'] for i in mapped_items)
    return {'items': mapped_items, 'total': total}
