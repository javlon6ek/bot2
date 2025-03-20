test = "Bot ishga tushdi"
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ADMIN_PANEL = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗄 Tugmalar"),KeyboardButton(text="📝 Xabarlar")],
        [KeyboardButton(text="🤖 Buyruqlar"),KeyboardButton(text="⚙️ Sozlamalar")]
    ],resize_keyboard=True)




TUGMA = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆕 Tugma qoʻshish"),KeyboardButton(text="🗑 Tugmani oʻchirish")],
        [KeyboardButton(text="🔗 Xabar biriktirish"),KeyboardButton(text="❓Savol qo'shish")],
    ],resize_keyboard=True) 
TUGMA_STOP=ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⛔️ toʻxtashish")],],resize_keyboard=True)







XABAR = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Xabar Qoʻshish")],
        [KeyboardButton(text="❌ Xabarni oʻchirish")]
    ],
    resize_keyboard=True)
XABAR_STOP=ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ toʻxtatish")],],resize_keyboard=True)







BUYRUQ = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🦾 Buyruq qoʻshish")],
        [KeyboardButton(text="👾 Buyruqni oʻchirish")]
    ],
    resize_keyboard=True)


BUYRUQ_STOP=ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚫 toʻxtatish")],],resize_keyboard=True)





ADMINLAR_UCHUN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="📨 Reklama")]
    ],
    resize_keyboard=True
)



SUPER_ADMIN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistika"),KeyboardButton(text="📨 Reklama")],
        [KeyboardButton(text="👮‍♂ Adminlar"),KeyboardButton(text="📢 Kanallar")]
    ],
    resize_keyboard=True
)
