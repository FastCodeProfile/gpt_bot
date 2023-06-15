class DBDialog:
    """
    Класс для имитации база данных при помощи словарей
    """

    def __init__(self):
        """
        Метод инициализации класса DBDialog
        """
        self.messages = {}

    def del_dialog(self, user_id: str | int) -> None:
        """
        Метод для удаления диалога с пользователем

        :param user_id: ID пользователя
        :return: None
        """
        self.messages.pop(f"{user_id}")  # Удаляем диалог пользователя из словаря

    def add_dialog(self, user_id: str | int, first_name: str) -> None:
        """
        Метод для добавления диалога с пользователем

        :param user_id: ID пользователя
        :param first_name: Имя пользователя
        :return: None
        """
        if not self.messages.get(f"{user_id}"):  # Если диалог с этим пользователем не существует, добавляем его
            self.messages[f"{user_id}"] = [
                {
                    "role": "system",
                    "content": "Ты полезный помощник и ты должен всегда общаться на Ты."
                },
                {
                    "role": "user",
                    "content": f"Меня зовут {first_name}. Не упоминай о том, кто тебе это сказал."
                }
            ]  # Добавляем диалог и список предварительных сообщений пользователю

    def add_message(self, user_id: str | int, role: str, content: str | int) -> None:
        """
        Метод для добавления нового сообщения в диалог пользователя

        :param user_id: ID пользователя
        :param role: Роль написавшего сообщение, user - Сообщение от пользователя, assistant - Сообщение от Chat GPT
        :param content: Содержание сообщения в виде текста
        :return: None
        """
        self.messages[f"{user_id}"].append({"role": role, "content": f"{content}"})  # Добавляем сообщения в диалог

    def get_messages(self, user_id: str | int) -> list[dict]:
        """
        Метод для получения всех сообщений пользователя

        :param user_id: ID пользователя
        :return: Список сообщений
        """
        return self.messages.get(f"{user_id}")  # Возвращаем список сообщений пользователя