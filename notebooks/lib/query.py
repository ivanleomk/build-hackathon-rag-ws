from lancedb.table import Table
from tqdm import tqdm
from lib.openai_helpers import generate_embeddings


def full_text_search(table: Table, queries, top_k):
    data = []
    for query in tqdm(queries):
        items = table.search(query["query"], query_type="fts").limit(top_k).to_list()
        data.append([item["chunk_id"] for item in items])
    return data


def semantic_search(table: Table, queries, top_k):
    data = []
    embedded_queries = generate_embeddings(queries, 20)
    for embedding in tqdm(embedded_queries):
        items = table.search(embedding, query_type="vector").limit(top_k).to_list()
        data.append([item["chunk_id"] for item in items])
    return data


def hybrid_search(table: Table, queries, top_k):
    data = []
    for query in tqdm(queries):
        items = table.search(query["query"], query_type="hybrid").limit(top_k).to_list()
        data.append([item["chunk_id"] for item in items])
    return data
