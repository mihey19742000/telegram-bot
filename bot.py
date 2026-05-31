# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.commands import router as commands_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    dp.include_router(commands_router)
    
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
# config.py
BOT_TOKEN = "8739772484:AAGos9Ji601eSYTGY7PNSUbEsnJTuxUneys"

# Платёжные реквизиты (все данные хранятся в текстах)
# Здесь только технические настройки

# ID админа для уведомлений (опционально)
ADMIN_ID = 6267777706  # замените на свой Telegram ID

# Файл для хранения статистики сборов
STATS_FILE = "donate_stats.json"
# handlers/commands.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from texts.content import (
    START_MESSAGE, ABOUT_PROJECT, DONATE_INFO, 
    HELP_MESSAGE, DONATE_METHODS, DONATE_THANK_YOU,
    DONATE_CONFIRMATION_REQUEST
)
from keyboards.inline import (
    main_menu_keyboard, donate_methods_keyboard, back_to_main_keyboard
)

router = Router()

# ===== КОМАНДЫ =====

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=main_menu_keyboard()
    )

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        ABOUT_PROJECT,
        reply_markup=back_to_main_keyboard()
    )

@router.message(Command("donate"))
async def cmd_donate(message: Message):
    await message.answer(
        DONATE_INFO,
        reply_markup=donate_methods_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_MESSAGE)

# ===== CALLBACK-ОБРАБОТЧИКИ =====

@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery):
    await callback.message.edit_text(
        ABOUT_PROJECT,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "donate")
async def cb_donate(callback: CallbackQuery):
    await callback.message.edit_text(
        DONATE_INFO,
        reply_markup=donate_methods_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery):
    await callback.message.edit_text(
        HELP_MESSAGE,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def cb_back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        START_MESSAGE,
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("donate_method_"))
async def cb_donate_method(callback: CallbackQuery):
    """Показывает реквизиты выбранного способа"""
    index = int(callback.data.split("_")[-1])
    
    if index < len(DONATE_METHODS):
        method = DONATE_METHODS[index]
        text = method["text"] + "\n" + DONATE_CONFIRMATION_REQUEST
        
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Я перевёл", callback_data="donate_confirm")],
                [InlineKeyboardButton(text="🔙 К способам", callback_data="donate")],
            ])
        )
    await callback.answer()

@router.callback_query(F.data == "donate_confirm")
async def cb_donate_confirm(callback: CallbackQuery):
    """Подтверждение перевода"""
    await callback.message.edit_text(
        DONATE_THANK_YOU,
        reply_markup=back_to_main_keyboard()
    )
    
    # Здесь можно добавить уведомление админу
    # await callback.bot.send_message(ADMIN_ID, f"Новый донат от @{callback.from_user.username}")
    
    await callback.answer("Спасибо! Ваша поддержка учтена.", show_alert=True)

# Не забудьте импорт в конце
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.content import DONATE_METHODS

def main_menu_keyboard():
    """Главное меню под сообщением /start"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 О проекте", callback_data="about")],
        [InlineKeyboardButton(text="💰 Поддержать", callback_data="donate")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
    ])

def donate_methods_keyboard():
    """Клавиатура выбора способа доната"""
    buttons = []
    for i, method in enumerate(DONATE_METHODS):
        buttons.append([
            InlineKeyboardButton(
                text=method["name"],
                callback_data=f"donate_method_{i}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(text="✅ Я перевёл", callback_data="donate_confirm")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_main_keyboard():
    """Кнопка возврата в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")]
    ])
# texts/content.py

# ===== ОСНОВНЫЕ ТЕКСТЫ БОТА =====

START_MESSAGE = """
🌟 <b>Лаборатория Биоритмов | Проект «Резонанс»</b>

Приветствую! Я бот для поддержки исследований в области биоритмологии и полевых структур организма.

Мы работаем над созданием методов, позволяющих гармонизировать внутренние ритмы человека и оптимизировать взаимодействие с тонкополевыми структурами.

Используйте кнопки меню для навигации.
"""

