import aiohttp


class ChatGPT:
    """
    Класс для взаимодействия с API Chat GPT
    """
    def __init__(self, openai_api_key: str) -> None:
        """
        Метод инициализации класса ChatGPT

        :param openai_api_key: Токен аккаунта OpenAI
        """
        self.data = {"model": "gpt-3.5-turbo"}  # Предварительные данные
        self.url = 'https://api.openai.com/v1/chat/completions'  # Ссылка для запроса к API
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}  # Заголовки

    async def answer(self, messages: [dict]) -> dict:
        """
        Метод для отправки сообщений в Chat GPT

        :param messages: Список сообщений пользователя
        :return: Ответ Chat GPT в виде словаря
        """
        self.data["messages"] = messages  # Добавляем сообщения в данные запроса
        async with aiohttp.ClientSession(headers=self.headers) as session:  # Открываем асинхронную сессию с заголовками
            response = await session.post(self.url, json=self.data)  # Делаем POST запрос c данными к API Chat GPT
            return await response.json()  # Возвращаем ответ в виде словаря
