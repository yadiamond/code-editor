from openai import OpenAI


def get_response(message, api_key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return completion.choices[0].message.content
