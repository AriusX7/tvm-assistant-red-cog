import os
from datetime import datetime
from typing import cast

import discord
from discord.ext.commands import CheckFailure
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands import Context
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import escape


_ = Translator("TvMLog", __file__)

default_guild = {
    "log_id": None,  # logging channel
    "bchannels": [],  # blacklisted channels
    "wchannels": []  # whitelisted channels
}

CHECK_MARK = "\N{WHITE HEAVY CHECK MARK}"


class NotHostOrAdmin(CheckFailure):
    """Raised if member is not host or admin."""


def is_host_or_admin():
    """Restrict the role to members with host role or admin permissions."""

    async def predicate(ctx: Context):

        if ctx.author.guild_permissions.administrator:
            return True

        cog = ctx.bot.get_cog("TvM")
        if cog:
            config = cog.config

            host_id = await config.guild(ctx.guild).host_id()
            user_role_ids = [role.id for role in ctx.author.roles]

            if host_id in user_role_ids:
                return True
            else:
                raise NotHostOrAdmin(
                    "This command can only be used by hosts and admins."
                )

    return commands.check(predicate)


@cog_i18n(_)
class TvMLog(commands.Cog):
    """Logging for TvMs!"""

    def __init__(self, bot: Red):
        self.bot = bot

        self.config = Config.get_conf(
            bot, "1_021_210_707", force_registration=True
        )

        try:
            self.tvm_conf: Config = bot.get_cog("TvM").config
        except AttributeError:
            pass

        self.config.register_guild(**default_guild)

    @commands.command(name="logchannel")
    @is_host_or_admin()
    @commands.guild_only()
    async def logging_channel(
        self, ctx: Context, *, channel: discord.TextChannel
    ):
        """Set the logging channel."""

        await self.config.guild(ctx.guild).log_id.set(channel.id)

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="wchannel")
    @is_host_or_admin()
    @commands.guild_only()
    async def whitelist_channel(
        self, ctx: Context, channel: discord.TextChannel
    ):
        """Whitelist a channel. Messages in it will always be logged."""

        async with self.config.guild(ctx.guild).wchannels() as wlist:
            wlist.append(channel.id)

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="bchannel")
    @is_host_or_admin()
    @commands.guild_only()
    async def blacklist_channel(
        self, ctx: Context, channel: discord.TextChannel
    ):
        """Blacklist a channel. Messages in it will never be logged."""

        async with self.config.guild(ctx.guild).bchannels() as blist:
            blist.append(channel.id)

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="rwchannel")
    @is_host_or_admin()
    @commands.guild_only()
    async def remove_whitelist_channel(
        self, ctx: Context, channel: discord.TextChannel
    ):
        """Remove channel from whitelist."""

        async with self.config.guild(ctx.guild).wchannels() as wlist:
            try:
                wlist.remove(channel.id)
            except ValueError:
                return await ctx.send(_(
                    "{} was not whitelisted.".format(channel.mention)
                ))

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="rbchannel")
    @is_host_or_admin()
    @commands.guild_only()
    async def remove_blacklist_channel(
        self, ctx: Context, channel: discord.TextChannel
    ):
        """Remove channel from blacklist."""

        async with self.config.guild(ctx.guild).bchannels() as blist:
            try:
                blist.remove(channel.id)
            except ValueError:
                return await ctx.send(_(
                    "{} was not blacklisted.".format(channel.mention)
                ))

        await ctx.message.add_reaction(CHECK_MARK)

    @commands.command(name="logsettings")
    @is_host_or_admin()
    @commands.guild_only()
    async def _log_settings(self, ctx: Context):
        """Display log settings."""

        guild: discord.Guild = ctx.guild

        async with self.config.guild(guild).wchannels() as wlist:
            whitelist = [guild.get_channel(ch_id).mention for ch_id in wlist]

        async with self.config.guild(guild).bchannels() as blist:
            blacklist = [guild.get_channel(ch_id).mention for ch_id in blist]

        allowed = []
        for channel in guild.text_channels:
            mention = channel.mention
            if (
                mention in whitelist
                or mention in blacklist
            ):
                continue
            if not await self.is_ignored_channel(guild, channel):
                allowed.append(mention)

        embed = discord.Embed(colour=0x00CDFF, title="TvM Log Settings")

        embed.add_field(
            name="Whitelisted Channels",
            value="\n".join(whitelist) or "No channels",
            inline=False
        )
        embed.add_field(
            name="Blacklisted Channels",
            value="\n".join(blacklist) or "No channels",
            inline=False
        )
        embed.add_field(
            name="Default Allowed Channels", value="\n".join(allowed) or "None"
        )

        await ctx.send(embed=embed)

    async def is_ignored_channel(
        self, guild: discord.Guild, channel: discord.TextChannel
    ):
        """Check if channel is an ignored channel."""

        async with self.config.guild(guild).wchannels() as wlist:
            if channel.id in wlist:
                return False

        async with self.config.guild(guild).bchannels() as blist:
            if channel.id in blist:
                return True

        everyone_perms = channel.overwrites_for(guild.default_role)

        if everyone_perms.read_messages is False:
            return True

    def set_text(
        self, message: discord.Message, embed: discord.Embed, iden: str
    ):
        """Set text into field. Break into multiple fields if necessary."""

        content = message.content

        if len(content) > 1024:
            first = content[:500]
            # second = content[1024:]
            fn = f"{iden.lower()}.txt"
            f = open(fn, "w")
            f.write(content)

            file = discord.File(fn)

            txt = f"{first.strip()}...\n\nFull message attached below."

            f.close()

            try:
                os.remove(fn)
            except OSError:
                open(fn, "w").close()

            embed.add_field(name=f"{iden} Content", value=txt)
            # embed.add_field(
            #     name=f"{iden} Content 2", value=second, inline=False
            # )
        else:
            file = None
            embed.add_field(name=f"{iden} Content", value=content)

        return embed, file

    @commands.Cog.listener(name="on_raw_message_delete")
    async def on_raw_message_delete_listener(
        self,
        payload: discord.RawMessageDeleteEvent,
        *,
        check_audit_log: bool = True
    ) -> None:
        """
            Source: ExtendedMogLog cog by Trusty.
            https://github.com/TrustyJAID/Trusty-cogs/tree/master/extendedmodlog
        """

        guild_id = payload.guild_id

        if guild_id is None:
            return

        guild = self.bot.get_guild(guild_id)

        log_id = await self.config.guild(guild).log_id()
        if not log_id:
            return

        log_channel = guild.get_channel(log_id)

        channel_id = payload.channel_id
        msg_channel = guild.get_channel(channel_id)

        if await self.is_ignored_channel(guild, msg_channel):
            return

        embed_links = log_channel.permissions_for(guild.me).embed_links
        message = payload.cached_message

        if message is None:
            if embed_links:
                embed = discord.Embed(
                    description=_("*Message's content unknown.*"),
                    colour=0xFF0000,
                )
                embed.add_field(name=_("Channel"), value=msg_channel.mention)
                embed.set_author(name=_("Deleted Message"))
                await log_channel.send(embed=embed)
            else:
                infomessage = _(
                    "`{time}` A message was deleted in {channel}"
                ).format(
                    time=datetime.utcnow().strftime("%H:%M:%S"),
                    channel=msg_channel.mention,
                )
                return await log_channel.send(
                    f"{infomessage}\n> *Message's content unknown.*"
                )
        await self._cached_message_delete(
            message, guild, log_channel, check_audit_log=check_audit_log
        )

    async def _cached_message_delete(
        self,
        message: discord.Message,
        guild: discord.Guild,
        channel: discord.TextChannel,
        *,
        check_audit_log: bool = True,
    ) -> None:
        """
            Source: ExtendedMogLog cog by Trusty.
            https://github.com/TrustyJAID/Trusty-cogs/tree/master/extendedmodlog
        """

        if message.author.bot:
            return
        if message.content == "" and message.attachments == []:
            return
        embed_links = channel.permissions_for(guild.me).embed_links
        time = message.created_at
        perp = None
        if (
            channel.permissions_for(guild.me).view_audit_log
            and check_audit_log
        ):
            action = discord.AuditLogAction.message_delete
            async for log in guild.audit_logs(limit=2, action=action):
                same_chan = log.extra.channel.id == message.channel.id
                if log.target.id == message.author.id and same_chan:
                    perp = f"{log.user}({log.user.id})"
                    break
        message_channel = cast(discord.TextChannel, message.channel)
        author = message.author
        if perp is None:
            infomessage = _(
                "`{time}` A message from **{author}**"
                " (`{a_id}`) was deleted in {channel}"
            ).format(
                time=time.strftime("%H:%M:%S"),
                author=author,
                channel=message_channel.mention,
                a_id=author.id,
            )
        else:
            infomessage = _(
                "`{time}` {perp} deleted a message from "
                "**{author}** (`{a_id}`) in {channel}"
            ).format(
                time=time.strftime("%H:%M:%S"),
                perp=perp,
                author=author,
                a_id=author.id,
                channel=message_channel.mention,
            )
        if embed_links:
            embed = discord.Embed(
                description=message.content,
                colour=0xFF0000,
                timestamp=time,
            )

            embed.add_field(name=_("Channel"), value=message_channel.mention)
            if perp:
                embed.add_field(name=_("Deleted by"), value=perp)
            if message.attachments:
                files = ", ".join(a.filename for a in message.attachments)
                if len(message.attachments) > 1:
                    files = files[:-2]
                embed.add_field(name=_("Attachments"), value=files)
            embed.set_footer(text=_("User ID: ") + str(message.author.id))
            embed.set_author(
                name=_("{member} ({m_id}) - Deleted Message").format(
                    member=author, m_id=author.id
                ),
                icon_url=str(message.author.avatar_url),
            )
            await channel.send(embed=embed)
        else:
            clean_msg = escape(message.clean_content, mass_mentions=True)[
                : (1990 - len(infomessage))
            ]
            await channel.send(f"{infomessage}\n>>> {clean_msg}")

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(
        self, payload: discord.RawBulkMessageDeleteEvent
    ):
        """
            Source: ExtendedMogLog cog by Trusty.
            https://github.com/TrustyJAID/Trusty-cogs/tree/master/extendedmodlog
        """

        guild_id = payload.guild_id
        if guild_id is None:
            return

        guild = self.bot.get_guild(guild_id)

        log_id = await self.config.guild(guild).log_id()
        if not log_id:
            return

        channel_id = payload.channel_id
        msg_channel = guild.get_channel(channel_id)

        try:
            log_channel = guild.get_channel(log_id)
        except RuntimeError:
            return

        if await self.is_ignored_channel(guild, msg_channel):
            return

        embed_links = log_channel.permissions_for(guild.me).embed_links

        message_amount = len(payload.message_ids)

        if embed_links:
            embed = discord.Embed(
                description=msg_channel.mention, colour=0xFF0000,
            )
            embed.set_author(
                name=_("Bulk message delete"), icon_url=guild.icon_url
            )
            embed.add_field(
                name=_("Channel"), value=msg_channel.mention
            )
            embed.add_field(
                name=_("Messages deleted"), value=str(message_amount)
            )
            await log_channel.send(embed=embed)
        else:
            infomessage = _(
                "`{time}` Bulk message delete in {channel},"
                " {amount} messages deleted."
            ).format(
                time=datetime.datetime.utcnow().strftime("%H:%M:%S"),
                amount=message_amount,
                channel=msg_channel.mention,
            )
            await log_channel.send(infomessage)

        for message in payload.cached_messages:
            new_payload = discord.RawMessageDeleteEvent(
                {
                    "id": message.id,
                    "channel_id": channel_id,
                    "guild_id": guild_id}
            )
            new_payload.cached_message = message
            try:
                await self.on_raw_message_delete_listener(
                    new_payload, check_audit_log=False
                )
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        """
            Source: ExtendedMogLog cog by Trusty.
            https://github.com/TrustyJAID/Trusty-cogs/tree/master/extendedmodlog
        """

        guild = before.guild
        if guild is None:
            return

        log_id = await self.config.guild(guild).log_id()
        if not log_id:
            return

        if before.content == after.content:
            return

        try:
            log_channel = guild.get_channel(log_id)
        except RuntimeError:
            return

        if await self.is_ignored_channel(guild, after.channel):
            return

        embed_links = log_channel.permissions_for(guild.me).embed_links

        time = datetime.utcnow()
        fmt = "%H:%M:%S"

        if embed_links:
            embed = discord.Embed(
                colour=0xFF9300,
                timestamp=before.created_at,
                description=(
                    f"[Click here to jump to the message.]({after.jump_url})"
                )
            )
            embed, bfile = self.set_text(before, embed, "Before")
            embed, afile = self.set_text(after, embed, "After")
            embed.add_field(
                name=_("Channel"), value=before.channel.mention, inline=False
            )
            embed.set_footer(text=_("Message ID: ") + str(before.id))
            embed.set_author(
                name=_("{member} ({m_id}) - Edited Message").format(
                    member=before.author, m_id=before.author.id
                ),
                icon_url=str(before.author.avatar_url),
            )
            await log_channel.send(embed=embed)
            if bfile:
                await log_channel.send(file=bfile)
            if afile:
                await log_channel.send(file=afile)
        else:
            msg = _(
                "`{time}` **{author}** (`{a_id}`) edited a message "
                "in {channel}.\nBefore:\n> {before}\nAfter:\n> {after}"
            ).format(
                time=time.strftime(fmt),
                author=before.author,
                a_id=before.author.id,
                channel=before.channel.mention,
                before=escape(before.content, mass_mentions=True),
                after=escape(after.content, mass_mentions=True),
            )
            await log_channel.send(msg[:2000])
