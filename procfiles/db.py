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
        query2 = """
        INSERT INTO user_filters (id, age_category, user_role_free, region1, region2, norma_msg)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        await db.execute(query2, (user_id, 0, 1, "RU", "UA", 100))
        await db.commit()
async def load_user_data(user_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        query = """
        SELECT * FROM users WHERE id = ?
        """
        cursor = await db.execute(query, (user_id,))
        user_data = await cursor.fetchone()
        return user_data if user_data else None
async def get_flood_info(flood_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM floods WHERE id = ?", (flood_id,))
        data = await cursor.fetchone()
        return data
async def get_user_filters(user_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM user_filters WHERE id = ?", (user_id,))
        data = await cursor.fetchone()
        return data
async def update_user_filter(user_id, filter_, new_filter):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(f"UPDATE user_filters SET {filter_} = ? WHERE id = ?", (new_filter, user_id))
        await db.commit()