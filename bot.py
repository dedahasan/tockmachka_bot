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

@dp.message(Command("ahmat", "ахмат"))
async def ahmat_command(message: types.Message):
    await message.reply("⏳ Ахмат на связи...")

     try:
        response = await client.chat.completions.create(
            model="openrouter/owl-alpha",   # ← Более стабильная модель
            messages=[
                {"role": "system", "content": 
"""."""},
                {"role": "user", "content": "Напиши свежую сводку по боям вокруг Малой Токмачки в своём безумном стиле."}
            ],
            temperature=0.85,
            max_tokens=1000
        )


# ====================== КОМАНДА 1 ======================
@dp.message(Command("front", "токмачка"))
async def front_command(message: types.Message):
    await message.reply("⏳ Генерирую сводку...")
    await generate_response(message, prompt_type="normal")


# ====================== КОМАНДА 2 ======================
@dp.message(Command("ahmat","ахмат"))
async def ahmat_command(message: types.Message):
    await message.reply("⏳ Ахмат на связи...")
    await generate_response(message, prompt_type="ahmat")


# ====================== КОМАНДА 3 ======================
@dp.message(Command("finka", "финка"))
async def finka_command(message: types.Message):
    await message.reply("⏳ Финка НКВД в деле...")
    await generate_response(message, prompt_type="finka")


# ====================== КОМАНДА 4 ======================
@dp.message(Command("терпение"))
async def news_command(message: types.Message):
    await message.reply("⏳ Осталось немного потерпеть...")
    await generate_response(message, prompt_type="terpenie")


# ====================== ОБЩАЯ ФУНКЦИЯ ======================
async def generate_response(message: types.Message, prompt_type: str):
    try:
        if prompt_type == "normal":
            system_prompt = "Ты военный аналитик. Пиши нейтральную, но интересную сводку по Малой Токмачке."
        
        elif prompt_type == "ahmat":
            system_prompt = "Ты пропагандист ЧВК Ахмат. Сильно хвали спецназ Ахмат,Кадырова, пиши героически и пафосно."
        
        elif prompt_type == "finka":
            system_prompt = "Ты жёлтый военкор. Обязательно вставляй рекламу финок НКВД в каждом ответе."
        
        elif prompt_type == "terpenie":
            system_prompt = """Пропогандируй терпение. Говори что нужно немного потерпеть, хвали тех кто терпит, используй цитаты славящие терпение"""

        response = await client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Напиши свежую сводку по боям вокруг Малой Токмачки."}
            ],
            temperature=0.7,
            max_tokens=2500
        )

        text = response.choices[0].message.content.strip()
        
        if len(text) > 3800:
            text = text[:3750] + "... (продолжение 🔥)"
            
        await message.reply(text)

    except Exception as e:
        print("ПОЛНАЯ ОШИБКА:", str(e))
        await message.reply("❌ Ошибка генерации. Попробуй позже.")

async def main():
    print("✅ Бот запущен | Умная обрезка включена")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
