import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from INFO import BOT_TOKEN, CHANNEL_ID, ADMIN_IDS
from tugmalar import ADMIN_PANEL, TUGMA, TUGMA_STOP, test
from tugmalar import XABAR, XABAR_STOP, BUYRUQ, BUYRUQ_STOP


print(test)

CHANNEL_ID = CHANNEL_ID
ADMIN_ID = ADMIN_IDS
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Database connections
conn_xabarlar = sqlite3.connect("xabarlar.db")
cursor_xabarlar = conn_xabarlar.cursor()

conn_buyruqlar = sqlite3.connect("buyruqlar.db")
cursor_buyruqlar = conn_buyruqlar.cursor()

# State classes
class XabarStates(StatesGroup):
    waiting_for_keyword = State()
    waiting_for_response = State()
    waiting_for_keyword_selection = State()

class BuyruqStates(StatesGroup):
    waiting_for_keyword = State()
    waiting_for_response = State()
    waiting_for_keyword_selection = State()

# Common initialization for databases
def init_databases():
    # Xabarlar database
    cursor_xabarlar.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )
    """)
    cursor_xabarlar.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            message_id INTEGER
        )
    """)
    
    # Buyruqlar database
    cursor_buyruqlar.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )
    """)
    cursor_buyruqlar.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            message_id INTEGER
        )
    """)
    
    conn_xabarlar.commit()
    conn_buyruqlar.commit()

init_databases()

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Tugmalardan birini tanlang", reply_markup=ADMIN_PANEL)
    else:
        await message.answer("Siz admin emassiz!")

# XABARLAR HANDLERS ------------------------------------------------------
@dp.message(F.text == "📝 Xabarlar")
async def xabarlar_menu(message: types.Message):
    await message.answer("Xabarlar bo'limi", reply_markup=XABAR)

@dp.message(F.text == "➕ Xabar Qoʻshish")
async def start_adding_xabar(message: types.Message, state: FSMContext):
    await message.answer("Xabar uchun kalit so'zni kiriting:")
    await state.set_state(XabarStates.waiting_for_keyword)

@dp.message(XabarStates.waiting_for_keyword)
async def receive_xabar_keyword(message: types.Message, state: FSMContext):
    keyword = message.text.lower()
    cursor_xabarlar.execute("SELECT keyword FROM keywords WHERE keyword = ?", (keyword,))
    if cursor_xabarlar.fetchone():
        await message.answer("Bu kalit so'z allaqachon mavjud!")
        return
    
    cursor_xabarlar.execute("INSERT INTO keywords (keyword) VALUES (?)", (keyword,))
    conn_xabarlar.commit()
    await state.update_data(keyword=keyword)
    await message.answer("Endi javob xabarlarini yuboring. 'To'xtatish' tugmasini bosgunga qadar davom eting.", reply_markup=XABAR_STOP)
    await state.set_state(XabarStates.waiting_for_response)

@dp.message(XabarStates.waiting_for_response)
async def receive_xabar_response(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "❌ toʻxtatish":
        await message.answer("Xabar qo'shish yakunlandi.", reply_markup=ADMIN_PANEL)
        await state.clear()
        return
    
    data = await state.get_data()
    keyword = data.get("keyword")
    sent_message = await bot.copy_message(chat_id=CHANNEL_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    cursor_xabarlar.execute("INSERT INTO responses (keyword, message_id) VALUES (?, ?)", (keyword, sent_message.message_id))
    conn_xabarlar.commit()
    await message.answer("Javob xabari saqlandi! Yana xabar yuborishingiz mumkin yoki 'To'xtatish' tugmasini bosing.")

@dp.message(F.text == "❌ Xabarni oʻchirish")
async def start_deleting_xabar(message: types.Message, state: FSMContext):
    cursor_xabarlar.execute("SELECT keyword FROM keywords")
    keywords = [row[0] for row in cursor_xabarlar.fetchall()]
    
    if not keywords:
        await message.answer("Hech qanday kalit so'z mavjud emas!")
        return
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=kw)] for kw in keywords],
        resize_keyboard=True
    )
    await message.answer("O'chirmoqchi bo'lgan kalit so'zni tanlang:", reply_markup=kb)
    await state.set_state(XabarStates.waiting_for_keyword_selection)

@dp.message(XabarStates.waiting_for_keyword_selection)
async def delete_xabar_keyword(message: types.Message, state: FSMContext):
    keyword = message.text
    cursor_xabarlar.execute("DELETE FROM keywords WHERE keyword = ?", (keyword,))
    cursor_xabarlar.execute("DELETE FROM responses WHERE keyword = ?", (keyword,))
    conn_xabarlar.commit()
    await message.answer(f"'{keyword}' kalit so'zi va unga bog'liq xabarlar o'chirildi!", reply_markup=ADMIN_PANEL)
    await state.clear()

# BUYRUQLAR HANDLERS ------------------------------------------------------
@dp.message(F.text == "🤖 Buyruqlar")
async def buyruqlar_menu(message: types.Message):
    await message.answer("Buyruqlar bo'limi", reply_markup=BUYRUQ)

