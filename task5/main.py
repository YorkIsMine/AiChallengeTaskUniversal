import litellm
from litellm import completion
import time
import os

# Загрузка ключа
try:
    env_store = {
        line.split('=', 1)[0]: line.split('=', 1)[1].strip()
        for line in open('../.env')
        if '=' in line and not line.startswith('#')
    }
except FileNotFoundError:
    env_store = {}

OPENAI_KEY = env_store.get("OPEN_AI_API_KEY", "")


def benchmark_openai(prompt):
    models_config = [
        {"level": "Слабая (GPT-4o-mini)", "id": "gpt-4o-mini"},
        {"level": "Средняя (GPT-4o)", "id": "gpt-4o"},
        {"level": "Сильная (GPT 5.2)", "id": "openai/gpt-5.2"}
    ]

    results = {}
    print(f"\n" + "=" * 60)

    for model in models_config:
        print(f"📡 Анализ через {model['level']}...")
        try:
            start_time = time.time()
            response = completion(
                model=model['id'],
                messages=[{"role": "user", "content": prompt}],
                api_key=OPENAI_KEY
            )
            end_time = time.time()

            duration = round(end_time - start_time, 2)
            tokens = response['usage']['total_tokens']
            cost = litellm.completion_cost(completion_response=response)
            answer = response['choices'][0]['message']['content']

            results[model['level']] = {
                "time": duration, "tokens": tokens,
                "cost": f"${cost:.5f}", "answer": answer
            }
        except Exception as e:
            results[model['level']] = {"time": "ERR", "tokens": 0, "cost": "0", "answer": f"Ошибка: {e}"}

    # Вывод сравнительной таблицы после каждого запроса
    print(f"\n{'Модель':<20} | {'Время':<8} | {'Токены':<8} | {'Стоимость':<10}")
    print("-" * 60)
    for label, data in results.items():
        print(f"{label:<20} | {data['time']:<8} | {data['tokens']:<8} | {data['cost']:<10}")
        short_answer = data['answer']
        print(f"   └─ {short_answer}...")
    print("=" * 60)


# Основной цикл ввода
if __name__ == "__main__":
    print("🤖 Система сравнения моделей OpenAI запущена.")
    print("Введите ваш запрос для сравнения (или 'exit' для выхода):")

    while True:
        user_input = input("\n📝 Ваш запрос: ").strip()

        if user_input.lower() in ['exit', 'quit', 'выход', 'стоп']:
            print("👋 Завершение работы.")
            break

        if not user_input:
            continue

        benchmark_openai(user_input)