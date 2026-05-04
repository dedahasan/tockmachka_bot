import asyncio
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

# === НАСТРОЙКИ ===
TOKEN = "8796438464:AAHK2J5VHjI23r5W1QhDTdR1giKCcCNLPog"
AI_API_KEY = "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"

client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=AI_API_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def procent_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    percent = round(random.uniform(65.0, 99.0), 2)
    
    text = f"Текущий процент удержания Малой Токмачки - {percent}%"
    
    await update.message.reply_text(text)


# Регистрация обработчиков
def register_handlers(application: Application):
    application.add_handler(CommandHandler("процент", procent_handler))

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

@dp.message(Command("поздняков"))
async def news_command(message: types.Message):
    await message.reply("⏳ Думаем...")
    await generate_response(message, prompt_type="pozdnyak")


# ====================== ОБЩАЯ ФУНКЦИЯ ======================
async def generate_response(message: types.Message, prompt_type: str):
    try:
        if prompt_type == "normal":
            system_prompt = "Ты военный аналитик. Пиши нейтральную, но интересную сводку по Малой Токмачке."
        
        elif prompt_type == "ahmat":
            system_prompt = "Ты пропагандист ЧВК Ахмат. Начинай каждый ответ со слов (Как сообщает мой дорогой Брат АПТИ АЛЛАУДИНОВ). Сильно хвали спецназ Ахмат,Кадырова, Адам Кадыров получил медаль, пиши героически и пафосно."
        
        elif prompt_type == "finka":
            system_prompt = "Ты жёлтый военкор. Обязательно вставляй рекламу финок НКВД в каждом ответе."

        elif prompt_type == "pozdnyak":
            system_prompt = "Ты желтый военкор Поздняков. Ты лютый Z патриот но нелюбишь власть за их мягкость. Пиши очень эмоционально, используй неформальную речь, используй много мата, упомянай степашек и чурок, еблю в жопу, куколдизм, призывай к ядерным ударам, пиши часть слов КАПСОМ."
        
        elif prompt_type == "terpenie":
            system_prompt = """Пропогандируй терпение. Говори что нужно немного потерпеть, хвали тех кто терпит, используй цитаты славящие терпение"""

        response = await client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Напиши свежую сводку по боям вокруг Малой Токмачки.Максимум 5-6 предложений."}
            ],
            temperature=0.8,
            max_tokens=3000
        )

        text = response.choices[0].message.content.strip()
        
        if len(text) > 3800:
            text = text[:3750] + "... (продолжение 🔥)"
            
        await message.reply(text)

    except Exception as e:
        print("ПОЛНАЯ ОШИБКА:", str(e))
        await message.reply("❌ Ошибка генерации. Попробуй позже.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Бот запущен с несколькими командами")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
