import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiohttp import web

# TOKENNI RENDER'DAN OLAMIZ
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# SIZNING ASLI KODINGIZDAGI O'ZGARUVCHILAR
OMMAVIY_KANAL = "@ingiliz_turnir" 
KANAL_LINK = "https://t.me/ingiliz_turnir"
KARTA_RAQAM = "5614 6820 1716 6317"
KARTA_E_SOHIBI = "Muxammadiyeva Dilafruz"
ADMIN_USERNAME = "Obidjonovich_11"

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=OMMAVIY_KANAL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    if not is_subscribed:
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=KANAL_LINK)],
            [types.InlineKeyboardButton(text="Obunani tekshirish 🔄", callback_data="check_sub")]
        ])
        await message.answer("❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=markup)
    else:
        await send_payment_details(message)

@dp.callback_query(F.data == "check_sub")
async def check_callback(call: types.CallbackQuery):
    if await check_subscription(call.from_user.id):
        await call.message.delete()
        await send_payment_details(call.message)
    else:
        await call.answer("❌ Hali obuna bo'lmadingiz!", show_alert=True)

async def send_payment_details(message):
    text = f"🎉 TABRIKLAYMIZ!...\n\n💳 Karta: {KARTA_RAQAM}\n👤 Egasi: {KARTA_E_SOHIBI}"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⚡️ Chekni yuborish", url=f"tg://resolve?domain={ADMIN_USERNAME}")]
    ])
    await message.answer(text, reply_markup=markup)

# RENDER UCHUN HTTP SERVER
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 10000)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
