from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
start_admin_message = "Приветствую админ 👋"

add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
add_channel_message = "Перещли сюда любое сообщение из канала"
not_command_message = "Такой команды нет"
all_channel_message = "Все добавленные каналы:"
not_channel_message = "У вас пока нет добавленных каналов!"
add_group_message = 'В группе бот должен быть добавлен как администратор\nНапишите в группу: `ere02423-piWAFkdab`'

create_post_1_message = "Введите текст поста:"
create_post_2_message = "Скиньте фото для поста:"
create_post_3_message = "Так выглядит ваш пост"

btn_url_1_message = "Впишите название кнопки"
btn_url_2_message = "Впишите url для кнопки"

btn_text_1_message = "Впишите что будет выводить кнопка после подписки"

channel_group_message = "Выбери каналы/группы в которые выложить этот пост"


MESSAGES = {
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,
    "add_channel": add_channel_message,
    "all_channel": all_channel_message,
    "not_channel": not_channel_message,
    "add_group": add_group_message,
    "create_post_1": create_post_1_message,
    "create_post_2": create_post_2_message,
    "create_post_3": create_post_3_message,

    "btn_url_1": btn_url_1_message,
    "btn_url_2": btn_url_2_message,

    "btn_text_1": btn_text_1_message,
    "channel_group": channel_group_message,
}
