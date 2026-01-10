import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

TOKEN = "8260684976:AAE6c4zlsgDVb_3M3VHeM5WSuUgBikTAR2s"
OWNER_ID = 5724011932

bot = Bot(token=TOKEN)
dp = Dispatcher()
message_map = {}

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Доброго времени суток!👋\n"
        "Вас приветствует анонимная служба доставки сообщений ✨Stars Delivery Service✨!\n"
        "Сообщения 100% анонимны."
    )

# Обработка всех сообщений
@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id == OWNER_ID and message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        if replied_id in message_map:
            target_id = message_map[replied_id]
            await bot.send_message(target_id, f"{message.text}")
            await message.answer("✅ Ответ отправлен.")
        return

    if message.from_user.id != OWNER_ID:
        sent = await bot.send_message(OWNER_ID, f"{message.text}")
        message_map[sent.message_id] = message.from_user.id

# === Настройка Webhook ===
async def on_startup(app):
    await bot.delete_webhook()
    domain = "ВАШ_ДОМЕН.up.railway.app"  # сюда вставьте ваш Railway домен
    await bot.set_webhook(f"https://{domain}/{TOKEN}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.close()

# === Создание aiohttp сервера для webhook ===
async def handle_webhook(request):
    update = types.Update(**await request.json())
    await dp.process_update(update)
    return web.Response(text="OK")

app = web.Application()
app.router.add_post(f"/{TOKEN}", handle_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

# Проверка сервера
async def hello(request):
    return web.Response(text="Bot is alive")
app.router.add_get("/", hello)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
