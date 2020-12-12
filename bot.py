import discord
import os
import utils
from discord.ext import commands

def get_pre(bot, message):
	return ['ас', 'as', 'ass']

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = get_pre, case_insensitive = True, intents = intents)

@bot.event
async def on_ready(): # Выполняется, когда бот запущен и готов к работе
	# Импортирование когов
	current_dir = os.listdir()
	for file in current_dir:
		if (file[-3:] == '.py'): # Если файл имеет расширение .py
			if (file.startswith('cog_')):
				bot.load_extension(file[:-3])
				print(f'Loaded {file}')

	# Подсчет строк кода
	linesOfCode = 0
	for file in current_dir:
		linesOfCode += utils.get_length(file)
	print(f'Строк кода всего: {linesOfCode}')

bot.run('') # Запуск бота