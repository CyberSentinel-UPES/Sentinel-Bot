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
    if check_channel(ctx, 'bot-commands'):
        emb = discord.Embed(
            title='Ping',
            description=f'{round(bot.latency*1000)} ms',
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
async def invite(ctx, age, uses, reason=''):
    if check_channel(ctx, 'bot-commands'):
        link = await ctx.channel.create_invite(max_age=int(age), max_uses=int(uses), reason=reason)
        emb = discord.Embed(
            title='Link Created',
            description=f'Max Age: {age}\nMax Uses: {uses}\nReason: {reason}\nLink: {link}',
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
        allowed_roles = ['core-team', 'sentinels']
        if check_role_user(user, allowed_roles):
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
                description='This role cannot be kicked.',
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

# help command 
@bot.command(name='help')
async def _help(ctx):
    emb = discord.Embed(
        title='List Of Commands',
        description='''1. `,ping`
A command that shows the latency of the bot.

2. `,clear`
A command to clear messages.
Usage: `~clear <amount>(including this line)`

3. `,invite`
A command to create an invite.
Usage: `~invite <AGE>(In seconds) <USES>(In integer) <REASON>(optional)`

4. `,kick`
A command to kick a member.
Usage: `~kick <mention member>`

5. `,help`
Display this help message''',
        color=1040190
    )
    await ctx.send(embed=emb)


# test command
@bot.command()
async def test(ctx, user: discord.Member):
    await ctx.send(f'{str(discord.utils.get(user.roles, name="admins"))}')

if __name__ == '__main__':
    bot.run('ODA1NDQyMjgwNjgwNTg3MzQ1.YBa8lA.QcdiGWMe50Hz6m6WjIzZtqKjmQQ')
