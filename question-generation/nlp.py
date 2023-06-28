#!/usr/bin/env python3

from transformers import BartTokenizer, BartForConditionalGeneration
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
    tokenizer = BartTokenizer.from_pretrained(model_id)
    model = BartForConditionalGeneration.from_pretrained(model_id)

    # Make use of CUDA if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    inputs = tokenizer(sequence, return_tensors="pt").to(device)

    model.to(device)
    with torch.no_grad():
        generated_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=64,
            min_length=9,
            num_return_sequences=4,
            diversity_penalty=1.0,
            num_beam_groups=4,
        )

    # Decode the generated token IDs and return the result as a list of strings
    return tokenizer.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )


def get_contexts_and_questions(file_name: str) -> "tuple[list, list]":
    """Retrieve a list of contexts and their corresponding list of generated questions.

    Each context is associated with one randomly selected question.
    This is a naive and potentially time consuming operation.

    Args:
        file_name: The name of the text file containing the context sequences.

    Returns:
        A tuple containing the list of contexts and their corresponding
        list of generated questions.
    """

    contexts = Path(file_name).read_text().split("\n")
    questions = [random.choice(generate_questions(c)) for c in contexts]

    return contexts, questions
