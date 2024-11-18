import logging
from run import bot, global_state

async def get_chat_id(username):
    chat = await bot.get_chat(username)
    return await get_channel_members(bot, chat.id)


async def get_channel_members(bot, channel_id: int):
    members = []
    chat = await bot.get_chat(channel_id)
    
    # Получаем количество участников
    total_members = await bot.get_chat_member_count(channel_id)  # Это вернёт именно число

    for user_id in range(total_members):  # Теперь здесь будет нормальное число
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            members.append(member.user)
        except Exception as e:
            print(f"Ошибка: {e}")
    
    return members