import aiosqlite
from datetime import datetime
import config

async def is_user_in_db(user_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        if user: return True
        else: return False

async def register_user(user_id: int, name: str, flood_id: int or None, personal_flood_id: int or None, age: int, country: str, phone_number: str or None, status: str = "user", banned: int = 0, popularity = 0):
    async with aiosqlite.connect(config.DB_PATH) as db:
        register_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        query = """
        INSERT INTO users (id, name, flood_id, personal_flood_id, age, country, register_date, status, banned, phone_number, popularity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        await db.execute(query, (user_id, name, flood_id, personal_flood_id, age, country, register_date, status, banned, phone_number, popularity))
        await db.commit()
async def load_user_data(user_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        query = """
        SELECT * FROM users WHERE id = ?
        """
        cursor = await db.execute(query, (user_id,))
        user_data = await cursor.fetchone()
        return user_data if user_data else None
