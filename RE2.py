import asyncio
import random
import string
from datetime import datetime
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = "8424047844:AAHwgJHoqxytQGYX2Z6QAV63RHaUrk3BHIo"
BASE_GROUP_LINK = "https://t.me/RE2CSARM"
ADMIN_ID = 8043927309

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_data = {}

def generate_random_suffix(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_data[message.from_user.id] = {
        'step': 'get_nick',
        'name': message.from_user.full_name,
        'username': message.from_user.username,
        'id': message.from_user.id,
        'joined': False,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    await message.answer(
        "👋 SALOM! SIZ RE2 NING RASMIY BOTIGA KELDINGIZ.\n\n💬 Iltimos, CS 1.6’dagi nickname’ingizni yozing:"
    )

@dp.message(F.text)
async def get_nick(message: types.Message):
    step = user_data.get(message.from_user.id, {}).get('step')
    if step == 'get_nick':
        user_data[message.from_user.id]['nickname'] = message.text
        user_data[message.from_user.id]['step'] = 'confirm_re2'

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ Qoydim")]],
            resize_keyboard=True
        )

        await message.answer(
            f"✅ Endi nickname’ingizning boshiga `RE2 | ` qo‘shing.\nMisol: `RE2 | {message.text}`\n\n📸 Skreen yuboring yoki \"Qoydim\" tugmasini bosing.",
            reply_markup=kb
        )
        return

    if step == 'confirm_re2' and message.text == "✅ Qoydim":
        await send_admin_info(message)
        await send_group_link(message)

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    step = user_data.get(message.from_user.id, {}).get('step')
    if step == 'confirm_re2':
        await send_admin_info(message)
        await send_group_link(message)

async def send_group_link(message: types.Message):
    suffix = generate_random_suffix()
    full_link = f"{BASE_GROUP_LINK}?ref={suffix}"

    await message.answer(
        f"🎉 Ajoyib! Hammasi tayyor!\n\n🔗 Guruhga qo‘shilish uchun havola:\n{full_link}",
        reply_markup=ReplyKeyboardRemove()
    )
    user_data.pop(message.from_user.id, None)

async def send_admin_info(message: types.Message):
    data = user_data[message.from_user.id]
    text = (
        f"📥 Yangi foydalanuvchi botdan to‘liq foydalanmoqda:\n\n"
        f"👤 Ismi: {data['name']}\n"
        f"🔗 Username: @{data['username'] if data['username'] else 'yo‘q'}\n"
        f"🆔 ID: {data['id']}\n"
        f"🎮 Nick: {data['nickname']}\n"
        f"🕒 Vaqt: {data['time']}\n"
        f"✅ Link oldi"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=text)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
