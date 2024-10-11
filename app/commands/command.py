from aiogram.types import BotCommand

command = [
    BotCommand(command="/start", description='Приветвие и описание работы'),
    BotCommand(command="/weather", description='Введите /weather [город], например /weather moscow'),
    BotCommand(command="/save", description='После выбора команды введите название города, который сохраниться для вас'),
    BotCommand(command="/mycity", description='Вывод погоды в городе который вы сохранили до этого'),
]