import instructor
import openai
from pydantic import BaseModel, Field
from tqdm.asyncio import tqdm_asyncio as asyncio
from asyncio import Semaphore
from tenacity import retry, stop_after_attempt, wait_random_exponential

client = instructor.from_openai(openai.AsyncOpenAI())


class QuestionAnswerPair(BaseModel):
    """
    This model represents a single question and answer generated from a text chunk and it's corresponding answer.
    """

    question: str = Field(
        ..., description="The generated question from the text chunk."
    )
    answer: str = Field(..., description="The answer to the generated question.")


class QuestionAnswerResponse(BaseModel):
    """
    This model represents questions and answers generated from a text chunk with some chain of thought included.The chain of thought provides insight into how the answer
    was derived from each question.

    Generate a minimum of 3 question and answer pairs
    """

    chain_of_thought: str = Field(
        ..., description="The reasoning process leading to the answer."
    )
    questions: list[QuestionAnswerPair] = Field(
        ...,
        description="The questions and answers generated from the text chunk.",
        min_length=3,
    )


async def generate_question_batch(text_chunk_batch, max_concurrent_calls: int):
    sem = Semaphore(max_concurrent_calls)

    @retry(
        wait=wait_random_exponential(multiplier=1, min=10, max=90),
        stop=stop_after_attempt(3),
    )
    async def generate_question(text: str):
        async with sem:
            question = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world class AI that excels at generating hypothethical questions that users might have based off a specific text chunk. Make sure to generate at least 3 questions and answers. Each question should be specific to the text chunk and answer should be specific to the question asked. ",
                    },
                    {"role": "user", "content": f"Here is the text chunk : {text}"},
                ],
                response_model=QuestionAnswerResponse,
                max_retries=3,
            )
            return (question.questions, text)

    coros = [generate_question(item) for item in text_chunk_batch]
    res = await asyncio.gather(*coros)
    return [{"response": item, "source": text} for item, text in res]
