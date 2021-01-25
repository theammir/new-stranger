import discord
import os, os.path
import utils
import database
import config
import sys
import utils
from help_command import HelpCommand
from discord.ext import commands

def get_pre(bot, message):
	return ['ас', 'as', 'As', 'Ас', 'AS', 'АС', 'аС', 'aS']

intents = discord.Intents.default()
intents.members = True; intents.presences = True
bot = commands.Bot(command_prefix = get_pre, case_insensitive = True, intents = intents, activity = utils.get_activity())

bot.help_command = HelpCommand()


@bot.event
async def on_ready(): # Runs when bot is ready
	# Cogs import
	current_dir = os.listdir()
	for file in current_dir:
		if (file[-3:] == '.py'): # If the file has .py extension
			if (file.startswith('cog_')):
				bot.load_extension(file[:-3])
				print(f'Loaded {file}')

	# Lines of code counting
	linesOfCode = 0
	for file in current_dir:
		if (file[-3:] == '.py'):
			linesOfCode += utils.get_length(file)
	print(f'Строк кода всего: {linesOfCode}')

	# Extenstions
	bot.load_extension('jishaku')

@bot.command(name = 'пинг', aliases = ['ping', 'asping', 'аспинг'], brief = 'Показывает пинг при отправке запроса и некоторую другую информацию.')
async def ping(ctx):
	'''
		Использование: `{prefix}пинг`.

		{param} Не принимает аргументов.

		Отправляет в чат задержку в милисекундах (мс), округлённую до десятитысячных (1/10000), занимаемое ботом место на диске и соотношение изображений к итоговому весу (Мб, округлённые до сотых).

		Ничего дополнительно не возвращает.
	'''
	latency_ms = bot.latency * 1000
	latency_ms = int(latency_ms * 10000) / 10000

	def get_directory_size(path: str = ''):
		size_bytes = 0

		current_dir = os.listdir(path if path else None)
		for file in current_dir:
			if (os.path.isfile(path + file)):
				size_bytes += os.path.getsize(path + file)
			elif (os.path.isdir(path + file)):
				size_bytes += get_directory_size(path + file + '/')

		return size_bytes

	size_mbytes = get_directory_size() / 1024 / 1024
	size_mbytes = int(size_mbytes * 100) / 100

	imgs_mbytes = get_directory_size('imgs/') / 1024 / 1024
	imgs_mbytes = int(imgs_mbytes * 100) / 100

	embed = discord.Embed(
			colour = 0xab92e0,
			title = 'PONG!~'
		)

	embed.add_field(name = 'Задержка', value = f'```{latency_ms}мс```')
	embed.add_field(name = 'Занимаемое место', value = f'```Бот занимает {size_mbytes}Мб на диске```')
	embed.add_field(name = 'Изображения', value = f'```{imgs_mbytes}/{size_mbytes}Мб```')

	await ctx.send(embed = embed)


with open('TOKEN.txt', 'r') as file:
	token = file.read()

bot.run(token) # Bot running