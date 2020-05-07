import re
import secrets
from datetime import datetime, timedelta
from typing import Union

import discord
from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.commands import Context
from redbot.core.i18n import cog_i18n, Translator
from redbot.core.utils.menus import (
    DEFAULT_CONTROLS, menu, start_adding_reactions
)
from redbot.core.utils.predicates import ReactionPredicate

from .bothelp import TvMHelpFormatter
from .utils import (
    TvMCommandFailure,
    tvmset_lock,
    if_host_or_admin,
    if_player_and_spec_roles_exist,
    if_player_role_exists,
    if_player_and_dead_roles_exist,
    if_repl_role_exists,
    if_in_private_channel,
    if_game_started
)

_ = Translator("TvM", __file__)

default_guild = {
    "host_id": None,
    "player_id": None,
    "spec_id": None,
    "dead_id": None,  # dead player role
    "repl_id": None,  # replacement role
    "signup_channel": None,
    "na_channel_id": None,
    "can_change_na": True,
    "tvmset_lock": False,
    "signups_on": True,
    "total_players": 12,
    "signed": 0,
    "na_submitted": [],
    "cycle": {
        "number": 0,
        "day": None,
        "vote": None,
        "night": None
    }
}

default_member = {
    "notes": [
        # structure of a note
        # {
        #     "note": None,
        #     "reason": None
        # }
    ]
}

CHECK_MARK = "\N{WHITE HEAVY CHECK MARK}"

VOTE_RE = re.compile(r"[\*_~|]*[Vv][Tt][Ll][\*_~|]* ([^\s\*_~|]+)")
UN_VOTE_RE = re.compile(
    r"[\*_~|]*[Uu][Nn]-?[Vv][Tt][Ll][\*_~|]*\s?([^\s\*_~|]+)?"
)
NO_VOTE_RE = re.compile(r"[\*_~|]*[Vv][Tt][Nn][Ll][\*_~|]*")

__version__ = "1.2.0"

old_invite = None


