from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import dp, bot
from data.config import ADMINS
from utils.db import Database
import asyncio
from filters.admin_filter import AdminFilter
from filters.private_filter import  IsPrivate

# Ma'lumotlar bazasi ob'ekti
db = Database("main_database.db")


class AdminReklama(StatesGroup):
    reklama_holati = State()
    tasdiqlash_holati = State()


# 1. Admin panel va Statistika
@dp.message_handler(IsPrivate(), text=["Reklama", 'Admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMINS:
        await db.create_table()
        u_count = await db.count_users()
        g_count = await db.count_groups()  # Guruhlar sonini olish

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text="📢 Reklama yuborish", callback_data="reklama_boshlash"),
            types.InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main")
        )
        await message.answer(
            f"📊 <b>Statistika</b>\n\n"
            f"👤 Foydalanuvchilar: {u_count} ta\n"
            f"👥 Guruhlar: {g_count} ta",
            parse_mode='html',
            reply_markup=markup
        )


# 2. Asosiy menyuga qaytish
@dp.callback_query_handler(text="back_to_main", state="*")
async def back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Asosiy menyuga qaytdingiz")
    try:
        await state.finish()
    except KeyError:
        await state.set_state(None)
    await call.answer()


# 3. Reklama yozish bosqichi
@dp.callback_query_handler(text="reklama_boshlash", state="*")
async def start_reklama(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.answer("Reklama xabarini yuboring (Matn, Rasm, Video yoki Post):")
        await AdminReklama.reklama_holati.set()
        await call.answer()


# 4. Preview (Ko'zdan kechirish)
@dp.message_handler(state=AdminReklama.reklama_holati, content_types=types.ContentTypes.ANY)
async def preview_reklama(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        # Xabar ID sini saqlab qolamiz
        await state.update_data(msg_id=message.message_id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text="✅ Yuborish", callback_data="yuborish_tasdiq"),
            types.InlineKeyboardButton(text="❌ Bekor qilish", callback_data="yuborish_bekor")
        )

        await message.answer("<b>Yuqoridagi xabarni barcha foydalanuvchilar va guruhlarga yuborasizmi?</b>",
                             parse_mode='html',
                             reply_markup=markup)
        await AdminReklama.tasdiqlash_holati.set()


# 5. Yuborishni tasdiqlash va Tarqatish
@dp.callback_query_handler(text="yuborish_tasdiq", state=AdminReklama.tasdiqlash_holati)
async def confirm_broadcast(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("msg_id")

    # Bazadan barcha foydalanuvchilar va guruhlarni olish
    users = await db.get_all_users()
    groups = await db.get_all_groups()

    # Hammasini bitta ro'yxatga jamlaymiz
    all_targets = users + groups

    count, error = 0, 0
    await call.message.edit_text("🚀 Reklama tarqatilmoqda...")

    for target in all_targets:
        try:
            # target[0] bu user_id yoki group_id (jadvalda 1-ustun)
            await bot.copy_message(
                chat_id=target[0],
                from_chat_id=call.from_user.id,
                message_id=msg_id
            )
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            error += 1

    await call.message.delete()
    await call.message.answer(
        f"✅ <b>Yuborildi:</b> {count}\n❌ <b>Bloklagan/Xato:</b> {error}",
        parse_mode='html',
    )

    try:
        await state.finish()
    except KeyError:
        await state.set_state(None)

    await call.answer()


# 6. Bekor qilish
@dp.callback_query_handler(text="yuborish_bekor", state=AdminReklama.tasdiqlash_holati)
async def cancel_broadcast(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Reklama bekor qilindi.")
    try:
        await state.finish()
    except KeyError:
        await state.set_state(None)

    await call.answer()

