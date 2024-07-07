import flag
from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import config
from procfiles import db,nsfwdetector,procfile



router = Router()

brawlers = config.brawlers
countries = config.countries

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Handler /start command"""
    user_id = msg.from_user.id
    if await db.is_user_in_db(user_id):
        data = await db.load_user_data(user_id)
        menu_btns = [
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
                         f"📈 Ранг: {procfile.calculate_rank(data[10])} ({data[10]})", reply_markup=menu)
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
        data = procfile.extract_data(msg.text)
        if data:
            name = str(data[1]).capitalize()
            age = data[2]
            country = str(data[3]).capitalize()
            role = str(data[4]).capitalize()
            if country in countries:
                if role in brawlers:
                    await db.register_user(user_id, name, None, None, age, country, None)
                    await msg.answer("Регистрация успешна!\n"
                                     "Напишите /start еще раз чтобы открыть меню")
                else: await msg.answer("Не удалось зарегистрироваться, проверьте правильность написания своей роли (посмотрите в игре как пишется имя вашего бравлера)")
            else: await msg.answer("Не удалось зарегистрироваться, проверьте правильность написания вашей страны.\n"
                                   "Или может вы придумали новую страну?🤨")
        else: await msg.answer("Не удалось зарегистрироваться, возможно вы ввели не все данные")

@router.callback_query(F.data == "floods")
async def floods_menu_handler(call: CallbackQuery):
    kb = [
        [
            types.InlineKeyboardButton(text="🔍 Найти флуд", callback_data="search_flood")
        ],
        [
            types.InlineKeyboardButton(text="➕ Создать флуд", callback_data="create_flood")
        ]
    ]
    menu = types.InlineKeyboardMarkup(inline_keyboard=kb)
    try:
        await call.message.edit_text("В этом меню вы можете создать или найти флуд:", reply_markup=menu)
    except:
        await call.message.answer("В этом меню вы можете создать или найти флуд:", reply_markup=menu)
@router.callback_query(F.data == "search_flood")
async def search_flood_handler(call: CallbackQuery):
    user_id = call.from_user.id
    user_filters = await db.get_user_filters(user_id)
    search_flood_btns = [
        [types.InlineKeyboardButton(text="🔍 Найти флуд", callback_data="search_flood_start")],
        [types.InlineKeyboardButton(text=f"Моя роль свободная {'✅' if user_filters[2] == 1 else '❌'}",
                                    callback_data="filters_switch_role_free"),
         types.InlineKeyboardButton(text=f"Включен Saturn Protect {'✅' if user_filters[6] == 1 else '❌'}",
                                    callback_data="filters_switch_saturn_protect_on")],
        [types.InlineKeyboardButton(text=f"Норма сообщений в неделю: {user_filters[5]}",
                                    callback_data="filters_switch_norma")],
        [
            types.InlineKeyboardButton(text=f"Регион 1: {flag.flag(user_filters[3])}",
                                       callback_data="filters_switch_region_1"),
            types.InlineKeyboardButton(text=f"Регион 2: {flag.flag(user_filters[4])}",
                                       callback_data="filters_switch_region_2")
        ]
    ]

    search_flood_markup = types.InlineKeyboardMarkup(inline_keyboard=search_flood_btns)
    try:
        await call.message.edit_text("В этом меню в с легкостью найдете флуд\n"
                                  "А в фильтрах настроить все по своему вкусу чтобы вам попался именно тот флуд, который вам нужно!", reply_markup=search_flood_markup)
    except:
        await call.message.answer("В этом меню в с легкостью найдете флуд\n"
                                  "А в фильтрах настроить все по своему вкусу чтобы вам попался именно тот флуд, который вам нужно!", reply_markup=search_flood_markup)

@router.callback_query(F.data.startwith == "filters_")
async def change_filters_handler(call: CallbackQuery):
    user_id = call.from_user.id
    params = call.data.replace("filters_", "")
    user_filters = await db.get_user_filters(user_id)
    if params == "switch_role_free":
        await db.update_user_filter(user_id, "user_role_free", 0 if user_filters[2] == 1 else 1)
    elif params == "switch_saturn_protect_on":
        await db.update_user_filter(user_id, "saturn_protect_on", 0 if user_filters[6] == 1 else 1)
    elif params ==