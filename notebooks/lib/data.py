from datasets import load_dataset, Dataset
from tqdm import tqdm
import hashlib
import json

def get_dataset(n:int):
    return load_dataset("ms_marco", "v1.1", split="train", streaming=True).take(
        n
    )

def generate_data_and_labels(dataset: Dataset):
    passages = set()
    data = []
    labels = []
    for row in tqdm(dataset):
        selected_passages = []
        for idx, passage in enumerate(row["passages"]["passage_text"]):
            if passage not in passages:
                chunk_id = hashlib.md5(passage.encode()).hexdigest()
                passage_data_obj = {"text": passage, "chunk_id": chunk_id}
                data.append(passage_data_obj)
                passages.add(passage)

                if row["passages"]["is_selected"][idx]:
                    selected_passages.append(passage_data_obj)

        if selected_passages:
            labels.append(
                {
                    "query": row["query"],
                    "selected_passages": selected_passages,
                    "answer": row["answers"],
                    "query_id": row["query_id"],
                    "query_type": row["query_type"],
                }
            )

    print(
        f"Extracted {len(passages)} unique passages and {len(labels)} test queries"
    )
    return data, labels

def save_labels(labels,file_path):
    with open(file_path, "w") as file:
        for label in labels:
            file.write(json.dumps(label) + "\n")
    print(f"Labels saved to {file_path}")

def generate_test_labels(labels, has_single_label:bool):
    res = []

    for row in labels:
        if has_single_label:
            for passage in row['selected_passages']:
                res.append({
                    "query": row["query"],
                    "selected_chunk_id": passage["chunk_id"],
                })
        else:
            res.append({
                "query": row["query"],
                "selected_chunk_ids": [passage["chunk_id"] for passage in row['selected_passages']],
            })
    
    return res

def get_labels(file_path):
    """
    We assume that this is a .jsonl file
    """
    with open(file_path, "r") as f:
        labels = []
        for line in f:
            labels.append(json.loads(line))
    return labels

