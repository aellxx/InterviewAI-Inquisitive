#!/usr/bin/env python3

from transformers import BartTokenizer, BartForConditionalGeneration
from pathlib import Path
import torch


def load_contexts_from(file_name: Path) -> "list[str]":
    """Retrieve context sequences from a text file.

    Args:
        file_name: A path to the text file containing the context sequences.
          Each line represents a separate sequence.

    Returns:
        A list of context sequences as strings.

    Raises:
        FileNotFoundError: file_name does not exist.
    """

    if file_name.is_file():
        with open(file_name, "r") as f:
            return f.readlines()
    else:
        raise FileNotFoundError(f"'{file_name.name}' does not exist.")


def generate_questions(sequence: str) -> "list[str]":
    """Generate questions based on a given sequence of context.

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


if __name__ == "__main__":
    c = load_contexts_from(Path("context.txt"))
    print(c)
