import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


# ======================================================
# 1. NGARKO ENVIRONMENT + KRIJO CLIENTS
# ======================================================

load_dotenv(override=True)

klienti_openai = OpenAI()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if Anthropic is not None and anthropic_api_key:
    klienti_claude = Anthropic(api_key=anthropic_api_key)
else:
    klienti_claude = None


# ======================================================
# 2. MESAZHI I SISTEMIT
# ======================================================

mesazhi_sistem = """
You are miliGPT, a helpful AI assistant created by Almir.

Your style:
- Be clear and simple.
- Answer in markdown.
- Do not wrap the whole answer in a code block.
- Answer in a friendly way.
- If the user asks in Albanian, answer in Albanian.
- If the user asks in English, answer in English.
- If you are not sure, say so clearly.
- Do not pretend to know live/current information unless the user provides it.
"""


# ======================================================
# 3. FUNKSIONI GPT LIVE / STREAMING
# ======================================================

def pergjigju_gpt_live(mesazhi_i_perdoruesit):
    mesazhet = [
        {"role": "system", "content": mesazhi_sistem},
        {"role": "user", "content": mesazhi_i_perdoruesit}
    ]

    rrjedha_pergjigjes = klienti_openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=mesazhet,
        stream=True
    )

    pergjigjja_deri_tani = ""

    for copa in rrjedha_pergjigjes:
        teksti_i_ri = copa.choices[0].delta.content or ""
        pergjigjja_deri_tani = pergjigjja_deri_tani + teksti_i_ri
        yield pergjigjja_deri_tani


# ======================================================
# 4. FUNKSIONI CLAUDE LIVE / STREAMING
# ======================================================

def pergjigju_claude_live(mesazhi_i_perdoruesit):
    if klienti_claude is None:
        yield """
Claude is not configured.

To use Claude:
1. Install the Anthropic package:
   pip install anthropic

2. Add this to your .env file:
   ANTHROPIC_API_KEY=your_key_here
"""
        return

    pergjigjja_deri_tani = ""

    with klienti_claude.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1200,
        system=mesazhi_sistem,
        messages=[
            {"role": "user", "content": mesazhi_i_perdoruesit}
        ]
    ) as rrjedha_pergjigjes:
        for teksti_i_ri in rrjedha_pergjigjes.text_stream:
            pergjigjja_deri_tani = pergjigjja_deri_tani + teksti_i_ri
            yield pergjigjja_deri_tani


# ======================================================
# 5. FUNKSIONI QE ZGJEDH MODELIN
# ======================================================

def pergjigju_sipas_modelit(mesazhi_i_perdoruesit, modeli_i_zgjedhur):
    if modeli_i_zgjedhur == "GPT":
        pergjigjja = pergjigju_gpt_live(mesazhi_i_perdoruesit)

    elif modeli_i_zgjedhur == "Claude":
        pergjigjja = pergjigju_claude_live(mesazhi_i_perdoruesit)

    else:
        yield "Model i panjohur. Zgjidh GPT ose Claude."
        return

    yield from pergjigjja


# ======================================================
# 6. GRADIO INPUTS + OUTPUT
# ======================================================

kutia_mesazhit = gr.Textbox(
    label="Mesazhi yt",
    info="Shkruaj pyetjen ose kërkesën për miliGPT",
    lines=7,
    placeholder="Shkruaj mesazhin këtu..."
)

zgjedhja_modelit = gr.Dropdown(
    choices=["GPT", "Claude"],
    value="GPT",
    label="Zgjidh modelin",
    info="Zgjidh nëse përgjigjja do vijë nga GPT ose Claude"
)

shfaqja_pergjigjes = gr.Markdown(
    label="Përgjigjja e miliGPT"
)


# ======================================================
# 7. GRADIO INTERFACE
# ======================================================

pamja = gr.Interface(
    fn=pergjigju_sipas_modelit,
    title="miliGPT · Multi-Model Assistant",
    description="""
Private AI assistant · Choose GPT or Claude · Streaming responses
""",
    inputs=[kutia_mesazhit, zgjedhja_modelit],
    outputs=[shfaqja_pergjigjes],
    examples=[
        ["Explain React state in simple terms.", "GPT"],
        ["Explain the Transformer architecture to a layperson.", "GPT"],
        ["Explain the Transformer architecture to an aspiring AI engineer.", "Claude"],
        ["Give me 5 ideas for an AI real estate assistant.", "GPT"],
        ["Write a professional email to a client.", "Claude"],
        ["Kush është kryeqyteti i Shqipërisë?", "GPT"]
    ],
    flagging_mode="never"
)


# ======================================================
# 8. HAPE APP-IN ME LOGIN + PUBLIC SHARE LINK
# ======================================================

pamja.launch(
    inbrowser=True,
    share=True,
    auth=[
        ("almir", "mili123"),
        ("friend", "demo123")
    ]
)