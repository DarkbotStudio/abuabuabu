from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command
import config
from procfiles import db,nsfwdetector

router = Router()

brawlers = config.brawlers
countries = config.countries

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Handler /start command"""
    user_id = msg.from_user.id
    if await db.is_user_in_db(user_id):
        def calculate_rank(popularity):
            if 0 == popularity <= 99:
                return 'D'
            elif 100 <= popularity <= 999:
                return 'C'
            elif 1000 <= popularity <= 9999:
                return 'B'
            elif 10000 <= popularity <= 99999:
                return 'A'
            elif 100000 <= popularity <= 999999:
                return 'S'
            elif popularity >= 1000000:
                return 'S+'
        data = await db.load_user_data(user_id)
        menu_btns = [
            [
                types.InlineKeyboardButton(text=f'{"🔍 Найти флуд" if data[2] is None else "🧑 Мой флуд"}', callback_data=f'{"search_flood" if data[2] is None else "my_flood"}')
            ],
            [
                types.InlineKeyboardButton(text="👥 Флуды", callback_data="floods"),
                types.InlineKeyboardButton(text="🔝 Топ флудов", callback_data="top_floods")
             ],
            [
                types.InlineKeyboardButton(text="📒 Мой профиль", callback_data="my_profile"),
                types.InlineKeyboardButton(text="🆘 Помощь", callback_data="help")
            ],
            [
                types.InlineKeyboardButton(text="⚙ Настройки", callback_data="settings"),
                types.InlineKeyboardButton(text="ℹ Информация", callback_data="info")
            ]
        ]
        menu = types.InlineKeyboardMarkup(inline_keyboard=menu_btns)
        await msg.answer(f"С возращением, {msg.from_user.full_name}!\n"
                         f"Вот твой профиль:\n"
                         f"🆔 ID: {user_id}\n"
                         f"📒 Имя: {data[1]}\n"
                         f"👥 В флуде: {'да' if data[2] is not None else 'нет'}\n"
                         f"📈 Ранг: {calculate_rank(data[10])} ({data[10]})", reply_markup=menu)
    else:
        await msg.answer(f"Привет, {msg.from_user.full_name}!\n"
                         f"Давно хотел вступить в флуд но не можешь найти подходящий?\n"
                         f"Или может хотел даже создать свой но в него никто не заходит?\n"
                         f"Не беда! Saturn Flood Bot был создан для таких ситуаций!\n"
                         f"Здесь ты найдешь сотни флудов которые с радостью примут тебя к себе\n"
                         f"Но не забывай что у каждого флуда есть свои правила за нарушение которых можно и получить по попе)\n"
                         f'Перед регистрацией ознакомься с <a href="https://teletype.in/@saturnfloodowner/BotData">данными которые сохраняет бот</a> и зарегистрируйся командой /reg [имя] [возраст] [страна] [персонаж из Brawl Stars (имя)]\n'
                         f'\n\nПосле регистрации мы будем считать что вы ознакомились с <a href="https://teletype.in/@saturnfloodowner/BotData">данными которые сохраняет бот</a>', disable_web_page_preview=True)

@router.message(Command("reg"))
async def reg_handler(msg: Message):
    """Handle /reg command and register user"""
    user_id = msg.from_user.id
    if await db.is_user_in_db(user_id):
        await msg.answer("Вы уже зарегистрированы!\n"
                         "Напишите /start чтобы открыть меню")
    else:
        def extract_data(text):
            return text.split() if len(text.split()) > 1 else None
        data = extract_data(msg.text)
        if data:
            name = str(data[1]).capitalize()
            age = data[2]
            country = data[3]
            role = data[4]
            if country in countries:
                if role in brawlers:
                    await db.register_user(user_id, name, None, None, age, country, None)
                    await msg.answer("Регистрация успешна!\n"
                                     "Напишите /start еще раз чтобы открыть меню")
                else: await msg.answer("Не удалось зарегистрироваться, проверьте правильность написания своей роли (посмотрите в игре как пишется имя вашего бравлера)")
            else: await msg.answer("Не удалось зарегистрироваться, проверьте правильность написания вашей страны.\n"
                                   "Или может вы придумали новую страну?🤨")
        else: await msg.answer("Не удалось зарегистрироваться, возможно вы ввели не все данные")
