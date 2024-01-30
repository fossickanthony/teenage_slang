from openai import OpenAI
import streamlit as st
import time

st.title("Human to Teenager")

client = OpenAI()

def get_translation_from_model(text, persona):
    try:
        for response in client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": text}
            ],
            temperature=0,
            stream=True,
        ):
            yield response.choices[0].delta.content or ""
    except BadRequestError as bad_request:
        pass

def run_pass(label, persona, text):
    label
    full_response = ""
    message_placeholder = st.empty()
    for response in get_translation_from_model(text, persona):
        full_response += response
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    return full_response

original_prompt = "Hey, what's up, bro? What can Fossick translate for you today?"
target_language = "modern teenager slang"

message_placeholder = st.empty()
full_response = ""

original_text = st.text_area("English")
go = st.button("break it down")

if not original_text:
    for c in original_prompt:
        full_response += c
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.03)
    message_placeholder.markdown(full_response)
elif not go:
    message_placeholder.markdown(original_prompt)
else:
    persona = f"Keep the original English but fill it with common {target_language} words and expressions. Do not tell me why you changed things, only show me the English with {target_language} words and phrases."

    message_placeholder.markdown(original_prompt)

    first = run_pass(f"{target_language}:", persona, original_text)
