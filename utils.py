import config
import discord
import database

def get_length(file: str) -> int:
    if ('__pycache__' not in file and '.' in file):
        with open(file, 'r', encoding = 'utf-8') as f:
            return len(list(filter(lambda i: i not in ['\n', ''] and not i.startswith('#'), f.readlines())))
    else:
        return 0

def get_activity():
	conn = database.Instance(config.DB_NAME)
	dogmas_count = len(conn.db.all())
	word = ''
	if (str(dogmas_count).endswith('1')):
		word = 'догму'
	elif (str(dogmas_count).endswith(('2', '3', '4'))):
		word = 'догмы'
	elif (str(dogmas_count).endswith(('0', '5', '6', '7', '8', '9'))):
		word = 'догм'

	return discord.Activity(type = discord.ActivityType.watching, name = f"на {dogmas_count} {word}")
			
async def update_presence(bot):
	await bot.change_presence(activity = get_activity())