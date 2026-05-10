from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_start_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = ["📊 Тиражи"]
    for button in buttons:
        builder.button(text=button)
    return builder.adjust(1).as_markup(resize_keyboard=True)


START_KEYBOARD = get_start_keyboard()
