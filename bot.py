import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from INFO import BOT_TOKEN, ADMIN_IDS,TEST
print(TEST)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    
    await message.answer("Assalomu alaykum! Botimizga xush kelibsiz!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
