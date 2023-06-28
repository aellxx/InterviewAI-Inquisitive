from transformers import pipeline
from pathlib import Path
import random
import torch


def interview_ai(sequence: str) -> "list[str]":
    """Generate questions based on a given sequence of context using Interview AI.

    Args:
        sequence: A string representing the context from which to generate questions.

    Returns:
        A list of generated questions as strings. The number of questions returned
        is determined by the num_return_sequences parameter of the model's generate method.
    """

    model_id = "hyechanjun/interview-question-remake"
    pipe = pipeline("text2text-generation", model=model_id)

    return pipe(
        sequence,
        max_length=64,
        min_length=9,
        num_beams=4,
        num_return_sequences=4,
        diversity_penalty=1.0,
        num_beam_groups=4,
    )
