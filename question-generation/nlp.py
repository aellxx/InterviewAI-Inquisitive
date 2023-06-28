from transformers import pipeline


def interview_ai(sequence: str, num_questions: int) -> "list[str]":
    """Generate questions based on a given sequence of context using Interview AI.

    Args:
        sequence: A string representing the context from which to generate questions.
        num_questions: The number of questions to generate.

    Returns:
        A list of generated questions as strings.
    """

    model_id = "hyechanjun/interview-question-remake"
    pipe = pipeline("text2text-generation", model=model_id)

    outputs = pipe(
        sequence,
        max_length=64,
        min_length=9,
        num_beams=4,
        num_return_sequences=num_questions,
        diversity_penalty=1.0,
        num_beam_groups=4,
    )

    return [output["generated_text"] for output in outputs]


def get_questions(sequence: str, num_questions: int) -> "list[str]":
    """Interface for the back-end server.

    Args:
        sequence: A string representing the context from which to generate questions.
        num_questions: The number of questions to generate.

    Returns:
        A list of generated questions as strings.
    """
    return interview_ai(sequence, num_questions=1)
