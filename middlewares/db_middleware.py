from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db import Database

db = Database("main_database.db")


class DbMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Har qanday xabar kelganda jadvalni tekshirish
        await db.create_table()

        user_id = message.from_user.id
        full_name = message.from_user.full_name

        # Foydalanuvchi bazada bormi yoki yo'qligini tekshirib, yo'q bo'lsa qo'shadi
        await db.add_user(user_id=user_id, name=full_name)