from itertools import batched
from openai import Client
from tqdm.asyncio import tqdm_asyncio as asyncio

client = Client()

def generate_embeddings(data,batch_size):
    batches = batched(data,batch_size)

    def generate_embeddings_batch(batch):
        res = client.embeddings.create(
            model="text-embedding-3-small", 
            input=[item['query'] for item in batch] 
        )
        return res.data

    batched_embeddings = [generate_embeddings_batch(list(batch)) for batch in batches]

    res = []
    for embeddings in batched_embeddings:
        for embedding in embeddings:
            res.append(embedding.embedding)
    
    return res

        
