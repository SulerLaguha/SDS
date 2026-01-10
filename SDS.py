import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "8260684976:AAE6c4zlsgDVb_3M3VHeM5WSuUgBikTAR2s"
OWNER_ID = 5724011932

bot = Bot(TOKEN)
dp = Dispatcher()

message_map = {}


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Доброго времени суток!👋\nВас приветствует анонимная служба доставки сообщений ✨Stars Delivery Service✨, или просто ✨SDS✨!\n⭐️Мы будем рады доставить ваши сообщения анонимно пользователю, и владельцу телегерамм канала \"Подвал Жизни\" - Сонному⭐️\n(сообщения 100% анонимны)")


@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id == OWNER_ID and message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        if replied_id in message_map:
            target_id = message_map[replied_id]
            await bot.send_message(
                target_id,
                f"{message.text}"
            )
            await message.answer("✅ Ответ отправлен.")
        return
    if message.from_user.id != OWNER_ID:
        sent = await bot.send_message(
            OWNER_ID,
            f"{message.text}"
        )
        message_map[sent.message_id] = message.from_user.id
async def main():
    await dp.start_polling(bot)

asyncio.run(main())