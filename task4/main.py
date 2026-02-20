from openai import OpenAI

# Reading .env file without libs
env_store = {
    line.split('=', 1)[0]: line.split('=', 1)[1].strip()
    for line in open('../.env')
    if '=' in line and not line.startswith('#')
}

API_KEY = env_store.get("OPEN_AI_API_KEY", "")
MODEL = "gpt-4"
MAX_ANSWER_TOKENS = 2000
client = OpenAI(api_key=API_KEY)
print("Use :q to exit")

while True:
    input_text = input("> ")

    if input_text.strip() == "":
        continue

    if input_text == ":q":
        break

    response = client.chat.completions.create(
        model=MODEL,
        temperature=1,
        max_completion_tokens=MAX_ANSWER_TOKENS,
        messages=[
            {"role": "user", "content": input_text},
        ],
    )

    print(f"bot> {response.choices[0].message.content}")
    print(f"input tokens: {response.usage.prompt_tokens}\n"
          f"output tokens {response.usage.completion_tokens}")
