import lancedb
from lancedb.pydantic import LanceModel
import os
from itertools import batched
from tqdm import tqdm


def get_table(db, table_name: str, schema: LanceModel):
    # We return the table if it exists
    if table_name in db.table_names():
        return db.open_table(table_name)

    return db.create_table(table_name, schema=schema)


def insert_data_into_table(table, data, batch_size=20):
    batches = batched(data, batch_size)

    for batch in tqdm(batches):
        table.add(list(batch))
