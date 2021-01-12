import discord
import config
import os, os.path
import database
import random
import config
import utils
import datetime as dt
from discord.ext import commands

class DogmasCog(commands.Cog, name = 'Догмы'):
	def __init__(self, bot):
		self.bot = bot
		self.conn = database.Instance(config.DB_NAME)

		self.yes = self.bot.get_emoji(config.YES_EMOJI_ID)
		self.no = self.bot.get_emoji(config.NO_EMOJI_ID)

		if not (os.path.exists('imgs')):
			os.mkdir('imgs')

	@commands.Cog.listener()
	async def on_message(self, message):
		ctx = await self.bot.get_context(message)
		if (message.content.startswith('//')):
			await self.asdogma(ctx, message.content.split(' ')[0][2:])

	@commands.command(name = 'догма', aliases = ['асдогма', 'dogma', 'asdogma'] brief = 'Отправляет в чат догму по указанному пользователем названию.')
	async def asdogma(self, ctx, key):
		'''
			Использование: `{prefix}догма <название>`.

				{param} <название> - название догмы, которую вы хотите отправить.
				Список догм можно посмотреть... пока-что нигде.

			Отправляет в чат догму (картинку и/или текст, предварительно заданную другим пользователем) в чат.
			Короткий вариант использования: //<название>.

			Вы можете просмотреть информацию о догме с помощью команды `{prefix}догма_инфо`.

			Возвращает:
				{no}: Если догма не была найдена.
		'''
		key = key.lower() # To make dogmas case insensitive
		image = None

		# Trying to select the dogma
		dogma = self.conn.find_item(key = key)
		if (dogma):
			image = dogma.get('img')
			if (image):
				print(image)
				if not (os.path.exists(image)):
					image = config.UNKNOWN_PIC
					await ctx.send("`Похоже, изображение не может быть найдено или повреждено. Это не значит, что мы его потеряли - так как название, под которым сохраняется картинка зависит от названия самой догмы, это могло случиться из-за невозможности назвать файл тем или иным образом (например, если назвать догму пингом другана или знаком вопроса).\n\nБлагодарим за понимание.`")
			await ctx.send(content = dogma.get('message'), file = discord.File(image) if image else None)
		else:
			await ctx.message.add_reaction(self.no)

	@commands.command(name = 'сет', aliases = ['ассет', 'asset', 'set'], brief = 'Создаёт вашу собственную догму.')
	async def asset(self, ctx, key, *, content = ''):
		'''
			Использование: `{prefix}сет <название> [содержание]`
				Возможно прикрепить к сообщению файл (к примеру, картинку, .mp3, .mp4...).

				{param} <название> - название вашей догмы. Не должно содержать пробелов, переносов строки (проще говоря, не больше одного слова).
				{param} [содержание] - текст, который будет выводиться. Является необязательным параметром при наличии вложенного файла.
				{param} [вложение] - файл, который будет выводиться. Является необязательным параметром при наличии содержания.

			Позволяет создать собственную догму. Имейте ввиду, что в информации о каждой догме сохраняется её автор.

			Вы можете отправить собственную догму с помощью команды `асдогма` (//).

			Возвращает:
				{no}: Если догма с таким названием уже существует.
				{yes}: При успешном создании догмы.
		'''
		key = key.lower()

		# Trying to get the dogma
		dogma = self.conn.find_item(key = key)
		if (dogma):
			await ctx.message.add_reaction(self.no)
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
			await ctx.message.add_reaction(self.yes)

			await utils.update_presence(self.bot)

	@commands.command(name = 'догма_инфо', aliases = ['асдогма_инфо', 'асдогма-инфо', 'догма-инфо', 'dogma_info', 'dogma-info', 'asdogma_info', 'asdogma-info'], brief = 'Показывает некоторую информацию о догме.')
	async def asdogma_info(self, ctx, key):
		'''
			Использование: `{prefix}догма_инфо <название>`

				{param} <название> - название догмы, информацию о которой вы хотите получить.

			Выводит некоторую информацию о догме:
				Создатель
				Дата создания
				Название

			Возвращает:
				{no}: Если догмы с таким названием не существует.
		'''
		dogma = self.conn.find_item(key = key)
		if not (dogma):
			await ctx.message.add_reaction(self.no)

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

	@commands.command(name = 'радуга', aliases = ['лгбт', 'аслгбт', 'асрадуга', 'rainbow', 'asrainbow', 'aslgbt', 'lgbt'], brief = 'Отправляет в чат случайную догму.')
	async def asrainbow(self, ctx):
		'''
			Использование: `{prefix}радуга`
			Синонимы: {aliases}

			{param} Не принимает аргументов.

			Выбирает случайную догму из списка существующих, отправляет её в чат, а так же информацию о ней (`{prefix}догма_инфо`)

			Ничего дополнительно не возвращает.
		'''
		dogma = random.choice(self.conn.db.all())

		await self.asdogma_info(ctx, dogma['key'])
		await self.asdogma(ctx, dogma['key'])

	@commands.command(name = 'делит', aliases = ['delete', 'asdelete', 'асделит'], hidden = True, brief = 'Удаляет догму.')
	async def asdelete(self, ctx, key):
		'''
			Использование: `{prefix}делит <название>`
			Синонимы: {aliases}
				{param} <название> - название догмы, которую вы хотите удалить.

			Удаляет догму. Да, насовсем.

			Возвращает:
				{no}: Если догма, которую вы пытаетесь удалить, не существует.
				{yes}: При успешном выполнении команды.
		'''
		dogma = self.conn.find_item(key = key)
		if not (dogma):
			await ctx.message.add_reaction(self.no)

		else:
			self.conn.delete_item(key = key)
			if (dogma.get('img')):
				os.remove(dogma['img'])

			await ctx.message.add_reaction(self.yes)

			await utils.update_presence(self.bot)


def setup(bot):
	bot.add_cog(DogmasCog(bot))