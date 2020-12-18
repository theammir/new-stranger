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

	

bot.run('') # Bot running