import sqlite3
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from INFO import BOT_TOKEN, ADMIN_IDS


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasi bilan ishlash
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Users jadvalini yaratish
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                (user_id INTEGER PRIMARY KEY)''')
conn.commit()

# /start komandasi uchun handler
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    
    # Bazaga user_id ni qo'shamiz (agar mavjud bo'lmasa)
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    
    await message.answer("Assalomu alaykum! Botimizga xush kelibsiz!")

# Admin panel uchun handler
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Sizga ruxsat berilmagan!")
        return
    
    # Tugma yaratish
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika")]
        ],
        resize_keyboard=True
    )
    await message.answer("Admin panel", reply_markup=keyboard)

# Statistika tugmasi uchun handler
@dp.message(F.text == "📊 Statistika")
async def show_stats(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Sizga ruxsat berilmagan!")
        return
    
    # Userlar sonini hisoblash
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    await message.answer(f"Jami foydalanuvchilar soni: {count} ta")

# Agar boshqa xabarlar bo'lsa
@dp.message()
async def other_messages(message: types.Message):
    await message.answer("Iltimos, buyruqlardan foydalaning!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)