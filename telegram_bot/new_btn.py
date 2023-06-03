import asyncio


async def save_btn(message, state):
    all_data = await state.get_data()

    if message.text[0:6] == "https:":
        try:
            btn_url = all_data["btn_url"] + [message.text]
            await state.update_data(btn_url=btn_url)
        except:
            await state.update_data(btn_url=[message.text])

    else:
        try:
            btn_text_text = all_data["btn_text_text"] + [message.text]
            await state.update_data(btn_text_text=btn_text_text)
        except:
            await state.update_data(btn_text_text=[message.text])

        try:
            callback_data = all_data["callback_data"] + [f"{message.from_user.id}_" + f"{message.message_id}"]
            await state.update_data(callback_data=callback_data)
        except:
            await state.update_data(callback_data=[f"{message.from_user.id}_" + f"{message.message_id}"])


async def save_channel(callback, state):
    all_data = await state.get_data()
    try:
        channel_id_repost = all_data["channel_id_repost"] + [callback.data[:-6]]
        await state.update_data(channel_id_repost=channel_id_repost)
    except:
        await state.update_data(channel_id_repost=[callback.data[:-6]])


async def delete_channel(callback, state):
    all_data = await state.get_data()
    chanel_id_repost = all_data["channel_id_repost"]
    channel_id_repost = chanel_id_repost.remove(f"{callback.data[:-5]}")
    await state.update_data(channel_id_repost=channel_id_repost)


async def post(all_data, channel_id_repost, bot, text, mark, time):
    await asyncio.sleep(time)
    try:
        file_id = all_data["photo"]
        for channel in channel_id_repost:
            await bot.send_photo(chat_id=channel, photo=file_id, caption=text, reply_markup=mark)
    except:
        try:
            try:
                file_id = all_data["photo"]
                for channel in channel_id_repost:
                    await bot.send_video(chat_id=channel, video=file_id, caption=text, reply_markup=mark)
            except:
                file_id = all_data["photo"]
                for channel in channel_id_repost:
                    await bot.send_animation(chat_id=channel, animation=file_id, caption=text, reply_markup=mark)
        except:
            for channel in channel_id_repost:
                await bot.send_message(chat_id=channel, text=text, reply_markup=mark)
