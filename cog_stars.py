import discord
import pss_api
import re
import asyncio
import datetime, time
import config
from discord.ext import commands, tasks

class StarCog(commands.Cog): # Cog class
	def __init__(self, bot):
		self.bot = bot
		self.NOW = datetime.date.today()
		self.bot.loop.create_task(self._ainit())
		self.property = '@Trophy'

	async def _ainit(self):
		self.get_property.start()
		await asyncio.sleep(5)
		self.count_loop.start()

	def cog_unload(self):
		self.get_property.cancel()
		self.count_loop.cancel()

	def _count_member_property(self, memberNick: str, property: str):
		user_data = pss_api.inspect_user(memberNick)
		if (user_data):
			return int(user_data[property])
		else:
			return 'NO DATA'

	def _get_member_fleet_division(self, memberNick):
		user_data = pss_api.inspect_user(memberNick)
		division = ''
		if (user_data):
			if (user_data.get('@Alliance')):
				fleet_ranking = pss_api.find_fleet_ranking(user_data['@Alliance']['@AllianceName'])

				if (fleet_ranking in range(51, 101)):
					division = config.DIVISIONS[0]
				elif (fleet_ranking in range(21, 51)):
					division = config.DIVISIONS[1]
				elif (fleet_ranking in range(9, 21)):
					division = config.DIVISIONS[2]
				elif (fleet_ranking in range(1, 9)):
					division = config.DIVISIONS[3]

		return division


	@commands.command(name = 'каунт')
	async def count(self, ctx):
		print("Invoked.")
		phoenix_role = discord.utils.get(ctx.guild.roles, name = config.TRUE_PHOENIX_ROLE_NAME) # Получаем роль феникса

		if (self.NOW.day in range(1, config.BREAKTIME + 1)):
			return

		if (phoenix_role):
			ingameUsername = '' # In-game player nickname
			for member in ctx.guild.members: # For each member: (in-game nick finding)
				if (phoenix_role in member.roles):
					memberNick = member.display_name
	
					info_search = re.findall(config.INFO_PATTERN, memberNick) # Finding table in member's nick
					if (info_search): # If info was found
						group = ''.join(info_search)
						nickToCheck = memberNick[len(group):]
					else:
						nickToCheck = memberNick

					bracket_search = re.search(config.BRACKET_PATTERN, nickToCheck) # Finding content in member's nick's brackets
					if (bracket_search):
						ingameUsername = bracket_search.group()[1:-1]
					else: # If wasn't found
						ingameUsername = nickToCheck
						
					user_property = self._count_member_property(ingameUsername, self.property)
					user_division = self._get_member_fleet_division(ingameUsername)

					try:
						if not (user_property == 'NO DATA'):
							table = f'[{user_division}{user_property}{config.PROPERTIES[self.property]}]'
						else:
							table = ''
						await member.edit(nick = f'{table}{nickToCheck}')
					except:
						if (len(memberNick) > 24):
							print(memberNick + ' has more than 24 symbols.')
						else:
							print(f'Cannot edit {memberNick}\'s nick.')
				else:
					info_search = re.findall(config.INFO_PATTERN, member.display_name)
					if (info_search):
						group = ''.join(info_search)
						await member.edit(nick = member.display_name[len(group):])
		else:
			print('Роль феникса не может быть найдена.')

	@tasks.loop(minutes = config.UPDATE_INTERVALS['PROPERTY'])
	async def count_loop(self):
		try:
			channel = self.bot.get_channel(config.CTX_CHANNEL)
			message = await channel.fetch_message(config.CTX_MESSAGE)

			ctx = await self.bot.get_context(message)
			await ctx.invoke(self.count)
		except Exception as e:
			print(e)
			return

	@tasks.loop(minutes = config.UPDATE_INTERVALS['PROPERTY'])
	async def get_property(self):
		try:
			DAYS = [30, 29 if (self.NOW.year % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

			if (int(time.strftime('%H')) in range(1)):
				if (self.NOW.day <= DAYS[self.NOW.month - 1] and self.NOW.day >= DAYS[self.NOW.month - 1] - 6):
					self.property = "@AllianceScore"
				else:
					self.property = "@Trophy"

			for prop in config.PROPERTIES:
				if (self.property == prop):
					self.count_loop.change_interval(minutes = config.UPDATE_INTERVALS[prop])
		except Exception as e:
			print(e)
			return




def setup(bot): # Adding the cog into bot.
	bot.add_cog(StarCog(bot))