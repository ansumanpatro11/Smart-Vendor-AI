# backend/services/semantic_service.py

# Use community embeddings
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
import pinecone
from backend.models.models import Product
from sqlalchemy.orm import Session

# Initialize Pinecone
pinecone.init(api_key="PINECONE_API", environment="us-east-1")  # adjust environment
index_name = "products"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=384)  # MiniLM-L6-v2 outputs 384 dim
index = pinecone.Index(index_name)

# Embedding model
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def add_products_to_vector_db(db: Session):
    products = db.query(Product).all()
    for p in products:
        text = f"{p.name} {p.category or ''}"
        vec = embeddings_model.embed_query(text)
        index.upsert([(str(p.product_id), vec, {"name": p.name, "category": p.category})])

def semantic_search_product(query: str, top_k: int = 1):
    query_vec = embeddings_model.embed_query(query)
    res = index.query(vector=query_vec, top_k=top_k, include_metadata=True)
    if res['matches']:
        match = res['matches'][0]
        return int(match['id']), match['metadata']['name']
    return None, None
