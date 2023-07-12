import streamlit as st

from backend import genQuestion

# Examples for each models
context_example = ''
context_length = ''
examples = [
    "Well, I was born in South Africa, lived there until I was 17. Came to North America of my own accord, against my parent’s wishes. And was in Canada for a few years. I started school there which is where I met my wife. Transferred down to the University of Pennsylvania and got a degree in physics, degree in business at Wharton. Came out to California with the intent of doing a PHD in the material science and physics [unintelligible] with an eye towards using that as an energy storage unit for electric vehicles. I ended up deferring that graduate work to start a couple to start a couple of area companies, one of which people have heard about, such as Pay Pal.",
    "Hi my name is Maria Sanchez, and I was born in Japan. I lived there for 20 years and moved out to the United States for college. I studied graphic design and later realized that my true passion was in fashion. It's lovely to see amazing models wearing my collection this fall, can't wait to show it to you guys soon. ",
    "I moved from Indiana to California when I was 19 to pursue my career as an young entrepreneur with a small loan of million dollars. My first start up was Blindr, where we sold blinders that auto adjusts depending on the time of the day. It was revolutionary, in only 2 years, we were able to accumulate 10 million customers and gain attraction internationally. We are planning to go further beyond this year with Blindr 2.0 where not only auto adjusts your blinders, but it also detects intruders who are violating your privacy at any time. ",
    "I think things out well. When I speak, I speak with conviction. If I feel like it's something that best suits me and my person, I deal with it. I say it. I have no problem speaking out publicly about issues. But for personal things, and for things about personal selfishness, or wanting more money, I don't do that. Once I give my word, that's it. I don't go back to renegotiate. I don't renegotiate my contracts."
]

# Wide page layout
st.set_page_config(layout="wide")

# Title
st.title("Interview AI Test Website")
st.caption("With the advent of machine learning, it has become increasingly clear that AI is capable of completing tasks that were hitherto considered only possible by human minds. We are now pushing the boundaries of what AI can do with natural language processing (NLP), from summarizing pages of text to keeping up a conversation with a human. Our project aims to join those on the frontier of machine learning by creating an AI Interviewer. There are two main problems to address here: first, whether creating such an interviewer will be possible, and second, whether it will be any good. The models have been fed datasets derived from https://www.kaggle.com/datasets/shuyangli94/interview-npr-media-dialog-transcripts")

# Adding a Session State to store stateful variables
if 'button_sent' not in st.session_state:
    st.session_state.button_sent = False

col1, col2, col3 = st.columns(3)

context_option = col2.selectbox(
    'Feel free to choose one of our premade contexts',
    ('Select one','Elon Musk', 'Fashion designer', 'Young entrepreneur', 'Michael Jordan')
)

if context_option == 'Select one':
    context_example = ""
elif context_option == 'Elon Musk':
    context_example = examples[0]
elif context_option == 'Fashion designer':
    context_example = examples[1]
elif context_option == 'Young entrepreneur':
    context_example = examples[2]
else:
    context_example = examples[3]

option = col1.selectbox(
    'Please select a model.',
    ('Base model', 'Lengthed model', 'Reverse model')
)

if option == 'Base model':
    st.write("This is the re-fine-tuned base model for our interview AI. It returns strings terminating in a question mark (?).")
elif option == 'Lengthed model':
    st.write("This is a length-tagged version of our interview AI. You can specify how long its responses should be (ranges of multiples of 10)")
elif option == 'Reverse model':
    st.write("This model asks a question that would have resulted in the context you provide (a.k.a. it traverses backward through the interview)")

if option == 'Lengthed model':
    context_length = col3.selectbox(
        'Length of response',
        ('1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91+')
    )

# Input fields
# user inputs context to construct a response (str)
input = st.text_area('Context', value=context_example)

if st.button('Submit') or st.session_state.button_sent:
    with st.spinner('Generating a response...'):
        output = genQuestion(option, input, context_length)
        print(output)
    st.session_state.button_sent = True
    st.text_area(label="Generated Responses:", value=output, height=200)
