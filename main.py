import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiohttp import web

# ⚙️ SOZLAMALAR
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OMMAVIY_KANAL = "@ingiliz_turnir" 
KANAL_LINK = "https://t.me/ingiliz_turnir"
KARTA_RAQAM = "5614 6820 1716 6317"
KARTA_E_SOHIBI = "Muxammadiyeva Dilafruz"
ADMIN_USERNAME = "Obidjonovich_11"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔍 Kanalga a'zolikni tekshiruvchi funksiya
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=OMMAVIY_KANAL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# === /START BUYRUG'I ===
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    if not is_subscribed:
        text = (
            f"❌ *Kechirasiz, botdan foydalanishdan oldin rasmiy kanalimizga a'zo bo'lishingiz kerak!*\n\n"
            f"Pastdagi tugma orqali kanalimizga obuna bo'ling va keyin **'Obunani tekshirish 🔄'** tugmasini bosing:"
        )
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=KANAL_LINK)],
            [types.InlineKeyboardButton(text="Obunani tekshirish 🔄", callback_data="check_sub")]
        ])
        await message.answer(text, parse_mode="Markdown", reply_markup=markup)
    else:
        await send_payment_details(message)

# === OBUNANI TEKSHIRISH CALLBACK ===
@dp.callback_query(F.data == "check_sub")
async def check_callback(call: types.CallbackQuery):
    if await check_subscription(call.from_user.id):
        await call.answer("✅ Rahmat! Obuna tasdiqlandi.", show_alert=False)
        await call.message.delete()
        await send_payment_details(call.message)
    else:
        await call.answer("❌ Siz hali kanalga a'zo bo'lmadingiz!", show_alert=True)

# === TO'LOV MATNINI YUBORISH ===
async def send_payment_details(message: types.Message):
    text = (
        f"🎉 *TABRIKLAYMIZ, {message.from_user.first_name.upper()}! RASMIY KANALIMIZGA OBUNA TASDIQLANDI!* 🎉\n\n"
        f"🚀 *Siz ingliz tili bo'yicha eng hayajonli 'WINNER TURNIRI' eshigiga yetib keldingiz!*\n"
        f"Bu shunchaki oddiy test emas — bu ham bilimingizni oshirish, ham haqiqiy pul mukofotini qo'lga kiritish imkoniyatidir! 💰\n\n"
        f"🛡 *TURNIR SHARTLARI VA QOIDALARI:* \n"
        f"🔹 Turnir umumiy **200 ta ishtirokchi** yig'ilgandan so'ng maxsus yopiq kanalda start oladi.\n"
        f"🔹 Savollar barcha uchun teng va adolatli vaqtda yuboriladi.\n"
        f"🔹 Eng tez va eng ko'p to'g'ri javob bergan **TOP-10 talik g'oliblar** aniqlanadi!\n\n"
        f"🎁 *YUTUQ FONDI:* \n"
        f"🥇 1-o'rindan 🏅 10-o'ringacha bo'lgan barcha g'oliblarga **200 000 so'mdan** jami **2 000 000 so'm** naqd pul mukofoti kafolatlanadi! 💸\n\n"
        f"⚙️ *TURNIRGA KIRISH BADALI:* \n"
        f"💵 Turnirda qatnashish narxi: `15 000 so'm` \n"
        f"💳 To'lov uchun karta raqam: `{KARTA_RAQAM}`\n"
        f"👤 Karta egasi: *{KARTA_E_SOHIBI}*\n\n"
        f"📸 *KEYINGI QADAM (MUHIM):* \n"
        f"To'lovni amalga oshirganingizdan so'ng, chekni (skrinshotini) pastdagi tugma orqali srazu adminga yuboring.\n\n"
        f"🔥 O'z bilimingizga ishoning va g'oliblar qatoridan joy oling!"
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⚡️ Chekni Adminga Yuborish ⚡️", url=f"tg://resolve?domain={ADMIN_USERNAME}")]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=markup)

# === RENDER UCHUN HTTP SERVER VA BOTNI ISHGA TUSHIRISH ===
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
