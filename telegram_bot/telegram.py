import re
import logging

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from telegram_bot.utils import StatesUsers, StatesAdmin
from telegram_bot.KeyboardButton import BUTTON_TYPES
from telegram_bot.new_btn import save_btn, save_channel, delete_channel, post
from content_text.messages import MESSAGES
from cfg.cfg import TOKEN, ADMIN_ID, CHANNEL_ID, C_DATA_TEXT


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# =============== ДОБАВИТЬ КАНАЛ ===============
@dp.message_handler(lambda message: message.text.lower() == 'добавть канал')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['add_channel'], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(StatesAdmin.all()[0])


# =============== ВВОД ID КАНАЛА ===============
@dp.message_handler(state=StatesAdmin.STATES_0)
async def start_command(message: Message, state: FSMContext):
    try:
        CHANNEL_ID[f"{int(message.forward_from_chat.id)}"] = f"{message.forward_from_chat.username}"
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

    except:
        await message.answer("Канал не был добавлен!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# =============== ДОБАВИТЬ ГРУППУ ===============
@dp.message_handler(lambda message: message.text.lower() == 'добавть группу')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['add_group'], parse_mode="MARKDOWN")


# =============== ВВОД ГРУППЫ ===============
@dp.message_handler(lambda message: message.text == 'ere02423-piWAFkdab')
async def start_command(message: Message):
    try:
        if message.chat.username is None:
            CHANNEL_ID[f"{int(message.chat.id)}"] = f"Закрытая_группа_{message.chat.id}"
            await message.answer("Добавил!")
        else:
            CHANNEL_ID[f"{int(message.chat.id)}"] = f"{message.chat.username}"
            await message.answer("Добавил!")

    except:
        await message.answer("Канал не был добавлен!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


# =============== ПОСМОТРЕТЬ ДОБАВЛЕННЫЕ КАНАЛ ===============
@dp.message_handler(lambda message: message.text.lower() == 'посмотреть добавленные')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:

        if message.from_user.id in ADMIN_ID:
            if not list(CHANNEL_ID.keys()):
                await message.answer(MESSAGES['not_channel'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

            else:
                await message.answer(MESSAGES['all_channel'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
                for channel in list(CHANNEL_ID.items()):
                    await message.answer(f"https://t.me/{channel[1]} | {channel[0]}", reply_markup=BUTTON_TYPES["BTN_DELETE_CHANNEL"])


# =============== УДАЛИТЬ КАНАЛ ===============
@dp.callback_query_handler(lambda c: c.data == "delete")
async def start_command(callback: CallbackQuery):
    try:
        matches = re.findall(r"(?<=\|).*", callback.message.text)
        for match in matches:
            id_g = match.strip()
            del CHANNEL_ID[f"{id_g}"]

        await callback.message.edit_reply_markup()
        await callback.message.edit_text(f"Канал: {callback.message.text} \n    Удалён")
    except Exception as ex:
        print(ex)


# =============== СОЗДАТЬ ПОСТ ===============
@dp.message_handler(lambda message: message.text.lower() == 'создать пост')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            if CHANNEL_ID == {}:
                await message.answer(MESSAGES['not_channel'])
                await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            else:
                await message.answer(MESSAGES['create_post_1'], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(StatesUsers.all()[0])


# =============== Добавления фото ===============
@dp.message_handler(state=StatesUsers.STATE_0)
async def start_command(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES['create_post_2'], reply_markup=BUTTON_TYPES["BTN_CANCEL_MISS"])
        await state.update_data(text=message.text)
        await state.set_state(StatesUsers.all()[1])


# =============== ВЫВОД ПОСТА ===============
@dp.message_handler(content_types=["photo"], state=StatesUsers.STATE_1)
async def get_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    all_data = await state.get_data()
    text = all_data["text"]
    await state.update_data(photo=file_id)

    await bot.send_photo(message.chat.id, file_id, caption=text)
    await message.answer(MESSAGES['create_post_3'], reply_markup=BUTTON_TYPES["BTN_POST"])
    await state.set_state(StatesUsers.all()[2])


@dp.message_handler(state=StatesUsers.STATE_1)
async def start_command(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        all_data = await state.get_data()
        text = all_data["text"]
        await message.answer(text)
        await message.answer(MESSAGES['create_post_3'], reply_markup=BUTTON_TYPES["BTN_POST"])
        await state.set_state(StatesUsers.all()[2])


# =============== ДОБАВИТЬ КНОПКУ С URL ===============
@dp.callback_query_handler(lambda c: c.data == "btn_url", state=StatesUsers.STATE_2)
@dp.callback_query_handler(lambda c: c.data == "btn_text", state=StatesUsers.STATE_2)
async def start_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(MESSAGES["btn_url_1"])

    if callback.data == "btn_url":
        await state.set_state(StatesUsers.all()[3])
    elif callback.data == "btn_text":
        await state.set_state(StatesUsers.all()[5])


# =============== ДОБАВИТЬ URL ===============
@dp.message_handler(state=StatesUsers.STATE_3)
async def start_command(message: Message, state: FSMContext):
    text_btn_url = await state.get_data()
    try:
        text_btn_url = text_btn_url["text_btn_url"] + [message.text]
        await state.update_data(text_btn_url=text_btn_url)
    except:
        await state.update_data(text_btn_url=[message.text])

    await message.answer(MESSAGES["btn_url_2"])
    await state.set_state(StatesUsers.all()[4])


# =============== ДОБАВИТЬ ТЕКСТ ПОСЛЕ ПОДПИСКИ ===============
@dp.message_handler(state=StatesUsers.STATE_5)
async def start_command(message: Message, state: FSMContext):
    text_btn_text = await state.get_data()
    try:
        text_btn_url = text_btn_text["text_btn_text"] + [message.text]
        await state.update_data(text_btn_text=text_btn_url)
    except:
        await state.update_data(text_btn_text=[message.text])

    await message.answer(MESSAGES["btn_text_1"])
    await state.set_state(StatesUsers.all()[4])


# =============== ДОБАВИТЬ URL ===============
@dp.message_handler(state=StatesUsers.STATE_4)
async def start_command(message: Message, state: FSMContext):
    await save_btn(message, state)

    mark = InlineKeyboardMarkup()
    # ДОБАВЛЕИЕ КНОПКИ С ССЫЛКОЙ
    all_data = await state.get_data()
    try:
        btn_url = all_data["btn_url"]
        text_btn_url = all_data["text_btn_url"]
        for idx, btn in enumerate(btn_url):
            mark.add(InlineKeyboardButton(text=text_btn_url[idx], url=btn))
    except:
        pass

    # ДОБАВЛЕИЕ КНОПКИ С ТЕКСТОМ
    try:
        text_btn_text = all_data["text_btn_text"]

        for idx, btn in enumerate(text_btn_text):
            mark.add(InlineKeyboardButton(text=btn, callback_data=f"{all_data['callback_data'][idx]}"))
    except:
        pass

    # ОТПРАВКА ПОСТА
    try:
        file_id = all_data["photo"]
        text = all_data["text"]
        await bot.send_photo(message.chat.id, file_id, caption=text, reply_markup=mark)
        await message.answer(MESSAGES['create_post_3'], reply_markup=BUTTON_TYPES["BTN_POST"])
        await state.set_state(StatesUsers.all()[2])
    except:
        text = all_data["text"]
        await message.answer(text, reply_markup=mark)
        await message.answer(MESSAGES['create_post_3'], reply_markup=BUTTON_TYPES["BTN_POST"])
        await state.set_state(StatesUsers.all()[2])


# =============== ВЫБОР КАНАЛОВ ===============
@dp.callback_query_handler(lambda c: c.data == "channel_group", state=StatesUsers.STATE_2)
async def start_command(callback: CallbackQuery, state: FSMContext):
    mark = InlineKeyboardMarkup()
    for channel in list(CHANNEL_ID.items()):
        try:
            channel_id_repost = await state.get_data()
            if f"{channel[0]}" in channel_id_repost["channel_id_repost"]:
                mark.add(InlineKeyboardButton(text=f"✅ https://t.me/{channel[1]} | {channel[0]} ✅", callback_data=f"{channel[0]}_True"))
            else:
                mark.add(InlineKeyboardButton(text=f"❎ https://t.me/{channel[1]} | {channel[0]} ❎", callback_data=f"{channel[0]}_False"))
        except:
            mark.add(InlineKeyboardButton(text=f"❎ https://t.me/{channel[1]} | {channel[0]} ❎", callback_data=f"{channel[0]}_False"))

    mark.add(InlineKeyboardButton(text=f"🔙 Назад 🔙", callback_data=f"BACK"))

    await callback.message.edit_text(MESSAGES["channel_group"], reply_markup=mark)

    await state.set_state(StatesUsers.all()[6])


# =============== НАЗАД ===============
@dp.callback_query_handler(state=StatesUsers.STATE_6)
@dp.callback_query_handler(lambda c: c.data == "BACK", state=StatesUsers.STATE_7)
async def start_command(callback: CallbackQuery, state: FSMContext):
    if callback.data == "BACK":
        await callback.message.edit_text(MESSAGES['create_post_3'], reply_markup=BUTTON_TYPES["BTN_POST"])
        await state.set_state(StatesUsers.all()[2])

    else:
        mark = InlineKeyboardMarkup()
        if "False" in callback.data:
            await save_channel(callback, state)

        else:
            await delete_channel(callback, state)

        for channel in list(CHANNEL_ID.items()):
            try:
                channel_id_repost = await state.get_data()
                if f"{channel[0]}" in channel_id_repost["channel_id_repost"]:
                    mark.add(InlineKeyboardButton(text=f"✅ https://t.me/{channel[1]} | {channel[0]} ✅",
                                                  callback_data=f"{channel[0]}_True"))
                else:
                    mark.add(InlineKeyboardButton(text=f"❎ https://t.me/{channel[1]} | {channel[0]} ❎",
                                                  callback_data=f"{channel[0]}_False"))
            except:
                mark.add(InlineKeyboardButton(text=f"❎ https://t.me/{channel[1]} | {channel[0]} ❎",
                                              callback_data=f"{channel[0]}_False"))

        mark.add(InlineKeyboardButton(text=f"🔙 Назад 🔙", callback_data=f"BACK"))
        await callback.message.edit_text(MESSAGES["channel_group"], reply_markup=mark)
        await state.set_state(StatesUsers.all()[6])


# =============== ВЫЛОЖИТЬ ===============
@dp.callback_query_handler(lambda c: c.data == "post", state=StatesUsers.STATE_2)
async def start_command(callback: CallbackQuery, state: FSMContext):
    try:
        all_data = await state.get_data()
        channel_id_repost = all_data["channel_id_repost"]

        if not channel_id_repost:
            await callback.answer(text="Что бы выложить пост выбери каналы", show_alert=True)
        else:
            await callback.answer(text="Пост выложен!", show_alert=True)

            mark = InlineKeyboardMarkup()
            # ДОБАВЛЕИЕ КНОПКИ С ССЫЛКОЙ
            try:
                btn_url = all_data["btn_url"]
                text_btn_url = all_data["text_btn_url"]
                for idx, btn in enumerate(btn_url):
                    mark.add(InlineKeyboardButton(text=text_btn_url[idx], url=btn))
            except:
                pass

            # ДОБАВЛЕИЕ КНОПКИ С ТЕКСТОМ
            try:
                text_btn_text = all_data["text_btn_text"]

                for idx, btn in enumerate(text_btn_text):
                    mark.add(InlineKeyboardButton(text=btn, callback_data=f"{all_data['callback_data'][idx]}"))

                    C_DATA_TEXT[f"{all_data['callback_data'][idx]}"] = f"{all_data['btn_text_text'][idx]}"

            except:
                pass

            text = all_data["text"]

            await post(all_data, channel_id_repost, bot, text, mark, 0)

            await callback.message.edit_reply_markup()
            await callback.message.edit_text("Выложил!")
            await state.finish()
    except:
        await callback.answer(text="Что бы выложить пост выбери каналы", show_alert=True)


# =============== ЗАПРОС ВРЕМЕНИ ===============
@dp.callback_query_handler(lambda c: c.data == "post_later", state=StatesUsers.STATE_2)
async def start_command(callback: CallbackQuery, state: FSMContext):
    try:
        all_data = await state.get_data()
        channel_id_repost = all_data["channel_id_repost"]
        if not channel_id_repost:
            await callback.answer(text="Что бы выложить пост выбери каналы", show_alert=True)
        else:
            await callback.message.edit_text("Введи число в секундах через сколько выложить пост", reply_markup=BUTTON_TYPES["BTN_BACK"])
            await state.set_state(StatesUsers.all()[7])
    except:
        await callback.answer(text="Что бы выложить пост выбери каналы", show_alert=True)


# =============== ВЫЛОЖИТЬ ПОЗЖЕ ===============
@dp.message_handler(state=StatesUsers.STATE_7)
async def start_command(message: Message, state: FSMContext):
    try:
        time_post = int(message.text)
        all_data = await state.get_data()
        channel_id_repost = all_data["channel_id_repost"]

        mark = InlineKeyboardMarkup()
        # ДОБАВЛЕИЕ КНОПКИ С ССЫЛКОЙ
        try:
            btn_url = all_data["btn_url"]
            text_btn_url = all_data["text_btn_url"]
            for idx, btn in enumerate(btn_url):
                mark.add(InlineKeyboardButton(text=text_btn_url[idx], url=btn))
        except:
            pass

        # ДОБАВЛЕИЕ КНОПКИ С ТЕКСТОМ
        try:
            text_btn_text = all_data["text_btn_text"]

            for idx, btn in enumerate(text_btn_text):
                mark.add(InlineKeyboardButton(text=btn, callback_data=f"{all_data['callback_data'][idx]}"))

                C_DATA_TEXT[f"{all_data['callback_data'][idx]}"] = f"{all_data['btn_text_text'][idx]}"

        except:
            pass

        text = all_data["text"]

        await message.answer(f"Пост будет выложен через {message.text}сек", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()

        await post(all_data, channel_id_repost, bot, text, mark, time_post)

    except:
        await message.answer("Вы ввели не целое число\nВведите целое число в секундах")
        await state.set_state(StatesUsers.all()[7])


# =============== ДОБАВИТЬ АДМИНА ===============
@dp.message_handler(lambda message: message.text.lower() == 'добавить админа')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(StatesAdmin.all()[1])


# =============== ВВОД ID АДМИНА ===============
@dp.message_handler(state=StatesAdmin.STATES_1)
async def start_command(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# =============== ОТМЕНА ===============
@dp.message_handler(lambda message: message.text.lower() == 'отмена')
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


@dp.callback_query_handler(lambda c: c.data == "cancel_in", state=StatesUsers.STATE_2)
async def start_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    await state.finish()


# СООБЩЕНИЯ В ГРУППЕ
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: CallbackQuery):
    for channel in CHANNEL_ID:
        user_id = callback_query.from_user.id
        chat_member = await bot.get_chat_member(channel, user_id)

        if chat_member.is_chat_member():
            for data_text in C_DATA_TEXT.items():
                if callback_query.data == data_text[0]:
                    await callback_query.answer(text=data_text[1], show_alert=True)
        else:
            await callback_query.answer("Подпишитесь, чтобы узнать текст кнопки.", show_alert=True)


# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
@dp.message_handler()
async def start_command(message: Message):
    if message.from_user.id == message.chat.id:
        if message.from_user.id in ADMIN_ID:
            await message.answer(MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    executor.start_polling(dp, on_shutdown=shutdown)
