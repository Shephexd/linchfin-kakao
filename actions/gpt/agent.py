import os
from typing import List, Type
from openai import OpenAI, AuthenticationError


GPT_API_KEY = os.getenv("GPT_API_KEY", "")
MODEL = "gpt-3.5-turbo"

openai_client = OpenAI(
    api_key=GPT_API_KEY
)


def ask_gpt_reply(input_msg, input_history: List[str] = None):
    if input_history is None:
        input_history = []

    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "you are a helpful financial assistant for koreans. Need to translate response to korean"},
            ]
            + input_history\
            + [{"role": "user", "content": input_msg}]

        )
        if response.choices:
            return response.choices[0].message.content
        else:
            return "적절한 답을 찾지 못했습니다."
    except AuthenticationError:
        return "토큰이 만료되었습니다."


if __name__ == "__main__":
    a = ask_gpt_reply("무슨 대답이 가능해?")
    print(a)