@cog_i18n(_)
class TvM(commands.Cog):
    """Set up the bot for your server by following the quickstart guide:
    \r https://ariusx7.github.io/tvm-assistant/quickstart
    """

    def __init__(self, bot: Red):
        self.bot = bot

        self.config = Config.get_conf(
            self, "1_177_021_220", force_registration=True
        )
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)

        self.bot._help_formatter = TvMHelpFormatter(self.bot)

    @commands.group(name="tvm")
    @if_host_or_admin()
    @commands.guild_only()
    async def _tvm(self, ctx: Context):
        """Set various roles, channels, etc."""

        if not ctx.invoked_subcommand:
            pass

    @_tvm.command(name="hostrole")
    @tvmset_lock()
    async def _role_host(self, ctx: Context, *, role: discord.Role):
        """Set the host role."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set `{}` as host role?"
            ).format(role.name)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).host_id.set(role.id)
            await ctx.send(_("Set `{}` as host role!").format(role.name))
        else:
            await ctx.send(_("Aborted host role setup."))

    @_tvm.command(name="playerrole")
    @tvmset_lock()
    async def _role_player(self, ctx: Context, *, role: discord.Role):
        """Set the player role."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set `{}` as player role?"
            ).format(role.name)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).player_id.set(role.id)
            await ctx.send(_("Set `{}` as player role!").format(role.name))
        else:
            await ctx.send(_("Aborted player role setup."))

    @_tvm.command(name="specrole", aliases=["spectatorrole"])
    @tvmset_lock()
    async def _role_spec(self, ctx: Context, *, role: discord.Role):
        """Set the spectator role."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set `{}` as spectator role?"
            ).format(role.name)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).spec_id.set(role.id)
            await ctx.send(_("Set `{}` as spectator role!").format(role.name))
        else:
            await ctx.send(_("Aborted spectator role setup."))

    @_tvm.command(name="deadrole")
    @tvmset_lock()
    async def _role_dead(self, ctx: Context, *, role: discord.Role):
        """Set the dead player role."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set `{}` as dead role?"
            ).format(role.name)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).dead_id.set(role.id)
            await ctx.send(_("Set `{}` as dead role!").format(role.name))
        else:
            await ctx.send(_("Aborted dead role setup."))

    @_tvm.command(name="replrole")
    @tvmset_lock()
    async def _role_repl(self, ctx: Context, *, role: discord.Role):
        """Set the replacement role."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set `{}` as replacement role?"
            ).format(role.name)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).repl_id.set(role.id)
            await ctx.send(
                _("Set `{}` as replacement role!").format(role.name)
            )
        else:
            await ctx.send(_("Aborted replacement role setup."))

    @_tvm.command(name="setroles")
    @tvmset_lock()
    async def _set_roles(self, ctx: Context):
        """Set up all 5 required roles."""

        guild: discord.Guild = ctx.guild

        host = await guild.create_role(
            name="Host", colour=discord.Color(0xFFBF37),
            hoist=True, mentionable=True
        )
        await self.config.guild(guild).host_id.set(host.id)
        await ctx.author.add_roles(host)

        player = await guild.create_role(
            name="Player", colour=discord.Color(0x37BFFF),
            hoist=True, mentionable=True
        )
        await self.config.guild(guild).player_id.set(player.id)

        repl = await guild.create_role(
            name="Replacement", colour=discord.Color(0x86FF40)
        )
        await self.config.guild(guild).repl_id.set(repl.id)

        spec = await guild.create_role(
            name="Spectator", colour=discord.Color(0xD837FF)
        )
        await self.config.guild(guild).spec_id.set(spec.id)

        dead = await guild.create_role(
            name="Dead", colour=discord.Color(0xDC5757)
        )
        await self.config.guild(guild).dead_id.set(dead.id)

        txt = _(
            "Host: {}"
            "\nPlayer: {}"
            "\nSpectator: {}"
            "\nDead: {}"
            "\nReplacement: {}"
        ).format(
            host.mention,
            player.mention,
            spec.mention,
            dead.mention,
            repl.mention
        )

        embed = discord.Embed(
            color=0x37BFFF, title="Created Roles!", description=txt
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("Set up required roles!")

    @_tvm.command(name="signup")
    @tvmset_lock()
    async def _signup_channel(
        self, ctx: Context, *, channel: discord.TextChannel
    ):
        """Set sign-ups channel."""

        msg = await ctx.send(
            _(
                "Are you sure you want to set {} as sign-ups channel?"
            ).format(channel.mention)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if pred.result:
            await self.config.guild(ctx.guild).signup_channel.set(channel.id)
            await ctx.send(
                _("Set as {} sign-ups channel!").format(channel.mention)
            )
        else:
            await ctx.send(_("Aborted sign-ups channel setup."))

    @_tvm.command(name="nachannel")
    @tvmset_lock()
    async def _na_channel(self, ctx: Context, *, channel: discord.TextChannel):
        """Set channel for the bot to send night actions."""

        await self.config.guild(ctx.guild).na_channel_id.set(channel.id)

        await ctx.message.add_reaction(CHECK_MARK)

    @_tvm.command(name="hostchannel")
    @tvmset_lock()
    async def _host_channel(self, ctx: Context, *, channel: discord.TextChannel):
        """Create host channel."""

        guild: discord.Guild = ctx.guild

        host_role = await self.role_from_config(guild, "host_id")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            host_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                add_reactions=True
            )
        }

        host_channel = await guild.create_text_channel(
            "host", overwrites=overwrites
        )

        await ctx.send(_("Created {} channel for hosts.").format(host_channel.mention))

    @_tvm.command(name="setchannels")
    @tvmset_lock()
    async def _set_channels(self, ctx: Context):
        """Set up all required channels."""

        guild: discord.Guild = ctx.guild

        signup = await guild.create_text_channel("sign-ups")
        await self.config.guild(guild).signup_channel.set(signup.id)

        host_role = await self.role_from_config(guild, "host_id")

        na_overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            host_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }

        nightaction = await guild.create_text_channel(
            "night-action", overwrites=na_overwrites
        )
        await self.config.guild(guild).na_channel_id.set(nightaction.id)

        txt = _(
            "Sign-ups: {}\nNight Actions: {}"
        ).format(
            signup.mention, nightaction.mention,
        )

        embed = discord.Embed(
            color=0x37BFFF, title="Created Channels!", description=txt
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("Created required channels!")
            await ctx.send(txt)

    @_tvm.command(name="changena")
    @tvmset_lock()
    async def _can_change_na(self, ctx: Context):
        """Toggle `Can Change NA` setting."""

        old = await self.config.guild(ctx.guild).can_change_na()
        new = False if old else True

        await self.config.guild(ctx.guild).can_change_na.set(new)

        await ctx.send(_("Changed `Can Change NA` to `{}`.").format(new))

    @_tvm.command(name="total")
    @tvmset_lock()
    async def _total_players(self, ctx: Context, number: int):
        """Set total number of players."""

        await self.config.guild(ctx.guild).total_players.set(number)

        await ctx.send(_("Set total players to `{}`.").format(number))

    @_tvm.command(name="lock")
    @tvmset_lock()
    async def _lock_settings(self, ctx: Context):
        """Lock TvM settings."""

        await self.config.guild(ctx.guild).tvmset_lock.set(True)

        await ctx.message.add_reaction(CHECK_MARK)

    @_tvm.command(name="unlock")
    async def _unlock_settings(self, ctx: Context):
        """Unlock TvM settings."""

        await self.config.guild(ctx.guild).tvmset_lock.set(False)

        await ctx.message.add_reaction(CHECK_MARK)

    @_tvm.command(name="signclose")
    @tvmset_lock()
    async def _close_sign_ups(self, ctx: Context):
        """Close sign-ups."""

        await self.config.guild(ctx.guild).signups_on.set(False)

        await ctx.message.add_reaction(CHECK_MARK)

    @_tvm.command(name="signopen")
    @tvmset_lock()
    async def _open_sign_ups(self, ctx: Context):
        """Open sign-ups."""

        await self.config.guild(ctx.guild).signups_on.set(True)

        await ctx.message.add_reaction(CHECK_MARK)

    @_tvm.command(name="settings", aliases=["show"])
    async def _show_settings(self, ctx: Context):
        """Show all the TvM settings."""

        guild: discord.Guild = ctx.guild

        host = await self.config.guild(guild).host_id()
        if host:
            host = discord.utils.get(guild.roles, id=host).mention
        else:
            host = f"`{host}`"

        player = await self.config.guild(guild).player_id()
        if player:
            player = discord.utils.get(guild.roles, id=player).mention
        else:
            player = f"`{player}`"

        spec = await self.config.guild(guild).spec_id()
        if spec:
            spec = discord.utils.get(guild.roles, id=spec).mention
        else:
            spec = f"`{spec}`"

        dead = await self.config.guild(guild).dead_id()
        if dead:
            dead = discord.utils.get(guild.roles, id=dead).mention
        else:
            dead = f"`{dead}`"

        repl = await self.config.guild(guild).repl_id()
        if repl:
            repl = discord.utils.get(guild.roles, id=repl).mention
        else:
            repl = f"`{repl}`"

        signup = await self.config.guild(guild).signup_channel()
        if signup:
            signup = discord.utils.get(guild.text_channels, id=signup).mention
        else:
            signup = f"`{signup}`"

        na_ch = await self.config.guild(guild).na_channel_id()
        if na_ch:
            na_ch = discord.utils.get(guild.text_channels, id=na_ch).mention
        else:
            na_ch = f"`{na_ch}`"

        can_change_na = await self.config.guild(guild).can_change_na()

        lock = await self.config.guild(guild).tvmset_lock()

        sign_ups = await self.config.guild(guild).signups_on()

        total = await self.config.guild(guild).total_players()

        signed = await self.config.guild(guild).signed()

        txt = _(
            "Host Role: {}"
            "\nPlayer Role: {}"
            "\nSpectator Role: {}"
            "\nDead Player Role: {}"
            "\nReplacement Role: {}"
            "\nSign-ups Channel: {}"
            "\nNight Action Channel: {}"
            "\nCan Change NA: `{}`"
            "\nTvM Settings Lock: `{}`"
            "\nSign-ups Open: `{}`"
            "\nTotal Players: `{}`"
            "\nSign-ups: `{}`"
        ).format(
            host, player, spec, dead, repl, signup, na_ch,
            can_change_na, lock, sign_ups, total, signed
        )

        embed = discord.Embed(
            color=0xAF70FF, title="TvM Settings", description=txt
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(
                _(
                    "I don't have permission to embed messages."
                    " Please give me the permission!"
                )
            )

    @commands.command(name="in")
    @commands.guild_only()
    @if_player_and_spec_roles_exist()
    async def _sign_in(self, ctx: Context, *, ignored: str = None):
        """Sign up for the TvM!"""

        guild: discord.Guild = ctx.guild
        channel: discord.TextChannel = ctx.channel
        author: discord.Member = ctx.author

        if not await self.config.guild(guild).signups_on():
            return await ctx.send(_("Sign-ups are closed!"))

        if not await self.check_total(guild):
            return await ctx.send(_("Maximum allowed players signed up!"))

        if await self.config.guild(guild).signup_channel() == channel.id:
            player_id = await self.config.guild(guild).player_id()
            player_role = discord.utils.get(guild.roles, id=player_id)

            if player_role not in author.roles:
                try:
                    await author.add_roles(player_role)
                    await self.update_total(ctx, override=1)
                except discord.Forbidden:
                    return await ctx.send(
                        _(
                            "I either don't have permissions to manage"
                            " roles or the `{}` role is above my highest role!"
                        ).format(player_role.name)
                    )

            await self.remove_extra_roles(ctx, ["spec", "repl"])

            await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="spec", aliases=["out", "spectator"])
    @commands.guild_only()
    @if_player_and_spec_roles_exist()
    async def _sign_out(self, ctx: Context, *, ignored: str = None):
        """Spec the TvM!"""

        guild: discord.Guild = ctx.guild
        channel: discord.TextChannel = ctx.channel
        author: discord.Member = ctx.author

        if not await self.config.guild(guild).signups_on():
            await ctx.send(_("You can't sign-out now. Contact the host."))
            return

        if await self.config.guild(guild).signup_channel() == channel.id:
            spec_id = await self.config.guild(guild).spec_id()
            spec_role = discord.utils.get(guild.roles, id=spec_id)

            if spec_role not in author.roles:
                try:
                    await author.add_roles(spec_role)
                except discord.Forbidden:
                    return await ctx.send(
                        _(
                            "I either don't have permissions to manage"
                            " roles or the `{}` role is above my highest role!"
                        ).format(spec_role.name)
                    )

            await self.update_total(ctx)

            await self.remove_extra_roles(ctx, ["player", "repl"])

            await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="repl", aliases=["replace", "replacement"])
    @commands.guild_only()
    @if_repl_role_exists()
    async def _sign_repl(self, ctx: Context, *, ignored: str = None):
        """Sign-up as a replacement!"""

        guild: discord.Guild = ctx.guild
        channel: discord.TextChannel = ctx.channel
        author: discord.Member = ctx.author

        if not await self.config.guild(guild).signups_on():
            return await ctx.send(
                _("You can't sign up as replacement now. Contact the host.")
            )

        if await self.config.guild(guild).signup_channel() == channel.id:
            repl_id = await self.config.guild(guild).repl_id()
            repl_role = discord.utils.get(guild.roles, id=repl_id)

            if repl_role not in author.roles:
                try:
                    await author.add_roles(repl_role)
                except discord.Forbidden:
                    return await ctx.send(
                        _(
                            "I either don't have permissions to manage"
                            " roles or the `{}` role is above my highest role!"
                        ).format(repl_role.name)
                    )

            await self.update_total(ctx)

            await self.remove_extra_roles(ctx, ["player", "spec"])

            await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(aliases=["randomise", "randomize"])
    @commands.guild_only()
    @if_host_or_admin()
    @if_player_role_exists()
    async def rand(self, ctx: Context, *, roles: str):
        """Randomly assign specified roles to people with `Player` role.

        Number of roles should be equal to number of players.
        """

        guild: discord.Guild = ctx.guild

        # players = [x.strip() for x in players.split(",") if x.strip() != ""]
        player_role = guild.get_role(
            await self.config.guild(guild).player_id()
        )
        players = [
            member for member in guild.members if player_role in member.roles
        ]
        roles = [y.strip() for y in roles.split(",") if y.strip() != ""]

        if len(players) != len(roles):
            return await ctx.send(
                _("Number of players is not equal to number of roles.")
            )

        result = ""

        for player in players:
            role = secrets.choice(roles)
            roles.remove(role)

            result += _("\n**{}:** {}").format(player, role)

        await ctx.send(result)

    @commands.command(name="playerchats", aliases=["pc"])
    @commands.guild_only()
    @if_host_or_admin()
    async def _player_chats(self, ctx: Context, *, cat_name="Private Chats"):
        """Create private channels for users with player role.

        You can specify category name for the player channels. If not
        specified, "Players Chats" will be used as default.
        """

        guild: discord.Guild = ctx.guild

        cat_ow = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            )
        }

        try:
            chats = await guild.create_category(
                cat_name, overwrites=cat_ow
            )
        except discord.Forbidden:
            await ctx.send(_("I don't have permissions to create a channel!"))
            return

        player_id = await self.config.guild(guild).player_id()
        player_role = discord.utils.get(guild.roles, id=player_id)

        for member in guild.members:
            if player_role not in member.roles:
                continue

            channel_name = member.name.replace(" ", "-")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                member: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    embed_links=True,
                    read_message_history=True,
                    attach_files=True
                ),
                guild.me: discord.PermissionOverwrite(
                    read_messages=True,
                    add_reactions=True
                )
            }

            await chats.create_text_channel(
                channel_name, overwrites=overwrites
            )

        await ctx.send(_("Created player channels!"))

    @commands.command(name="mafiachat", aliases=["mafchat"])
    @commands.guild_only()
    @if_host_or_admin()
    async def _mafia_chat(self, ctx: Context, *mafias: discord.Member):
        """Create a mafia chat."""

        guild: discord.Guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            )
        }

        for user in mafias:
            overwrites[user] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )

        channel = await guild.create_text_channel(
            "mafia-chat", overwrites=overwrites
        )

        await ctx.send(_("Created {}!").format(channel.mention))

    @commands.command(name="nightaction", aliases=["na"])
    @commands.guild_only()
    @if_in_private_channel()
    async def _night_action(self, ctx: Context, *, action: str):
        """Submit your night action!"""

        author = ctx.author
        guild = ctx.guild

        if author.name[-1].lower() == "s":
            name = f"{author.name}'"
        else:
            name = f"{author.name}'s"

        title = _("{} Night Action").format(name)

        async with self.config.guild(guild).na_submitted() as submitted:
            if author.id in submitted:
                if not await self.config.guild(guild).can_change_na():
                    return await ctx.send(
                        _("You've already submitted a night action!")
                    )
                else:
                    title += _(" (Updated)")

        na_channel = await self.check_na_channel(guild)

        if not na_channel:
            na_channel = await self.create_na_channel(guild)

        await na_channel.send(_("**{}**\n{}").format(title, action))

        async with self.config.guild(guild).na_submitted() as submitted:
            if author.id not in submitted:
                submitted.append(author.id)

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="host")
    @commands.guild_only()
    @if_host_or_admin()
    async def _make_host(self, ctx: Context, *, user: discord.Member):
        """Make the specified user a host!"""

        guild: discord.Guild = ctx.guild

        host_id = await self.config.guild(guild).host_id()
        role: discord.Role = discord.utils.get(guild.roles, id=host_id)

        try:
            await user.add_roles(role)
        except discord.Forbidden:
            return await ctx.send(
                _(
                    "I either don't have permissions to manage"
                    " roles or the `{}` role is above my highest role!"
                ).format(role.name)
            )

        await ctx.send(_("Made `{}` a host!").format(user.display_name))

    @commands.command(name="specchat")
    @commands.guild_only()
    @if_host_or_admin()
    async def _spec_chat(
        self, ctx: Context, *, channel: discord.TextChannel = None
    ):
        """Create spectator chat or fix permissions of an existing channel."""

        guild: discord.Guild = ctx.guild

        if not channel:
            channel = await guild.create_text_channel("spec-chat")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            )
        }

        visible_roles = []

        host_id = await self.config.guild(guild).host_id()
        if host_id:
            visible_roles.append(
                discord.utils.get(guild.roles, id=host_id)
            )

        spec_id = await self.config.guild(guild).spec_id()
        if spec_id:
            visible_roles.append(
                discord.utils.get(guild.roles, id=spec_id)
            )

        dead_id = await self.config.guild(guild).dead_id()
        if dead_id:
            visible_roles.append(
                discord.utils.get(guild.roles, id=dead_id)
            )

        for role in visible_roles:
            overwrites[role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )

        await channel.edit(overwrites=overwrites)

    @commands.command(name="cycle")
    @commands.guild_only()
    @if_host_or_admin()
    @if_player_role_exists()
    async def _create_cycle(self, ctx: Context, number: int = None):
        """Create a category for a cycle with day, votes and night channels."""

        guild: discord.Guild = ctx.guild

        if not number:
            number = (
                await self.config.guild(guild).get_raw("cycle", "number") + 1
            )

        msg = await ctx.send(
            _(
                "Are you sure you want to create cycle `{}` channels? Make"
                " sure you have the day text ready. Users will be able to talk"
                " in the day and vote channels as soon as they are created."
            ).format(number)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if not pred.result:
            return await ctx.send(_("Process aborted."))

        player_id = await self.config.guild(guild).player_id()
        player_role = discord.utils.get(guild.roles, id=player_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False
            ),
            player_role: discord.PermissionOverwrite(
                send_messages=True,
                attach_files=False
            ),
            guild.me: discord.PermissionOverwrite(
                send_messages=True,
                embed_links=True
            )
        }

        cycle_category = await guild.create_category_channel(
            f"Cycle {number}", overwrites=overwrites
        )

        day = await cycle_category.create_text_channel(f"day-{number}")
        vote = await cycle_category.create_text_channel(f"day-{number}-votes")

        night_overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True
            )
        }

        night = await cycle_category.create_text_channel(
            f"night-{number}", overwrites=night_overwrites
        )

        await self.config.guild(guild).na_submitted.clear()

        async with self.config.guild(guild).cycle() as cycle:
            cycle["number"] = number
            cycle["day"] = day.id
            cycle["vote"] = vote.id
            cycle["night"] = night.id

        await ctx.send(_("Created cycle {} channels!").format(number))

    @commands.command(name="night")
    @commands.guild_only()
    @if_host_or_admin()
    @if_player_role_exists()
    async def _night(self, ctx: Context):
        """Close day channels and open night channel."""

        guild: discord.Guild = ctx.guild

        data = await self.config.guild(guild).all()

        cycle = data['cycle']

        number = cycle['number']

        msg = await ctx.send(
            _(
                "Are you sure you want to start night {}? Make sure you"
                " have already posted the night starting text."
            ).format(number)
        )
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)

        if not pred.result:
            return await ctx.send(_("Process aborted."))

        day = guild.get_channel(cycle['day'])
        vote = guild.get_channel(cycle['vote'])
        night = guild.get_channel(cycle['night'])

        night_overwrites = day.overwrites
        day_overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False,
                add_reactions=False,
            )
        }

        await day.edit(overwrites=day_overwrites)
        await vote.edit(overwrites=day_overwrites)
        await night.edit(overwrites=night_overwrites)

        na_channel = await self.check_na_channel(guild)
        if not na_channel:
            na_channel = await self.create_na_channel(guild)

        try:
            await na_channel.send(
                _("**Night {} begins!**\n\n\n\n\u200b").format(number)
            )
        except discord.Forbidden:
            pass

        await ctx.send(_("Night {} channel opened.").format(number))

    @commands.command(name="kill")
    @commands.guild_only()
    @if_host_or_admin()
    @if_player_and_dead_roles_exist()
    async def _kill_player(self, ctx: Context, *, user: discord.Member):
        """Kill player by removing player role and adding dead player role."""

        guild = ctx.guild

        player_id = await self.config.guild(guild).player_id()
        player_role = discord.utils.get(guild.roles, id=player_id)

        if player_role not in user.roles:
            return await ctx.send(_("User doesn't have player role."))

        try:
            await user.remove_roles(player_role)
        except discord.Forbidden:
            return await ctx.send(
                        _(
                            "I either don't have permissions to manage"
                            " roles or the `{}` role is above my highest role!"
                        ).format(player_role.name)
                    )

        dead_id = await self.config.guild(guild).dead_id()
        dead_role = discord.utils.get(guild.roles, id=dead_id)

        await user.add_roles(dead_role)

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="synctotal")
    @commands.guild_only()
    @if_host_or_admin()
    @if_player_role_exists()
    async def _sync_total(self, ctx: Context):
        """Remove discrepancy between counted and actual sign-ups."""

        guild = ctx.guild

        player_id = await self.config.guild(guild).player_id()
        player_role = discord.utils.get(guild.roles, id=player_id)

        signed = len([
            user.id for user in guild.members
            if player_role in user.roles
        ])

        await self.config.guild(guild).signed.set(signed)

        await ctx.send(_("Synced total number of signed-up players."))

    @commands.group(name="clear")
    @commands.guild_only()
    @if_host_or_admin()
    async def _clear(self, ctx: Context):
        """Clear various database settings."""

        if not ctx.invoked_subcommand:
            pass

    @_clear.command(name="nasubmitted")
    async def _clear_na_submitted(self, ctx: Context):
        """Clear the list of users who have submitted the NA this cycle."""

        await self.config.guild(ctx.guild).na_submitted.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="player")
    async def _clear_player(self, ctx: Context):
        """Remove the player role from database."""

        await self.config.guild(ctx.guild).player_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="spec", aliases=["spectator"])
    async def _clear_spec(self, ctx: Context):
        """Remove the spectator role from database."""

        await self.config.guild(ctx.guild).spec_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="dead")
    async def _clear_dead(self, ctx: Context):
        """Remove the dead player role from database."""

        await self.config.guild(ctx.guild).dead_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="repl", aliases=["replacement"])
    async def _clear_repl(self, ctx: Context):
        """Remove the replacement role from database."""

        await self.config.guild(ctx.guild).repl_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="host")
    async def _clear_host(self, ctx: Context):
        """Remove the host role from database."""

        await self.config.guild(ctx.guild).host_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="signups")
    async def _clear_signups(self, ctx: Context):
        """Remove sign-ups channel from database."""

        await self.config.guild(ctx.guild).signup_channel.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_clear.command(name="nachannel")
    async def _clear_na_channel(self, ctx: Context):
        """Remove night action channel from database."""

        await self.config.guild(ctx.guild).na_channel_id.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="players")
    @commands.guild_only()
    @if_player_role_exists()
    async def _players(self, ctx: Context):
        """List of users with `Player` role."""

        guild = ctx.guild

        player_role = await self.role_from_config(guild, "player_id")

        players = [
            user.mention for user in guild.members if player_role in user.roles
        ]

        title = _("Total Players: {}").format(len(players))
        txt = "\n".join(players)

        embed = discord.Embed(
            colour=player_role.color, title=title, description=txt
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I need embed permissions for this command.")

    @commands.command(name="replacements")
    @commands.guild_only()
    @if_repl_role_exists()
    async def _replacements(self, ctx: Context):
        """List of users with `Replacement` role."""

        guild = ctx.guild

        repl_role = await self.role_from_config(guild, "repl_id")

        repls = [
            user.mention for user in guild.members if repl_role in user.roles
        ]

        title = _("Total Replacements: {}").format(len(repls))
        txt = "\n".join(repls)

        embed = discord.Embed(
            colour=repl_role.color, title=title, description=txt
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I need embed permissions for this command.")

    @commands.command(name="votecount", aliases=["vc"])
    @commands.guild_only()
    @if_player_role_exists()
    @if_game_started()
    async def _vote_count(
        self, ctx: Context, *, channel: discord.TextChannel = None
    ):
        """Count votes!

        The bot can automatically detect voting channels. However,
        it may not be able to detect the correct channel in some cases.
        Please specify the vote channel in such cases!
        """

        guild: discord.Guild = ctx.guild

        if not channel:
            channel = await self.get_vote_channel(guild)
            if isinstance(channel, str):
                return await ctx.send(channel)

            history = await channel.history(oldest_first=True).flatten()
            if len(history) > 100:
                return await ctx.send(_(
                    "I couldn't identify a voting channel. Please specify one explicitly."
                ))
        else:
            history = await channel.history(oldest_first=True).flatten()
            if len(history) > 100:
                return await ctx.send(_(
                    "That channel has too many messages!"
                    " Please ask a host for manual vote count."
                ))

        if len(history) < 1:
            return await ctx.send(_("{} is empty.").format(channel.mention))

        user_votes = {}
        player_role = guild.get_role(
            await self.config.guild(guild).player_id()
        )

        for message in history:
            author = message.author
            if player_role not in author.roles:
                continue
            vote = self.get_vote_from_message(message)
            if not vote:
                continue
            user_votes[f"{author.name}#{author.discriminator}"] = vote

        user_votes = await self.get_non_voters(guild, user_votes)

        votes = {}
        for user in user_votes:
            val = user_votes[user].capitalize()
            try:
                votes[val].append(user)
            except KeyError:
                votes[val] = [user]

        # max votes first
        votes = dict(sorted(
            votes.items(), key=lambda item: len(item[1]), reverse=True
        ))

        # Pop and add stuff back to dict for ordering purpose.
        try:
            votes["VTNL"] = votes.pop("Vtnl")
        except KeyError:
            pass
        try:
            votes["No vote"] = votes.pop("No vote")
        except KeyError:
            pass

        txt = ""

        for i, vote in enumerate(votes, start=1):
            voters = votes[vote]

            if vote == "VTNL":
                txt += _("\n\n**{}** - {} ({})").format(vote, len(voters), ", ".join(voters))
            elif vote == "No vote":
                txt += _("\n\n**Not voting** - {} ({})").format(len(voters), ", ".join(voters))
            else:
                txt += _("\n{}. **{}** - {} ({})").format(i, vote, len(voters), ", ".join(voters))

        title = _("Vote Count")

        embed = discord.Embed(
            color=0x00CDFF, title=title,
            description=_("__Counting from {} channel.__\n\n{}").format(
                channel.mention, txt.strip()
            )
        )

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(
                f"**{title}**\n\n__Counting from {channel.mention}"
                f" channel.__\n\n{txt.strip()}"
            )

    @commands.command(name="timesince", aliases=["ts"])
    @commands.guild_only()
    @if_game_started()
    async def _time_since(self, ctx: Context):
        """Tell time elapsed since day/night channel was opened."""

        guild: discord.Guild = ctx.guild

        cycle = await self.config.guild(guild).cycle()
        player = guild.get_role(await self.config.guild(guild).player_id())

        channel = guild.get_channel(cycle["day"])
        phase_name = f"Day {cycle['number']}"
        if not self.is_day(channel, player):
            channel = guild.get_channel(cycle["night"])
            phase_name = f"Night {cycle['number']}"

        diff = datetime.utcnow() - channel.created_at

        await ctx.send(
            _("{} began about {} ago.").format(
                phase_name, self.format_time_since(diff)
            )
        )

    @commands.command(name="started")
    @commands.guild_only()
    @if_host_or_admin()
    async def _started(self, ctx: Context, cycle_number=1):
        """Used to fix the issue when the bot can't detect if game started.

        `cycle_number` is the number of cycle currently on. Defaults to 1.
        """

        await self.config.guild(ctx.guild).set_raw(
            "cycle", "number", value=cycle_number
        )

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.group(name="notes")
    @commands.guild_only()
    @if_in_private_channel()
    async def _notes(self, ctx: Context):
        """Save and view game specific notes."""
        pass

    @_notes.command(name="add")
    async def _add_note(
        self,
        ctx: Context,
        note: Union[discord.Message, str],
        *,
        reason: str = None
    ):
        """Save a game-specific note for future reference.

        Note can either be a message link or text. If it is text,
        please wrap it inside double quotes. You can also specify
        a reason for adding the note.
        """

        if isinstance(note, discord.Message):
            content = note.clean_content
            author = str(note.author)
            channel = note.channel.mention
            jump_url = note.jump_url
        else:
            content = note
            author = None
            channel = None
            jump_url = None

        async with self.config.member(ctx.author).notes() as notes:
            notes.append({
                "note": content,
                "reason": reason or "No reason",
                "author": author,
                "channel": channel,
                "jump_url": jump_url
            })

        await ctx.message.add_reaction(CHECK_MARK)

    @_notes.command(name="all")
    async def _view_all_notes(self, ctx: Context):
        """View all saved game-specific notes."""

        author = ctx.author

        note_infos = []

        embed_links = ctx.channel.permissions_for(ctx.guild.me).embed_links

        author_str = f"{author.name}'"

        if author.name[-1].lower() != "s":
            author_str += "s"

        async with self.config.member(author).notes() as notes:
            total = len(notes)
            for page_num, note in enumerate(notes, start=1):
                msg_info = ""
                if note["author"]:
                    msg_info += _("**Author:** {}").format(note["author"])
                if note["channel"]:
                    msg_info += _("\n**Channel:** {}").format(note["channel"])
                if note["jump_url"]:
                    if embed_links:
                        msg_info += _(
                            "\n[Click here to jump to message]({})"
                        ).format(note["jump_url"])
                    else:
                        msg_info += _(
                            "\n**Jump To Message:** {}"
                        ).format(note["jump_url"])

                note_info = _(
                    "{}\n\n**Note:**\n```{}```\n**Reason:**\n```{}```"
                ).format(
                    msg_info,
                    note["note"],
                    note["reason"]
                ).strip()

                if embed_links:
                    page = discord.Embed(
                        colour=0xff0000,
                        description=note_info,
                        title=_("{} TvM Notes").format(author_str),
                        timestamp=ctx.message.created_at
                    )

                    page.set_footer(
                        text=_("Page {page_num}/{leng}").format(
                            page_num=page_num, leng=total
                        )
                    )
                else:
                    page = _(
                        "**{author} TvM Notes**"
                        "\n\n{note}"
                        "\n{footer}"
                    ).format(
                        author=author_str,
                        note=note_info,
                        footer=_("*Page {page_num}/{leng}*").format(
                            page_num=page_num, leng=total
                        )
                    )

                note_infos.append(page)

        await menu(ctx, note_infos, DEFAULT_CONTROLS)

    @_notes.command(name="view")
    async def _view_note(self, ctx: Context, number: int):
        """View saved game-specific note specified by number."""

        author = ctx.author

        embed_links = ctx.channel.permissions_for(ctx.guild.me).embed_links

        author_str = f"{author.name}'"

        if author.name[-1].lower() != "s":
            author_str += "s"

        async with self.config.member(author).notes() as notes:
            try:
                note = notes[number-1]
            except IndexError:
                return await ctx.send(
                    _("Note number {} not found.").format(number)
                )

            msg_info = ""
            if note["author"]:
                msg_info += _("**Author:** {}").format(note["author"])
            if note["channel"]:
                msg_info += _("\n**Channel:** {}").format(note["channel"])
            if note["jump_url"]:
                if embed_links:
                    msg_info += _(
                        "\n[Click here to jump to message]({})"
                    ).format(note["jump_url"])
                else:
                    msg_info += _(
                        "\n**Jump To Message:** {}"
                    ).format(note["jump_url"])

            note_info = _(
                "{}\n\n**Note:**\n```{}```\n**Reason:**\n```{}```"
            ).format(
                msg_info,
                note["note"],
                note["reason"]
            ).strip()

            if embed_links:
                page = discord.Embed(
                    colour=0xff0000,
                    description=note_info,
                    title=_("{} TvM Note #{}").format(author_str, number),
                    timestamp=ctx.message.created_at
                )
                await ctx.send(embed=page)
            else:
                page = _(
                    "**{author} TvM Note #{number}**"
                    "\n\n{note}"
                ).format(
                    author=author_str,
                    number=number,
                    note=note_info
                )
                await ctx.send(page)

    @_notes.command(name="total")
    async def _total_notes(self, ctx: Context):
        """Total number of saved game-specific notes."""

        async with self.config.member(ctx.author).notes() as notes:
            await ctx.send(_("You have {} notes saved.").format(len(notes)))

    @_notes.command(name="removeall")
    async def _remove_all_notes(self, ctx: Context):
        """Remove all saved game-specific notes."""

        async with self.config.member(ctx.author).notes() as notes:
            notes.clear()

        await ctx.message.add_reaction(CHECK_MARK)

    @_notes.command(name="remove")
    async def _remove_note(self, ctx: Context, number: int):
        """Remove saved game-specific note specified by number."""

        async with self.config.member(ctx.author).notes() as notes:
            try:
                notes.pop(number-1)
            except IndexError:
                return await ctx.send(
                    _("Note number {} not found.").format(number)
                )

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="invite")
    async def invite_(self, ctx: Context):
        """Get TvM Assistant's invite url."""

        perm_int = discord.Permissions(268494928)

        data = await self.bot.application_info()
        invite_url = discord.utils.oauth_url(data.id, permissions=perm_int)

        value = (
            f"Invite TvM Assistant to your bot by [clicking here]({invite_url})."
            "\n\nInviting the bot will give it some management permissions. You can"
            " review them when you use the link."
        )

        embed = discord.Embed(color=await ctx.embed_colour(), description=value)
        embed.set_author(name=f"Invite TvM Assistant", icon_url=ctx.me.avatar_url)

        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            return await ctx.send(
                f"{invite_url}\n\nInviting the bot will give it some management permissions."
                " You can review them when you use the link."
            )

    async def check_na_channel(self, guild: discord.Guild):
        """Check if night action channel exists.

        If it does, return the channel object. Otherwise, return False.
        """

        ch_id = await self.config.guild(guild).na_channel_id()

        if ch_id:
            return discord.utils.get(guild.text_channels, id=ch_id)
        return False

    async def create_na_channel(self, guild: discord.Guild):
        """Create a channel for the bot to send night actions.

        Also add the channel to guild database. Returns the channel.
        """

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                add_reactions=True
            )
        }

        channel = await guild.create_text_channel(
            "night-actions", overwrites=overwrites
        )

        await self.config.guild(guild).na_channel_id.set(channel.id)

        return channel

    async def cog_command_error(self, ctx: Context, error: Exception):
        if not isinstance(
            getattr(error, "original", error),
            (
                # commands.CheckFailure,
                commands.UserInputError,
                commands.DisabledCommand,
                commands.CommandOnCooldown,
            ),
        ):
            if isinstance(error, TvMCommandFailure):
                await ctx.send(error)

        await ctx.bot.on_command_error(
            ctx, getattr(error, "original", error), unhandled_by_cog=True
        )

    async def role_from_id(self, guild: discord.Guild, role_id: int):
        """Get `discord.Role` object from given role ID."""

        return discord.utils.get(guild.roles, id=role_id)

    async def remove_extra_roles(self, ctx: Context, extra: list):
        """Remove roles listed in `extra`."""

        guild = ctx.guild
        author = ctx.author

        for item in extra:
            if item == "player":
                id_ = await self.config.guild(guild).player_id()
                role = discord.utils.get(guild.roles, id=id_)

                if role in author.roles:
                    await author.remove_roles(role)

            elif item == "spec":
                id_ = await self.config.guild(guild).spec_id()
                role = discord.utils.get(guild.roles, id=id_)

                if role in author.roles:
                    await author.remove_roles(role)

            elif item == "repl":
                id_ = await self.config.guild(guild).repl_id()
                role = discord.utils.get(guild.roles, id=id_)

                if role in author.roles:
                    await author.remove_roles(role)

    async def check_total(self, guild: discord.Guild):
        """Return True total sign-ups is less than total players."""

        max_allowed = await self.config.guild(guild).total_players()
        signed = await self.config.guild(guild).signed()

        if signed < max_allowed:
            return True

    async def update_total(self, ctx: Context, override=0):
        """Update total signed players."""

        guild = ctx.guild
        author = ctx.author

        old = await self.config.guild(guild).signed()

        if override:
            return await self.config.guild(guild).signed.set(old+override)

        player_id = await self.config.guild(guild).player_id()
        player_role = discord.utils.get(guild.roles, id=player_id)

        if player_role in author.roles:
            await self.config.guild(guild).signed.set(old-1)

    async def role_from_config(self, guild: discord.Guild, iden: str):
        """Return `iden` role from the guild database."""

        id_ = await getattr(self.config.guild(guild), iden)()

        return discord.utils.get(guild.roles, id=id_)

    async def get_vote_channel(self, guild: discord.Guild):
        """Return latest vote channel.

        Error message is returned if no channels can be found.
        """

        vote_channels = [
            ch for ch in guild.channels
            if "voting" in ch.name
            or "vote" in ch.name
        ]

        if len(vote_channels) < 1:
            return _(
                "I couldn't identify a voting channel."
                " Please specify one explicitly."
            )

        if len(vote_channels) > 1:
            # get channel with the largest suffixed number
            return max(
                vote_channels, key=lambda obj: int(obj.name.split("-")[1])
            )

        else:
            return vote_channels[0]

    def get_vote_from_message(self, message: discord.Message):
        """Return name of person votes against from the message."""

        content = message.clean_content
        message

        res = re.match(VOTE_RE, content)
        if res:
            return res.group(1)
        else:
            res = re.match(NO_VOTE_RE, content)
        if res:
            return "VTNL"
        else:
            res = re.match(UN_VOTE_RE, content)
        if res:
            return "No vote"

    async def get_non_voters(self, guild: discord.Guild, uservotes: dict):
        """Return dict after adding non-voters."""

        player_role = guild.get_role(
            await self.config.guild(guild).player_id()
        )

        for member in guild.members:
            if player_role in member.roles:
                userkey = f"{member.name}#{member.discriminator}"
                if userkey not in uservotes:
                    uservotes[userkey] = "No vote"

        return uservotes

    def is_day(
        self, day_channel: discord.TextChannel, player: discord.Role
    ):
        """Checks whether it is day. Returns True if it is."""

        if day_channel.overwrites_for(player).send_messages:
            return True

    def format_time_since(self, timedelta: timedelta):
        """Get human representation of time passed since channel was created.

        Version of `redbot.core.utils.chat_formatting.humanize_timedelta`
        to only return days, hours and minutes.
        """

        seconds = timedelta.total_seconds()

        periods = [
            (_("day"), _("days"), 60 * 60 * 24),
            (_("hour"), _("hours"), 60 * 60),
            (_("minute"), _("minutes"), 60),
        ]

        strings = []
        for period_name, plural_period_name, period_seconds in periods:
            if seconds >= period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                if period_value == 0:
                    continue
                unit = plural_period_name if period_value > 1 else period_name
                strings.append(f"{int(period_value)} {unit}")

        return ", ".join(strings)

    def cog_unload(self):
        global old_invite
        if old_invite:
            try:
                self.bot.remove_command("invite")
            except Exception:
                pass
            self.bot.add_command(old_invite)


async def setup(bot: Red):
    global old_invite
    old_invite = bot.get_command("invite")
    if old_invite:
        bot.remove_command("invite")

    cog = TvM(bot)
    bot.add_cog(cog)
