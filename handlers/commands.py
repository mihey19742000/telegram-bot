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
