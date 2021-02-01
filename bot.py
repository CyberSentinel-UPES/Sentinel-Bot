import discord
from discord.ext import commands

# command prefix
bot = commands.Bot(command_prefix=',')
bot.remove_command('help')

# check for bot-commands channel
def check_channel(ctx, channel):
    if str(ctx.message.channel) == channel:
        return True
    else:
        return False

# check author role
def check_role(ctx, roles):
    for role in roles:
        if str(discord.utils.get(ctx.author.roles, name=role)) == role:
            return True
    return False

# check user role
def check_role_user(user, roles):
    for role in roles:
        if str(discord.utils.get(user.roles, name=role)) == role:
            return True
    return Flase

# when bot is ready
@bot.event
async def on_ready():
    print('Bot Ready!!')

# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(
            title='Command Not Found',
            description='404, Not Found\nRun `,help` to list all commands.',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Error',
            description='An unknown error occured\nPlease refer to `,help`',
            color=1040190
        )
        await ctx.send(embed=emb)

# check the latency of the bot
@bot.command()
async def ping(ctx):
    emb = discord.Embed(
        title='Ping',
        description=f'{round(bot.latency*1000)} ms',
        color=1040190
    )
    await ctx.send(embed=emb)

# to clear some ammount of messages
@bot.command()
async def clear(ctx,amount=1):
    allowed_roles = ['admins', 'heads', 'sensei']
    if check_role(ctx, allowed_roles):
        await ctx.channel.purge(limit=amount)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='Inappropriate Role !! :(',
            color=1040190
        )
        await ctx.send(embed=emb)

# generate an invite
@bot.command()
async def invite(ctx, age, uses):
    if check_channel(ctx, 'bot-commands'):
        link = await ctx.channel.create_invite(max_age=int(age), max_uses=int(uses), reason='')
        emb = discord.Embed(
            title='Link Created',
            description=f'Max Age: {age}\nMax Uses: {uses}\nLink: {link}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='Inappropriate Channel !! :(',
            color=1040190
        )
        await ctx.send(embed=emb)

# kick a member
@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, user: discord.Member, reason='No reason specified !!!'):
    allowed_roles = ['sensei', 'heads', 'admins']
    if check_role(ctx, allowed_roles):
        await user.kick(reason=reason)
        emb = discord.Embed(
            title='User Kicked',
            description=f'{user.mention} kicked\nBy: {ctx.message.author.mention}\nReason: {reason}',
            color=1040190
        )
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            title='Not Allowed',
            description='You are not allowed to use this command.',
            color=1040190
        )
        await ctx.send(embed=emb)

# to report a member
@bot.command()
async def report(ctx, user: discord.Member, reason):
    channel_id = discord.utils.get(ctx.guild.channels, name='reports').id
    channel = bot.get_channel(channel_id)
    emb = discord.Embed(
        title='Report',
        color=1040190
    )
    emb.add_field(name='By', value=ctx.message.author.mention, inline=False)
    emb.add_field(name='To', value=user.mention, inline=False)
    emb.add_field(name='Reason', value=reason, inline=False)
    await channel.send(embed=emb)
    emb = discord.Embed(
        title='Successful',
        description='The user was reported successfully.',
        color=1040190
    )
    await ctx.send(embed=emb)

# help command 
@bot.command(name='help')
async def _help(ctx):
    emb = discord.Embed(
        title='List Of Commands',
        color=1040190
    )
    channel = discord.ChannelType
    emb.add_field(name='1. `,help`', value='Display this help message.', inline=False)
    emb.add_field(name='2. `,ping`', value='A command that shows the latency of the bot.', inline=False)
    emb.add_field(name='3. `,clear`', value='A command to clear messages.\nUsage: `,clear <amount>(including this line)`', inline=False)
    emb.add_field(name='4. `,invite`', value='A command to create an invite.\nUsage: `,invite <AGE>(In seconds) <USES>(In integer)`', inline=False)
    emb.add_field(name='5. `,kick`', value='A command to kick a member.\nUsage: `,kick <mention member>`', inline=False)
    emb.add_field(name='6. `,report`', value='A command to report a member.\nUsage: `,report <mention member> <reason>`')
    await ctx.send(embed=emb)

# test command
@bot.command()
async def test(ctx, user: discord.Member):
    await ctx.send(f'{str(discord.utils.get(user.roles, name="admins"))}')

if __name__ == '__main__':
    bot.run('ODA1NDQyMjgwNjgwNTg3MzQ1.YBa8lA.QcdiGWMe50Hz6m6WjIzZtqKjmQQ')
