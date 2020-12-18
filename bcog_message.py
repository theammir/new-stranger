import discord
from discord.ext import commands

class MessageCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		channel = message.channel

		killant = self.bot.get_user(472853149137240064)
		if (killant in message.mentions):
			await channel.send('```#КИЛЛ ВЕРНИСЬ В КОНОХУ```')

		if ('суй' in message.content.lower()):
			await channel.send('СУЙ ОГУРЕЦ В ЖОПУ!')
		if ('ъуъ' in message.content.lower()):
			await channel.send('ЪУЪ ОГУРЕЦ В ЖОПУ!')


def setup(bot):
	bot.add_cog(MessageCog(bot))