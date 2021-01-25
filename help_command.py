import discord
import config
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
	def __init__(self):
		super().__init__(command_attrs = {
				'name': 'хелп',
				'brief': 'Показывает это сообщение.',
				'aliases': ['help', 'ashelp', 'асхелп']
			})

	def format_command_aliases(self, command):
		if not (command.aliases):
			return

		return ', '.join(f'`{alias}`' for alias in command.aliases)

	async def send_bot_help(self, mapping):
		for key, value in mapping.items():
			mapping[key] = await self.filter_commands(value)

		embed = discord.Embed(colour = 0xab92e0, title = 'Эта команда отображает базовую информацию о категориях и командах в них.')

		for cog, commands in mapping.items():
			commands = list(set(commands))
			value = []
			name = f'**{cog.qualified_name}:**' if cog else '**Вне категории:**'
			for com in commands:
				brief = com.brief
				if (brief):
					brief = list(brief); brief[0] = brief[0].lower(); brief = ''.join(brief)
				value.append(f'`{self.context.prefix}{com.name}` - {brief.rstrip(".") if brief else "описание недоступно"}')
			if (value):
				embed.add_field(name = name, value = '\n'.join(value))

		await self.context.send(embed = embed)

	async def send_command_help(self, command):
		if (await self.filter_commands([command])):
			param = self.context.bot.get_emoji(config.PARAM_EMOJI_ID)
			yes = self.context.bot.get_emoji(config.YES_EMOJI_ID)
			no = self.context.bot.get_emoji(config.NO_EMOJI_ID)
			embed = discord.Embed(
					colour = 0xab92e0,
					title = 'Эта команда отображает подробную информацию об указанной функции бота.'
				)
			docstring = inspect.getdoc(command.callback)
			if (docstring):
				docstring = docstring.format(prefix = self.context.prefix, param = str(param), yes = str(yes), no = str(no), aliases = self.format_command_aliases(command))
				embed.description = docstring
			else:
				embed.description = 'Похоже, эта команда не была задокументирована разработчиком.'

			await self.context.send(embed = embed)