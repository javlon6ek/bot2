import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command



bot = Bot(token="7930866215:AAE-IY2THlg3kQIbuwGh6eyLD9Pz1kjNdF8")
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    
    await message.answer("NAGAp")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
