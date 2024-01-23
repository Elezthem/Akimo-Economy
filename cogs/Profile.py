import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase
from random import *


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='профиль', description='Посмотреть профиль')
    async def profile(self, interaction, member: disnake.Member = None):
        await self.db.create_table()
        if not member:
            member = interaction.author
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        embed = disnake.Embed(color=0x2F3136, title=f'Профиль пользователя - {member}')
        embed.add_field(name='🪙 Монеты', value=f'```{user[1]}```')
        embed.add_field(name='💎 Премиум монеты', value=f'```{user[2]}```')
        embed.add_field(name='❤ Лайки', value=f'```{user[3]}```')
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))