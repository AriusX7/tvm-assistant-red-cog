from discord.ext.commands import CheckFailure
from redbot.core import commands, checks


class TvMSettingsLocked(CheckFailure):
    """Raised if TvM settings are locked."""


class NotHostOrAdmin(CheckFailure):
    """Raised if member is not host or admin."""


class NotRequiredRoles(CheckFailure):
    """Raised if player or spectator roles are not set up."""


class NotPrivateChannel(CheckFailure):
    """Raised if night action command is used outside player's channel."""


def tvmset_lock():
    """A decorator to check if TvM setting commands are locked."""

    async def predicate(ctx: commands.Context):
        cog = ctx.cog
        if cog:
            config = cog.config

            lock = await config.guild(ctx.guild).tvmset_lock()
            if lock:
                raise TvMSettingsLocked(
                    "TvM setting commands are currently locked."
                    " Remove the lock before running the setting commands."
                )
        # Run command if not locked
        return True

    return commands.check(predicate)


def is_host_or_admin():
    """Restrict the role to members with host role or admin permissions."""

    async def predicate(ctx: commands.Context):

        if await checks.is_admin_or_superior(ctx):
            return True

        cog = ctx.cog
        if cog:
            config = cog.config

            host_id = await config.guild(ctx.guild).host_id()
            user_role_ids = [role.id for role in ctx.author.roles]

            if host_id in user_role_ids:
                return True
            else:
                raise NotHostOrAdmin(
                    "This command can only be used by hosts or admins."
                )

    return commands.check(predicate)


def player_and_spec_roles_exist():
    """Check if player and spectator roles are set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            player = await config.guild(guild).player_id()
            spec = await config.guild(guild).spec_id()

            if not player and spec:
                txt = "Player role is not set up!"
            elif player and not spec:
                txt = "Spectator role is not set up!"
            elif not player and not spec:
                txt = "Player and spectator roles are not set up!"
            else:
                return True

            raise NotRequiredRoles(txt)

    return commands.check(predicate)


def player_role_exists():
    """Check if player role is set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            player = await config.guild(guild).player_id()

            if player:
                return True

            raise NotHostOrAdmin("Player role is not set up!")

    return commands.check(predicate)


def player_and_dead_roles_exist():
    """Check if player and dead player roles are set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            player = await config.guild(guild).player_id()
            dead = await config.guild(guild).dead_id()

            if not player and dead:
                txt = "Player role is not set up!"
            elif player and not dead:
                txt = "Dead player role is not set up!"
            elif not player and not dead:
                txt = "Player and dead players roles are not set up!"
            else:
                return True

            raise NotRequiredRoles(txt)

    return commands.check(predicate)


def repl_role_exists():
    """Check if replacement role is set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            repl = await config.guild(guild).repl_id()

            if repl:
                return True

            raise NotHostOrAdmin("Replacement role is not set up!")

    return commands.check(predicate)


def in_private_channel():
    """Restrict the night action command to user's private channel."""

    async def predicate(ctx: commands.Context):

        channel = ctx.channel

        overwrites = channel.overwrites_for(ctx.author)

        if overwrites.send_messages:
            return True

        raise NotPrivateChannel(
            "This command can only be used in your private channel."
        )

    return commands.check(predicate)
