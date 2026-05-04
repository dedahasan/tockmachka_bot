import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# === НАСТРОЙКИ ===
TOKEN = "8796438464:AAHK2J5VHjI23r5W1QhDTdR1giKCcCNLPog"
AI_API_KEY = "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"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====================== КОМАНДА /процент ======================
@dp.message(Command("процент"))
async def procent_handler(message: types.Message):
    percent = round(random.uniform(65.0, 99.0), 2)
    text = f"Текущий процент удержания Малой Токмачки - {percent}%"
    await message.reply(text)


# ====================== ОСТАЛЬНЫЕ КОМАНДЫ ======================
@dp.message(Command("front", "токмачка"))
async def front_command(message: types.Message):
    await message.reply("⏳ Генерирую сводку...")
    await generate_response(message, prompt_type="normal")


@dp.message(Command("ahmat", "ахмат"))
async def ahmat_command(message: types.Message):
    await message.reply("⏳ Ахмат на связи...")
    await generate_response(message, prompt_type="ahmat")


@dp.message(Command("finka", "финка"))
async def finka_command(message: types.Message):
    await message.reply("⏳ Финка НКВД в деле...")
    await generate_response(message, prompt_type="finka")


@dp.message(Command("терпение"))
async def terpenie_command(message: types.Message):
    await message.reply("⏳ Осталось немного потерпеть...")
    await generate_response(message, prompt_type="terpenie")


@dp.message(Command("поздняков"))
async def pozdnyak_command(message: types.Message):
    await message.reply("⏳ Думаем...")
    await generate_response(message, prompt_type="pozdnyak")


# ====================== ОБЩАЯ ФУНКЦИЯ ======================
async def generate_response(message: types.Message, prompt_type: str):
    # ... (твой код generate_response без изменений)
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

        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=AI_API_KEY)

        response = await client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Напиши свежую сводку по боям вокруг Малой Токмачки. Максимум 5-6 предложений."}
            ],
            temperature=0.8,
            max_tokens=3000
        )

        text = response.choices[0].message.content.strip()
        await message.reply(text)

    except Exception as e:
        print("ПОЛНАЯ ОШИБКА:", str(e))
        await message.reply("❌ Ошибка генерации. Попробуй позже.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Бот успешно запущен!")
    print("Доступные команды: /процент, /ahmat, /токмачка, /терпение, /поздняков")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
