import asyncio
from os import getenv

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from .integration import ChatGPT
from .utils import DBDialog

load_dotenv()


bot = AsyncTeleBot(getenv('TOKEN'))
db_dialog = DBDialog()  # Экземпляр класса DBDialog
db_dialog.add_dialog('0', 'Система')  # Создаём системный диалог
chat_gpt = ChatGPT(getenv('GPT_TOKEN'))  # Экземпляр класса ChatGPT


@bot.message_handler(commands=['start'])
async def handler_command_start(message: Message) -> None:
    system_dialog = db_dialog.get_messages('0')  # Получаем все системные сообщения
    system_dialog.append({"role": "user", "content": "Кто ты и чем ты полезен? Оформи текст смайликами."})
    chat_gpt_answer = await chat_gpt.answer(system_dialog)  # Отправляем диалог в Chat GPT
    await bot.reply_to(message,
                       f'{chat_gpt_answer["choices"][0]["message"]["content"]}')  # Отправляем ответ пользователю


@bot.message_handler(commands=['reset'])
async def handler_command_reset(message: Message) -> None:
    user_id = message.from_user.id
    if db_dialog.get_messages(user_id):  # Проверяем существование диалога
        db_dialog.del_dialog(user_id)  # Сбрасываем диалог
    await bot.reply_to(message, 'Контекст диалога сброшен 💬')


@bot.message_handler(func=lambda message: True)
async def handler_chat_gpt(message: Message) -> None:
    """
    Обработчик для общения с Chat GPT
    :param message: Объект класса Message
    :return: None
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    db_dialog.add_dialog(user_id, first_name)  # Добавляем диалог, если его не существует
    db_dialog.add_message(user_id, 'user', message.text)  # Добавляем сообщение пользователя в диалог
    user_messages = db_dialog.get_messages(user_id)  # Получаем все сообщения пользователя
    chat_gpt_answer = await chat_gpt.answer(user_messages)  # Отправляем сообщения в Chat GPT
    db_dialog.add_message(user_id, 'assistant',
                          chat_gpt_answer["choices"][0]["message"]["content"])  # Добавляем ответ в диалог
    await bot.reply_to(message, chat_gpt_answer["choices"][0]["message"]["content"])  # Отправляем ответ пользователю
    if len(db_dialog.get_messages(user_id)) > 30:  # Если в диалоге больше 30 сообщений, сбрасываем его
        db_dialog.del_dialog(user_id)  # Сбрасываем диалог


asyncio.run(bot.polling())
