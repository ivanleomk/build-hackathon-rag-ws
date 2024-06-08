from notebooks.lib.db import get_table, insert_data_into_table
from notebooks.lib.data import (
    get_dataset,
    generate_data_and_labels,
    generate_test_labels,
    save_labels,
)
from notebooks.lib.models import EmbeddedPassage
import lancedb


def setup_table():
    db = lancedb.connect("lance")
    table = get_table(db, "ms_marco", EmbeddedPassage)
    dataset = get_dataset(100)
    data, labels = generate_data_and_labels(dataset)
    insert_data_into_table(table, data)

    single_label = generate_test_labels(labels, True)
    multi_label = generate_test_labels(labels, False)

    save_labels(single_label, "queries_single_label.json")
    save_labels(multi_label, "queries_multi_label.json")

    table.create_fts_index("text")


if __name__ == "__main__":
    setup_table()
