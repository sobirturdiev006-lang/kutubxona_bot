import aiosqlite

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Foydalanuvchilar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    contact TEXT
                )
            """)
            # Guruhlar jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id BIGINT PRIMARY KEY,
                    title TEXT
                )
            """)
            await db.commit()

    async def get_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def add_user(self, user_id, name):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )
            await db.commit()

    async def add_group(self, group_id, title):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO groups (group_id, title) VALUES (?, ?)",
                (group_id, title)
            )
            await db.commit()

    async def get_all_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users") as cursor:
                return await cursor.fetchall()

    async def get_all_groups(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM groups") as cursor:
                return await cursor.fetchall()

    async def count_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    async def update_user_info(self, user_id: int, name: str = None, email: str = None, contact: str = None):
        """
        users jadvalidagi name/email/contact ni yangilaydi.
        Qaysi maydon berilsa, o‘sha update bo‘ladi.
        """
        fields = []
        values = []

        if name is not None:
            fields.append("name = ?")
            values.append(name)

        if email is not None:
            fields.append("email = ?")
            values.append(email)

        if contact is not None:
            fields.append("contact = ?")
            values.append(contact)

        if not fields:
            return  # update qiladigan narsa yo‘q

        values.append(user_id)

        sql = f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?"

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql, tuple(values))
            await db.commit()

    async def count_groups(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM groups") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0