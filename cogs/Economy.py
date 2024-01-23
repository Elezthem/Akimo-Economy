import disnake
from disnake.ext import commands
from utils.databases import UsersDataBase
from random import *

class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds
        self.author = author
        self.footer = footer
        self.timeout = timeout
        self.page = 0
        super().__init__(timeout=self.timeout)

        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')

    @disnake.ui.button(label='◀️', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == 0:
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1
        else:
            return

        await self.button_callback(interaction)

    @disnake.ui.button(label='▶️', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:
                self.page = 0
            else:
                self.page += 1
        else:
            return

        await self.button_callback(interaction)

    async def button_callback(self, interaction):
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)
        

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='баланс', description='Посмотреть баланс')
    async def balance(self, interaction, member: disnake.Member = None):
        await self.db.create_table()
        if not member:
            member = interaction.author
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        embed = disnake.Embed(color=0x2F3136, title=f'Баланс пользователя - {member}')
        embed.add_field(name='🪙 Монеты', value=f'```{user[1]}```')
        embed.add_field(name='💎 Премиум монеты', value=f'```{user[2]}```')
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    
    @commands.slash_command(name='забрать', description='Забрать деньги у пользователя')
    @commands.has_permissions(administrator=True)
    async def give(self, interaction, member: disnake.Member,
                   amount: int, arg=commands.Param(choices=['монеты', 'премиум монеты'])):
        await self.db.create_table()
        await self.db.add_user(member)
        if arg == 'монеты':
            await self.db.update_money(member, -amount, 0)
            embed = disnake.Embed(color=0x2F3136, title=f'Изъятие монет у пользователя - {member}')
            embed.description = f'Администратор {interaction.author.mention} забрал монеты у {member.mention} {amount} монет.'
            embed.set_thumbnail(url=member.display_avatar.url)
        else:
            await self.db.update_money(member, 0, -amount)
            embed = disnake.Embed(color=0x2F3136, title=f'Изъятие монет у пользователя - {member}')
            embed.description = f'Администратор {interaction.author.mention} забрал премиум монеты у {member.mention} {amount} премиум монет.'
            embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='выдать', description='Выдать деньги пользователю')
    @commands.has_permissions(administrator=True)
    async def give(self, interaction, member: disnake.Member,
                   amount: int, arg=commands.Param(choices=['монеты', 'премиум монеты'])):
        await self.db.create_table()
        await self.db.add_user(member)
        if arg == 'монеты':
            await self.db.update_money(member, amount, 0)
            embed = disnake.Embed(color=0x2F3136, title=f'Выдача монет пользователю - {member}')
            embed.description = f'Пользователь {interaction.author.mention} выдал {member.mention} {amount} монет.'
            embed.set_thumbnail(url=member.display_avatar.url)
        else:
            await self.db.update_money(member, 0, amount)
            embed = disnake.Embed(color=0x2F3136, title=f'Выдача премиум монет пользователю - {member}')
            embed.description = f'Пользователь {interaction.author.mention} выдал {member.mention} {amount} премиум монет.'
            embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    #@commands.slash_command(name='лайк', description='Лайкнуть пользователя')
    #@commands.has_permissions(administrator=True)
    #async def give(self, interaction, member: disnake.Member):
        #await self.db.create_table()
        #await self.db.add_user(member)
        #await self.db.update_likes(member)
        #embed = disnake.Embed(color=0x2F3136, title=f'Лайк пользователя - {member}')
        #embed.description = f'Пользователь {interaction.author.mention} лайкнул {member.mention} .'
        #embed.set_thumbnail(url=member.display_avatar.url)
        #await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='передать', description='Передать монеты пользователю')
    async def pick_up(self, interaction, member: disnake.Member,
                   amount: int, arg=commands.Param(choices=['монеты', 'премиум монеты'])):
            embed = disnake.Embed(color=0x2F3136, title=f'Передача монет пользователю - {member}')
            embed.description = f'Пользователь {interaction.author.mention} Передал {member.mention} {amount} монет.'
            embed.set_thumbnail(url=member.display_avatar.url)
            await self.db.update_money(interaction.author, -amount, 0)
            await self.db.update_money(member, amount, 0)
            await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='работать', description='Работать')
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def work(self, interaction):
        workmoney = randint(5, 15)
        await self.db.add_user(interaction.author)
        await self.db.update_money(interaction.author, workmoney, 0)
        embed = disnake.Embed(color=0x2F3136, title=f'Работа - {interaction.author}')
        embed.description = f'Пользователь {interaction.author.mention} заработал {workmoney} монет.'
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    

    @commands.slash_command(name='топ', description='Посмотреть топ пользователей')
    async def top(self, interaction):
        await self.db.create_table()
        top = await self.db.get_top()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** {self.bot.get_user(user[0])} - {user[1]} 🪙\n'
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(color=0x2F3136, title='Топ пользователей')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.author, True)
        await interaction.response.send_message(embed=embeds[0], view=view)
        



def setup(bot):
    bot.add_cog(Economy(bot))
