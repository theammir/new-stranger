import discord
import database
import config
from discord.ext import commands

class BackupCog(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
         self.conn = database.Instance(config.DB_NAME)

    @commands.is_owner()
    @commands.command(name = 'all_dogmas')
    async def all_dogmas(self, ctx):
        db = self.conn.db.all()
        for db_item in db:
            text = 'Dogma '
            file = None
            text += db_item['key'] + '\n\n'
            text += db_item['message'] if db_item.get('message') else ''
            if (db_item.get('img')):
                file = discord.File(db_item['img'])
            await ctx.send(text, file = file if file else None)

    @commands.is_owner()
    @commands.command(name = 'backup')
    async def dogmas_db(self, ctx, name: str = None):
        if (not name):
            name = config.DB_NAME
        await ctx.send(file = discord.File(name))

def setup(bot):
    bot.add_cog(BackupCog(bot))
