from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr


# ======================================================
# 1. LOAD ENVIRONMENT + OPENAI CLIENT
# ======================================================

load_dotenv(override=True)

openai = OpenAI()


# ======================================================
# 2. SYSTEM MESSAGE
# ======================================================

system_message = """
You are miliGPT, a helpful AI assistant created by Almir.

Your style:
- Be clear and simple.
- Answer in a friendly way.
- If the user asks in Albanian, answer in Albanian.
- If the user asks in English, answer in English.
- If you are not sure, say so clearly.
- Do not pretend to know live/current information unless the user provides it.
"""


# ======================================================
# 3. GPT FUNCTION
# ======================================================

def message_gpt(user_message):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content


# ======================================================
# 4. GRADIO INPUT + OUTPUT
# ======================================================

message_input = gr.Textbox(
    label="Your message",
    info="Ask miliGPT anything",
    lines=7,
    placeholder="Write your message here..."
)

message_output = gr.Markdown(
    label="miliGPT response"
)


# ======================================================
# 5. GRADIO INTERFACE
# ======================================================

view = gr.Interface(
    fn=message_gpt,
    title="miliGPT",
    description="""
Private AI assistant · Model alpe2.1
""",
    inputs=[message_input],
    outputs=[message_output],
    examples=[
    "Explain React state in simple terms.",
    "Give me 5 ideas for an AI real estate assistant.",
    "Write a professional email to a client.",
    "Kush është kryeqyteti i Shqipërisë?"
],
    flagging_mode="never"
)


# ======================================================
# 6. LAUNCH WITH LOGIN + PUBLIC SHARE LINK
# ======================================================

view.launch(
    inbrowser=True,
    share=True,
    auth=[
        ("almir", "mili123"),
        ("friend", "demo123")
    ]
)


