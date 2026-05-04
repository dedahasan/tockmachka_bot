import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

# === НАСТРОЙКИ ===
TOKEN = "8796438464:AAHK2J5VHjI23r5W1QhDTdR1giKCcCNLPog"
AI_API_KEY = "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"

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",   # ← Должно быть именно так
    api_key=AI_API_KEY
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def smart_truncate(text: str, max_length: int = 3800):
    if len(text) <= max_length:
        return text
    
    # Ищем последнее полное предложение
    for end in ['. ', '! ', '? ']:
        pos = text[:max_length].rfind(end)
        if pos > 100:  # нашли нормальную точку
            return text[:pos + 1].strip()
    
    # Если не нашли — обрезаем жёстко
    return text[:max_length - 50] + "... (продолжение в следующей серии 🔥)"

@dp.message(Command("news", "front", "токмачка"))
async def front_command(message: types.Message):
    await message.reply("⏳ Анализирую ситуацию вокруг Малой Токмачки...")
    
    try:
        response = await client.chat.completions.create(
            model="openrouter/owl-alpha",   # ← Более стабильная модель
            messages=[
                {"role": "system", "content": 
"""Ты — главный редактор самой жёлтой газеты "Токмачка Экспресс".
Стиль: гротескный, сенсационный, саркастичный, как у желтой прессы.
Используй чёрный юмор и преувеличения.
Пиши ОЧЕНЬ КОРОТКО!
Максимум 4 предложения.
Максимум 3200 символов.
В каждом ответе обязательно упомяни спецназ "Ахмат" и рекламу финок НКВД.
Пиши ТОЛЬКО чистую сводку на русском языке.
Без заголовков, без "Сводка", без дат, без вступлений.
Сразу начинай с текста.
Максимум 5 предложений."""},
                {"role": "user", "content": "Напиши свежую сводку по боям вокруг Малой Токмачки в своём безумном стиле."}
            ],
            temperature=0.65,
            max_tokens=2000
        )

# Получаем текст
        text = ""
        if hasattr(response, 'choices') and response.choices:
            message_obj = response.choices[0].message
            if message_obj and hasattr(message_obj, 'content'):
                text = message_obj.content or ""

        if not text.strip():
            text = "В Малой Токмачке тишина... Попробуй позже (активированы белые списки) 🔥"

        # Умная обрезка
        final_text = smart_truncate(text.strip())

        await message.reply(final_text)

    except Exception as e:
        print("ПОЛНАЯ ОШИБКА:", str(e))
        await message.reply("❌ Ошибка генерации. Попробуй позже.")

async def main():
    print("✅ Бот запущен | Умная обрезка включена")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
