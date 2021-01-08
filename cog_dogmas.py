import discord
import config
import os, os.path
import database
import random
import requests, io
import datetime as dt
from discord.ext import commands

class DogmasCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.conn = database.Instance(config.DB_NAME)
		

	@commands.command(name = 'догма')
	async def asdogma(self, ctx, key):
		key = key.lower() # To make dogmas case insensitive
		image = None
		filename = ''

		# Trying to select the dogma
		dogma = self.conn.find_item(key = key)
		if (dogma):
			image = dogma.get('img')
			if (image):
				if not (os.path.exists(image)):
					unknown = requests.get(config.UNKNOWN_PIC)
					image = io.BytesIO(unknown.content)
					filename = config.PIC_NAME if config.PIC_NAME else 'unknown.jpg'
					await ctx.send("`Похоже, изображение не может быть найдено или повреждено. Это не значит, что мы его потеряли - так как название, под которым сохраняется картинка зависит от названия самой догмы, это могло случиться из-за невозможности назвать файл тем или иным образом (например, если назвать догму пингом другана или знаком вопроса).\n\nБлагодарим за понимание.`")
			await ctx.send(content = dogma.get('message'), file = discord.File(image, filename = filename if filename else None))
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
				path = r'imgs/_' + key + extension
				await ctx.message.attachments[0].save(path)
			result = self.conn.add_item({
				'key': key,
				'message': content,
				'img': path,
				'author': ctx.message.author.id,
				'stamp': dt.datetime.now().strftime('%b, %d.%m.%Y %H:%M')})
			await ctx.message.add_reaction('✔️')

			dogmas_count = len(self.conn.db.all())
			word = ''
			if (str(dogmas_count).endswith('1')):
				word = 'догму'
			elif (str(dogmas_count).endswith(('2', '3', '4'))):
				word = 'догмы'
			elif (str(dogmas_count).endswith(('0', '5', '6', '7', '8', '9'))):
				word = 'догм'
			
			await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"на {dogmas_count} {word}"))

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
				embed.set_author(name = 'Автор неизвестен', icon_url = config.UNKNOWN_PIC)

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

	@commands.command(name = 'делит', aliases = ['delete'])
	async def asdelete(self, ctx, key):
		dogma = self.conn.find_item(key = key)
		if not (dogma):
			await ctx.message.add_reaction('❌')

		else:
			self.conn.delete_item(key = key)
			if (dogma.get('img')):
				os.remove(dogma['img'])

			await ctx.message.add_reaction('✔️')

			dogmas_count = len(self.conn.db.all())
			word = ''
			if (str(dogmas_count).endswith('1')):
				word = 'догму'
			elif (str(dogmas_count).endswith(('2', '3', '4'))):
				word = 'догмы'
			elif (str(dogmas_count).endswith(('0', '5', '6', '7', '8', '9'))):
				word = 'догм'
			
			await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"на {dogmas_count} {word}"))




def setup(bot):
	bot.add_cog(DogmasCog(bot))