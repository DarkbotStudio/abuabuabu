from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from procfiles import db, config, main, keyboards

router = Router()

brawlers = config.brawlers
countries = config.countries
cis_regions = config.cis_country_codes

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Handler /start command"""
    user_id = msg.from_user.id
    if await db.is_user_in_db(user_id):
        await msg.answer(await main.start_in_db_func(user_id, msg), reply_markup=keyboards.create_start())
    else:
        await msg.answer(await main.start_func(msg), disable_web_page_preview=True)

@router.message(Command("reg"))
async def reg_handler(msg: Message):
    """Handle /reg command and register user"""
    user_id = msg.from_user.id
    await msg.answer(await main.reg_func(user_id, msg))

async def display_flood_menu(call: CallbackQuery):
    menu = await keyboards.create_floods_menu(call.from_user.id)
    message_text = await main.flood_menu_text_func()
    try:
        await call.message.edit_text(message_text, reply_markup=menu)
    except:
        await call.message.answer(message_text, reply_markup=menu)

@router.callback_query(F.data == "search_flood")
async def search_flood_handler(call: CallbackQuery):
    user_id = call.from_user.id
    search_flood_markup = await keyboards.create_floods_menu(user_id)
    try:
        await call.message.edit_text(await main.flood_menu_text_func(), reply_markup=search_flood_markup)
    except:
        await call.message.answer(await main.flood_menu_text_func(), reply_markup=search_flood_markup)


@router.callback_query(F.data.startswith("filters_"))
async def change_filters_handler(call: CallbackQuery):
    user_id = call.from_user.id
    params = call.data.replace("filters_", "")
    message_text, reply_markup = await main.filters_func(user_id, params)

    if message_text and reply_markup:
        await call.message.edit_text(message_text, reply_markup=reply_markup)