@dp.message(F.text == "🦾 Buyruq qoʻshish")
async def start_adding_buyruq(message: types.Message, state: FSMContext):
    await message.answer("Buyruq uchun kalit so'zni kiriting:")
    await state.set_state(BuyruqStates.waiting_for_keyword)

@dp.message(BuyruqStates.waiting_for_keyword)
async def receive_buyruq_keyword(message: types.Message, state: FSMContext):
    keyword = message.text.lower()
    cursor_buyruqlar.execute("SELECT keyword FROM keywords WHERE keyword = ?", (keyword,))
    if cursor_buyruqlar.fetchone():
        await message.answer("Bu kalit so'z allaqachon mavjud!")
        return
    
    cursor_buyruqlar.execute("INSERT INTO keywords (keyword) VALUES (?)", (keyword,))
    conn_buyruqlar.commit()
    await state.update_data(keyword=keyword)
    await message.answer("Endi javob xabarlarini yuboring. 'To'xtatish' tugmasini bosgunga qadar davom eting.", reply_markup=BUYRUQ_STOP)
    await state.set_state(BuyruqStates.waiting_for_response)

@dp.message(BuyruqStates.waiting_for_response)
async def receive_buyruq_response(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "🚫 toʻxtatish":
        await message.answer("Buyruq qo'shish yakunlandi.", reply_markup=ADMIN_PANEL)
        await state.clear()
        return
    
    data = await state.get_data()
    keyword = data.get("keyword")
    sent_message = await bot.copy_message(chat_id=CHANNEL_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    cursor_buyruqlar.execute("INSERT INTO responses (keyword, message_id) VALUES (?, ?)", (keyword, sent_message.message_id))
    conn_buyruqlar.commit()
    await message.answer("Javob xabari saqlandi! Yana xabar yuborishingiz mumkin yoki 'To'xtatish' tugmasini bosing.")

@dp.message(F.text == "👾 Buyruqni oʻchirish")
async def start_deleting_buyruq(message: types.Message, state: FSMContext):
    cursor_buyruqlar.execute("SELECT keyword FROM keywords")
    keywords = [row[0] for row in cursor_buyruqlar.fetchall()]
    
    if not keywords:
        await message.answer("Hech qanday kalit so'z mavjud emas!")
        return
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=kw)] for kw in keywords],
        resize_keyboard=True
    )
    await message.answer("O'chirmoqchi bo'lgan kalit so'zni tanlang:", reply_markup=kb)
    await state.set_state(BuyruqStates.waiting_for_keyword_selection)

@dp.message(BuyruqStates.waiting_for_keyword_selection)
async def delete_buyruq_keyword(message: types.Message, state: FSMContext):
    keyword = message.text
    cursor_buyruqlar.execute("DELETE FROM keywords WHERE keyword = ?", (keyword,))
    cursor_buyruqlar.execute("DELETE FROM responses WHERE keyword = ?", (keyword,))
    conn_buyruqlar.commit()
    await message.answer(f"'{keyword}' kalit so'zi va unga bog'liq xabarlar o'chirildi!", reply_markup=ADMIN_PANEL)
    await state.clear()

# COMMON HANDLERS ------------------------------------------------------
@dp.message(Command("start"))
async def start(message: types.Message):
    start_param = message.text.split(' ')[-1]
    user_id = message.from_user.id
    
    # Check in buyruqlar database first
    cursor_buyruqlar.execute("SELECT message_id FROM responses WHERE keyword = ?", (start_param,))
    results = cursor_buyruqlar.fetchall()
    
    if not results:
        # Check in xabarlar database if not found
        cursor_xabarlar.execute("SELECT message_id FROM responses WHERE keyword = ?", (start_param,))
        results = cursor_xabarlar.fetchall()
    
    if results:
        for result in results:
            await bot.copy_message(chat_id=user_id, from_chat_id=CHANNEL_ID, message_id=result[0])
    else:
        await bot.send_message(user_id, "Salom")

@dp.message()
async def handle_message(message: types.Message):
    text = message.text
    
    # Handle buyruqlar
    cursor_buyruqlar.execute("SELECT keyword FROM keywords")
    buyruq_keywords = [row[0] for row in cursor_buyruqlar.fetchall()]
    for keyword in buyruq_keywords:
        if keyword == text:
            cursor_buyruqlar.execute("SELECT message_id FROM responses WHERE keyword = ?", (keyword,))
            results = cursor_buyruqlar.fetchall()
            for result in results:
                await bot.copy_message(chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=result[0])
    
    # Handle xabarlar
    cursor_xabarlar.execute("SELECT keyword FROM keywords")
    xabar_keywords = [row[0] for row in cursor_xabarlar.fetchall()]
    for keyword in xabar_keywords:
        if keyword in text:
            cursor_xabarlar.execute("SELECT message_id FROM responses WHERE keyword = ?", (keyword,))
            results = cursor_xabarlar.fetchall()
            for result in results:
                await bot.copy_message(chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=result[0])

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