ABOUT_PROJECT = """
🔬 <b>О проекте «Резонанс»</b>

<blockquote>Человек — это не только биохимия. Это сложная колебательная система, где каждый орган имеет свою частоту, а организм в целом формирует единое поле.</blockquote>

<b>Наши направления исследований:</b>

• 🧬 <b>Биоритмологическая коррекция</b>
  Изучение циркадианных, ультрадианных и инфрадианных ритмов. Разработка протоколов синхронизации внутренних часов организма с природными циклами.

• ⚡ <b>Полевые структуры организма</b>
  Исследование биофотонной эмиссии, электромагнитного каркаса клеток и тканей. Поиск способов неинвазивной диагностики через регистрацию полей.

• 🌊 <b>Волновые методы взаимодействия</b>
  Технологии низкоинтенсивного резонансного воздействия: акустического, электромагнитного, светового. Без химии. Без вторжения.

• 🧘 <b>Интеграция с телесными практиками</b>
  Соединение научных данных с опытом цигун, йоги, дыхательных техник. Создание моста между наукой и традицией.

<b>Почему это важно?</b>
Хронический стресс, нарушение сна, десинхроноз — бич современного мира. Мы ищем методы мягкой перенастройки организма, работая с первопричинами, а не симптомами.
"""

DONATE_INFO = """
💰 <b>Поддержать исследования</b>

Каждое пожертвование приближает нас к важным открытиям.
Все средства направляются на:

• Лабораторное оборудование (датчики ЭЭГ, ВСР, газоразрядной визуализации)
• Разработку программного обеспечения для анализа биоритмов
• Проведение пилотных исследований с участием добровольцев
• Публикацию результатов в открытом доступе

<b>Выберите удобный способ перевода:</b>
"""

DONATE_THANK_YOU = """
🙏 <b>Благодарю за поддержку!</b>

Ваш вклад ценен не только суммой, но и вниманием к теме.
Исследования продолжаются благодаря таким людям, как вы.

Если хотите следить за ходом проекта — напишите мне в личные сообщения.
"""

HELP_MESSAGE = """
📋 <b>Доступные команды:</b>

/start — главное меню
/about — о проекте и исследованиях
/donate — поддержать проект
/help — это сообщение

По любым вопросам пишите: @BioPhotonRytm
"""

# ===== ПЛАТЁЖНЫЕ РЕКВИЗИТЫ (заполните своими данными) =====

DONATE_METHODS = [
    {
        "name": "💳 Перевод на карту (СБП)",
        "text": """
<b>Перевод на карту:</b>
<code>2202 2080 4614 8079</code>
<b>Банк:</b> Сбер Банк
<b>Получатель:</b> Mikhail Andreyev

<i>После перевода нажмите «Подтвердить перевод»</i>
"""
    },
    {
        "name": "🪙 Криптовалюта (USDT TRC20)",
        "text": """
<b>USDT (TRC20):</b>
<code>TGSfdk3BEVAqtvhF8vaNDyWWAHyhzDaXEa</code>
<i>Сеть: TRON</i>
"""
    },
    {
        "name": "📱 По номеру телефона",
        "text": """
<b>Перевод по номеру:</b>
<code>+7 949 378-30-53</code>
<i>ПСБ / Т-Банк / Озон</i>
"""
    },
]

# Текст с просьбой подтвердить донат
DONATE_CONFIRMATION_REQUEST = """
✅ Если вы сделали перевод, нажмите кнопку ниже, чтобы я учел ваш вклад в общей статистике сборов.
"""
# utils/__init__.py
# utils/stats.py
import json
import os
from datetime import datetime
from config import STATS_FILE

def load_stats():
    """Загружает статистику из JSON-файла"""
    if not os.path.exists(STATS_FILE):
        return {
            "total_donations": 0,
            "donations_count": 0,
            "history": []
        }
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_stats(stats):
    """Сохраняет статистику в JSON-файл"""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def add_donation(user_id: int, username: str, amount: float = None):
    """
    Фиксирует донат в статистике.
    amount — опционально, если сумма известна.
    """
    stats = load_stats()
    stats["total_donations"] += amount if amount else 0
    stats["donations_count"] += 1
    stats["history"].append({
        "user_id": user_id,
        "username": username,
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    })
    save_stats(stats)
    return stats
pip install aiogram
aiogram>=3.4.0