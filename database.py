import aiosqlite

async def init_db():
    async with aiosqlite.connect("bookings.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                service TEXT NOT NULL,
                time TEXT NOT NULL,
                user_id INTEGER
            )
        """)
        await db.commit()

async def save_booking(name, service, time, user_id):
    async with aiosqlite.connect("bookings.db") as db:
        await db.execute(
            "INSERT INTO bookings (name, service, time, user_id) VALUES (?, ?, ?, ?)",
            (name, service, time, user_id)
        )
        await db.commit()

async def get_all_books():
    async with aiosqlite.connect("bookings.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM bookings") as cursor:
            rows = await cursor.fetchall()
            return rows
