from aiogram import executor
from middlewares.db_middleware import DbMiddleware
from loader import dp

import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    dp.middleware.setup(DbMiddleware())
    executor.start_polling(dp, on_startup=on_startup)