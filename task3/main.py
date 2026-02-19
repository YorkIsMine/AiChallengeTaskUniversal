from openai import OpenAI

# Reading .env file without libs
env_store = {
    line.split('=', 1)[0]: line.split('=', 1)[1].strip()
    for line in open('../.env')
    if '=' in line and not line.startswith('#')
}

# 1) Что надо делать, чтобы не быть замененным в эпоху искусственного интеллекта?
# 2) Что надо делать, чтобы не быть замененным в эпоху искусственного интеллекта? Реши задачу по шагам
# 3) Составь промпт для более точного решения этой задачи: Что надо делать, чтобы не быть замененным в эпоху искусственного интеллекта? На промпт не отвечай!
# 4) Ты - ассистент по решению задач. Для заданной задачи тебе необходимо
# представить себя в ролях разных экспертов для решения задач, такие как: айтишник, психолог, критик, президент.
# Каждая роль должна включать себя минимум из 3 шагов

SYS_PROMPT = """Ты - ассистент по решению задач. Для заданной задачи тебе необходимо
представить себя в ролях разных экспертов для решения задач, такие как: айтишник, психолог, критик, президент.
Каждая роль должна включать себя минимум из 3 шагов"""

# Расскажите о навыках, умениях или качествах, которые могут помочь человеку оставаться востребованным и незаменимым в условиях развития искусственного интеллекта.

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
        max_completion_tokens=MAX_ANSWER_TOKENS,
        messages=[
            {"role": "system", "content": f"{SYS_PROMPT}"},
            {"role": "user", "content": input_text},
        ],
    )

    print(f"bot> {response.choices[0].message.content}")
    print(f"input tokens: {response.usage.prompt_tokens}\n"
          f"output tokens {response.usage.completion_tokens}")
