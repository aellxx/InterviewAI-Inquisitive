from transformers import BartForConditionalGeneration, BartTokenizer
import streamlit as st

@st.cache_data
def genQuestion(model_choice, context, tag):
    """Generate interview questions.
    
    Args:
        model_choice: specify which BART model to use.
        context: input text for the model.
        tag: specify the length of the generated question (only if model_choice is 'Lengthed model').

    Returns:
        final_output: the four decoded generated sequences, separated by two newlines.
    """

    model, tok = None, None

    # Checks which BART model to use based on the value of model_choice
    # Then loads a pre-trained BART model and tokenizer accordingly
    if model_choice=="Base model":
        model = BartForConditionalGeneration.from_pretrained("hyechanjun/interview-question-remake")
        tok = BartTokenizer.from_pretrained("hyechanjun/interview-question-remake")
    elif model_choice=="Lengthed model":
        model = BartForConditionalGeneration.from_pretrained("hyechanjun/interview-length-tagged")
        tok = BartTokenizer.from_pretrained("hyechanjun/interview-length-tagged")
        if (tag == '1-10'):
            context += ' <TEN>'
        elif (tag == '11-20'):
            context += ' <TWENTY>'
        elif (tag == '21-30'):
            context += ' <THIRTY>'
        elif (tag == '31-40'):
            context += ' <FORTY>'
        elif (tag == '51-60'):
            context += ' <FIFTY>'
        elif (tag == '61-70'):
            context += ' <SIXTY>'
        elif (tag == '71-80'):
            context += ' <SEVENTY>'
        elif (tag == '81-90'):
            context += ' <EIGHTY>'
        elif (tag == '81-90'):
            context += ' <NINETY>'
        elif (tag == '91+'):
            context += ' <HUNDRED>'
    elif model_choice=="Reverse model":
        model = BartForConditionalGeneration.from_pretrained("hyechanjun/reverse-interview-question")
        tok = BartTokenizer.from_pretrained("hyechanjun/reverse-interview-question")

    # Tokenize context parameter using the selected tokenizer
    inputs = tok(context, return_tensors="pt")

    # Generate text using the selected pre-trained BART model
    output = model.generate(inputs["input_ids"], num_beams=4, max_length=64, min_length=9, num_return_sequences=4, diversity_penalty=1.0, num_beam_groups=4)

    # Decode the generated text, then format it into a single string
    final_output = ''
    for i in range(4):
        final_output +=  [tok.decode(beam, skip_special_tokens=True, clean_up_tokenization_spaces=False) for beam in output][i] + "\n\n"

    return final_output
