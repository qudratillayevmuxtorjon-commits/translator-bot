import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from deep_translator import GoogleTranslator

# Siz taqdim etgan bot tokeni
TOKEN = "7980627399:AAG_boDGBBnHR4rfWFaw5Y6I3QTCmOOM_Q8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchilarning tanlagan tilini saqlash uchun lug'at (default: o'zbek tili 'uz')
user_languages = {}

# Tillarni tanlash uchun inline tugmalar menyusi
def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ]
    ])
    return keyboard

# /start buyrug'i uchun handler
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_languages:
        user_languages[user_id] = "uz"  # Boshlang'ich til — o'zbek tili
        
    await message.answer(
        f"Salom, {message.from_user.full_name}! 🌐\n\n"
        "Menga istalgan tilda matn yuboring, men uni siz tanlagan tilga tarjima qilib beraman.\n"
        "Kerakli tarjima tilini o'zgartirish uchun quyidagi tugmalardan birini bosing:",
        reply_markup=get_language_keyboard()
    )

# Tugmalar bosilganda ishlaydigan callback handler
@dp.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # lang_uz -> 'uz', lang_ru -> 'ru', lang_en -> 'en'
    selected_lang = callback.data.split("_")[1]
    
    user_languages[user_id] = selected_lang
    
    lang_names = {
        "uz": "🇺🇿 O'zbekcha",
        "ru": "🇷🇺 Ruscha",
        "en": "🇬🇧 Inglizcha"
    }
    
    await callback.message.answer(f"✅ Tarjima tili **{lang_names[selected_lang]}** ga o'zgartirildi! Endi istalgan matnni yuborishingiz mumkin.")
    await callback.answer()

# Matnli xabarlarni tarjima qilish handleri
@dp.message()
async def translate_handler(message: types.Message):
    user_id = message.from_user.id
    # Agar foydalanuvchi til tanlamagan bo'lsa, avtomatik 'uz' tanlanadi
    target_lang = user_languages.get(user_id, "uz")
    
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        await message.reply(
            f"🔤 **Tarjima ({target_lang.upper()}):**\n\n{translated_text}",
            reply_markup=get_language_keyboard() # Har bir javob tagida ham tilni o'zgartirish tugmasi chiqadi
        )
    except Exception as e:
        await message.reply("Kechirasiz, tarjima qilishda xatolik yuz berdi.")

# Botni ishga tushirish
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Tarjimon bot ishga tushdi va ulanishni kutmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
