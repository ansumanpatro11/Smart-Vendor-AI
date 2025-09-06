import os
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from backend import models

load_dotenv()

class ParsedItem(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., description="Quantity sold")
    price_per_unit: float = Field(..., description="Per-unit selling price")

class ParsedBill(BaseModel):
    customer_name: Optional[str] = None
    date: Optional[str] = None
    total_amount: Optional[float] = None
    items: List[ParsedItem] = Field(default_factory=list)

class DBMappedItem(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

class DBReadyBill(BaseModel):
    customer_name: Optional[str] = None
    total_amount: Optional[float] = None
    items: List[DBMappedItem]

parser = PydanticOutputParser(pydantic_object=ParsedBill)

PROMPT_TMPL = """
You extract structured bill data from the text strictly following the format instructions.

Text:
{bill_text}

{format_instructions}
"""

def _map_items_to_db_ids(items: List[ParsedItem], db: Session) -> List[DBMappedItem]:
    mapped: List[DBMappedItem] = []
    for it in items:
        prod = db.query(models.Product).filter(models.Product.name.ilike(it.product_name)).first()
        if not prod:
            prod = db.query(models.Product).filter(models.Product.name.ilike(f"{it.product_name}%")).first()
        if not prod:
            raise ValueError(f"Product '{it.product_name}' not found in catalog")
        mapped.append(DBMappedItem(product_id=prod.product_id, quantity=it.quantity, price_per_unit=it.price_per_unit))
    return mapped

async def parse_bill_text(bill_text: str, db: Session) -> DBReadyBill:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate(
        template=PROMPT_TMPL,
        input_variables=["bill_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    try:
        response = await llm.apredict(prompt.format(bill_text=bill_text))
        parsed = parser.parse(response)
        mapped_items = _map_items_to_db_ids(parsed.items, db) if parsed.items else []
        total = parsed.total_amount
        if (total is None or total == 0) and mapped_items:
            total = sum(i.quantity * i.price_per_unit for i in mapped_items)
        return DBReadyBill(customer_name=parsed.customer_name, total_amount=total, items=mapped_items)
    except Exception as e:
        print("LLM parsing error:", e)
        return DBReadyBill(customer_name=None, total_amount=None, items=[])
