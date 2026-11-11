"""Your code goes here.

Right now SupportAgent sends the conversation to Gemini with no tools,
so it can chat but knows nothing about orders. Your job is to turn it into
a support agent. The requirements are in README.md.
"""

from google import genai
from google.genai import types

import store  # noqa: F401  (you'll use this)

MODEL = "gemini-3.6-flash"  # if you hit errors or rate limits, try "gemini-3.8-flash"

SYSTEM_PROMPT = """You are a customer support assistant for Brightcart, an online electronics store."""
# TODO: tell the model what it can and cannot do.


# TODO: declare the functions the model can call (types.FunctionDeclaration).
TOOLS: list[types.Tool] = []


def run_tool(name: str, args: dict) -> dict:
    """TODO: call the matching function in store.py and return the result."""
    raise NotImplementedError(name)


class SupportAgent:
    def __init__(self) -> None:
        self.client = genai.Client()  # reads GEMINI_API_KEY from the environment
        self.history: list[types.Content] = []

    def respond(self, user_message: str) -> str:
        self.history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

        response = self.client.models.generate_content(
            model=MODEL,
            contents=self.history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )

        # TODO: handle function calls. Today this only works when the model answers directly.

        self.history.append(response.candidates[0].content)

        return response.text or ""
