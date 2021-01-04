import discord
import config
import os.path
import database
import random
import datetime as dt
from discord.ext import commands

class DogmasCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.conn = database.Instance(config.DB_NAME)
		

	@commands.command(name = 'догма')
	async def asdogma(self, ctx, key):
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
			result = self.conn.add_item({'key': key, 'message': content, 'img': path, 'author': ctx.message.author.id, 'stamp': dt.datetime.now().strftime('%b, %d.%m.%Y %H:%M')})
			await ctx.message.add_reaction('✔️')

	@commands.command(name = 'догма_инфо')
	async def asdogma_info(self, ctx, key):
		dogma = self.conn.find_item(key = key)
		if not (dogma):
			await ctx.message.add_reaction('❌')

		else:
			embed = discord.Embed(
					colour = 0xab92e0,
					title = f'Догма \"{dogma["key"]}\"',
				)
			if (dogma.get('author')):
				author = self.bot.get_user(dogma['author'])
				embed.set_author(name = str(author), icon_url = author.avatar_url)
			else:
				embed.set_author(name = 'Автор неизвестен', icon_url = 'https://i.imgur.com/rWGrw6c.png')

			if (dogma.get('message')):
				embed.add_field(name = 'Текстовое содержание', value = dogma['message'] if len(dogma['message']) < 200 else dogma['message'][200:] + '...')
			if (dogma.get('img')):
				embed.description = 'Содержит изображение.'
			if (dogma.get('stamp')):
				embed.set_footer(text = 'Дата добавления: ' + dogma['stamp'])
			else:
				embed.set_footer(text = 'Дата добавления неизвестна')
				
			await ctx.send(embed = embed)

	@commands.command(name = 'радуга', aliases = ['лгбт'])
	async def asrainbow(self, ctx):
		dogma = random.choice(self.conn.db.all())

		await self.asdogma_info(ctx, dogma['key'])
		await self.asdogma(ctx, dogma['key'])




def setup(bot):
	bot.add_cog(DogmasCog(bot))