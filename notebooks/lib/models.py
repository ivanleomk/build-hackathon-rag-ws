from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

func = get_registry().get("openai").create(name="text-embedding-3-small")


class EmbeddedPassage(LanceModel):
    vector: Vector(dim=func.ndims()) = func.VectorField()  # type: ignore
    chunk_id: str
    text: str = func.SourceField()


class EmbeddedText(LanceModel):
    vector: Vector(dim=func.ndims()) = func.VectorField()  # type: ignore
    chunk_id: str
    text: str = func.SourceField()
    source_text: str
