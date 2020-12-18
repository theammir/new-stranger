import discord
import config
import os.path
import database
from discord.ext import commands

class DogmasCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.conn = database.Instance(config.DB_NAME)
		

	@commands.command(name = 'догма')
	async def dogma(self, ctx, key):
		key = key.lower() # To make dogmas case insensitive

		# Trying to select the dogma
		dogma = self.conn.find_item(key = key)
		print(dogma)
		if (dogma):
			await ctx.send(content = dogma.get('message'), file = discord.File(dogma.get('img')) if dogma.get('img') != '' else None)
		else:
			await ctx.message.add_reaction('❌')

	@commands.command(name = 'сет')
	async def asset(self, ctx, key, *, content = ''):
		key = key.lower()

		# Trying to get the dogma
		dogma = self.conn.find_item(key = key)
		if (dogma):
			await ctx.message.add_reaction('❌')
		else:
			path = ''
			if (ctx.message.attachments):
				file = ctx.message.attachments[0]
				extension = file.filename[file.filename.index('.'):]
				path = r'imgs\\_' + key + extension
				await ctx.message.attachments[0].save(path)
			result = self.conn.add_item({'key': key, 'message': content, 'img': path})
			await ctx.message.add_reaction('✔️')



def setup(bot):
	bot.add_cog(DogmasCog(bot))