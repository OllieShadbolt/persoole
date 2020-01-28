#! /usr/bin/env python3
"""
A python script for running the persoole Discord bot.
"""
import discord
import asyncio

__version__ = '1.0'

client = discord.Client()
latest_message = {}
colours = {
    'default': discord.Colour.default(),
    'teal': discord.Colour.teal(),
    'dark_teal': discord.Colour.dark_teal(),
    'green': discord.Colour.green(),
    'dark_green': discord.Colour.dark_green(),
    'blue': discord.Colour.blue(),
    'dark_blue': discord.Colour.dark_blue(),
    'purple': discord.Colour.purple(),
    'dark_purple': discord.Colour.dark_purple(),
    'magenta': discord.Colour.magenta(),
    'dark_magenta': discord.Colour.dark_magenta(),
    'gold': discord.Colour.gold(),
    'dark_gold': discord.Colour.dark_gold(),
    'orange': discord.Colour.orange(),
    'dark_orange': discord.Colour.dark_orange(),
    'red': discord.Colour.red(),
    'dark_red': discord.Colour.dark_red(),
    'lighter_gray': discord.Colour.lighter_grey(),
    'dark_grey': discord.Colour.dark_grey(),
    'light_grey': discord.Colour.light_grey(),
    'darker_grey': discord.Colour.darker_grey(),
    'blurple': discord.Colour.blurple(),
    'greyple': discord.Colour.greyple(),
}


class Content:
    """
    Common content strings.
    """
    interrupt = "Send anything to interrupt these messages."
    error_suffix = " Type \"help\" for more."
    hex_prefix = "Hex Value: "
    confirmation = "Done!"


def test_role(role, member):
    """
    Test if the given role is a valid personal role for the given member.
    """
    return (
        role.members == [member] and role.position <
        role.guild.get_member(client.user.id).roles[-1].position
    )


def test_latest_message(member_id, message_id):
    """
    Test if the given message id is the latest for the given member id.
    """
    return latest_message[member_id] == message_id


def get_role(role_id):
    """
    Returns a role with the given ID.
    """
    for guild in client.guilds:
        role = guild.get_role(role_id)
        if role is not None:
            return role


@client.event
async def on_message(message):
    if (
        message.channel.type != discord.ChannelType.private or
        message.author == client.user
    ):
        return

    latest_message[message.author.id] = message.id
    await message.author.trigger_typing()
    await asyncio.sleep(1)

    if not test_latest_message(message.author.id, message.id):
        return

    args = message.content.split(' ')

    if args[0].lower() == 'help':
        if len(args) == 1:
            await message.author.send(
                "_ _\n"
                "Your message must be formatted like this:\n"
                "> [**Role ID**] [**Colour**] [**Name**]\n\n"
                "For example:\n"
                "> **987654321987654321 ffffff My Role Name**\n\n"
                "Type \"**help roles**\" to get your role IDs.\n"
                "Colour can either be a hex value or a colour name.\n"
                "Type \"**help colours**\" (or \"**help colors**\") "
                "to get all acceptable colour names.\n"
                "Name is optional."
            )
            return

        elif len(args) == 2:
            help_arg = args[1].lower()
            if help_arg in ['colors', 'colours']:
                for key in colours.keys():

                    colour = colours[key]
                    embed = discord.Embed(
                        colour=colour,
                        description=Content.hex_prefix + str(colour)[1:]
                    )
                    embed.set_author(name=key)

                    await message.author.send(
                        "> " + Content.interrupt, embed=embed
                    )
                    await message.author.trigger_typing()
                    await asyncio.sleep(1)

                    if not test_latest_message(message.author.id, message.id):
                        return

                await message.author.send(Content.confirmation)
                return

            if help_arg == 'roles':
                for guild in client.guilds:
                    member = guild.get_member(message.author.id)
                    if member is None:
                        continue

                    for role in member.roles[1:]:
                        if not test_role(role, member):
                            continue

                        embed = discord.Embed(
                            title=role.name,
                            description=(
                                Content.hex_prefix + str(role.color)[1:]
                            ),
                            colour=role.colour
                        )
                        embed.set_author(
                            name="Role ID above. " + Content.interrupt
                        )
                        embed.set_footer(text=guild.name)

                        await message.author.send(
                            "> %s" % (role.id), embed=embed
                        )
                        await message.author.trigger_typing()
                        await asyncio.sleep(1)

                        if not test_latest_message(
                            message.author.id, message.id
                        ):
                            return

                await message.author.send(Content.confirmation)
                return

        await message.author.send("Invalid option." + Content.error_suffix)
        return

    try:
        role = get_role(int(args[0]))

    except ValueError:
        role = None

    if role is None or not test_role(role, message.author):
        await message.author.send("Invalid role ID." + Content.error_suffix)
        return

    if len(args) == 1:
        await message.author.send("No colour provided." + Content.error_suffix)
        return

    colour_arg = args[1].lower()

    if colour_arg in colours:
        colour = colours[colour_arg]
    else:
        try:
            colour = discord.Colour(int(args[1], 16))

        except ValueError:
            await message.author.send("Invalid colour." + Content.error_suffix)
            return

    try:
        if len(args) == 2:
            await role.edit(colour=colour)

        else:
            await role.edit(colour=colour, name=' '.join(args[2:]))

        content = Content.confirmation

    except discord.Forbidden:
        content = "I do not have permissions to change the role."

    except discord.HTTPException:
        content = "Editing the role failed."

    await message.author.send(content)


def main():
    client.run('xxx')


if __name__ == '__main__':
    main()
