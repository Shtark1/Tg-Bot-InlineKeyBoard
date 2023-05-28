from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# КНОПКИ МЕНЮ
btn_add_channel = KeyboardButton("Добавть канал")
btn_add_group = KeyboardButton("Добавть группу")
btn_view_added = KeyboardButton("Посмотреть добавленные")
btn_create_post = KeyboardButton("Создать пост")
btn_add_admin = KeyboardButton("Добавить админа")

btn_cancel = KeyboardButton("Отмена")
btn_miss = KeyboardButton("Пропустить")

# ДЛЯ ГОТОВОГО ПОСТА
btn_add_btn_url = InlineKeyboardButton(text="Добавить URL-кнопку", callback_data="btn_url")
btn_add_btn_text = InlineKeyboardButton(text="Добавить ТЕКСТ-кнопку", callback_data="btn_text")
btn_chanel_group = InlineKeyboardButton(text="Выбор каналов/групп", callback_data="channel_group")
btn_post = InlineKeyboardButton(text="Выложить", callback_data="post")
btn_post_later = InlineKeyboardButton(text="Выложить позже", callback_data="post_later")
btn_cancel_in = InlineKeyboardButton(text="Отмена", callback_data="cancel_in")

# УДАЛИТЬ КАНАЛ
btn_delete = InlineKeyboardButton(text="❌ Удалить ❌", callback_data="delete")

# НАЗАД
back = InlineKeyboardButton(text=f"🔙 Назад 🔙", callback_data="BACK")


BUTTON_TYPES = {
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_channel, btn_add_group).add(btn_view_added).add(btn_create_post).add(btn_add_admin),
    "BTN_DELETE_CHANNEL": InlineKeyboardMarkup().add(btn_delete),
    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
    "BTN_CANCEL_MISS": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_miss).add(btn_cancel),
    "BTN_POST":  InlineKeyboardMarkup().add(btn_add_btn_url, btn_add_btn_text).add(btn_chanel_group).add(btn_post, btn_post_later).add(btn_cancel_in),

    "BTN_BACK": InlineKeyboardMarkup().add(back),

    "BTN_REFERENCE": InlineKeyboardMarkup(),
}
