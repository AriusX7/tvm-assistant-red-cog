from discord.ext.commands import CheckFailure
from redbot.core import commands


class TvMCommandFailure(CheckFailure):
    """Raised when a TvM command condition is not met."""


def tvmset_lock():
    """A decorator to check if TvM setting commands are locked."""

    async def predicate(ctx: commands.Context):
        cog = ctx.cog
        if cog:
            config = cog.config

            lock = await config.guild(ctx.guild).tvmset_lock()
            if lock:
                raise TvMCommandFailure(
                    "TvM setting commands are currently locked."
                    " Remove the lock before running the setting commands."
                )
        # Run command if not locked
        return True

    return commands.check(predicate)


def if_host_or_admin():
    """Restrict the role to members with host role or admin permissions."""

    async def predicate(ctx: commands.Context):

        if ctx.author.guild_permissions.administrator:
            return True

        cog = ctx.cog
        if cog:
            config = cog.config

            host_id = await config.guild(ctx.guild).host_id()
            user_role_ids = [role.id for role in ctx.author.roles]

            if host_id in user_role_ids:
                return True
            else:
                raise TvMCommandFailure(
                    "This command can only be used by hosts and admins."
                )

    return commands.check(predicate)


def if_player_and_spec_roles_exist():
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

            raise TvMCommandFailure(txt)

    return commands.check(predicate)


def if_player_role_exists():
    """Check if player role is set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            player = await config.guild(guild).player_id()

            if player:
                return True

            raise TvMCommandFailure("Player role is not set up!")

    return commands.check(predicate)


def if_player_and_dead_roles_exist():
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

            raise TvMCommandFailure(txt)

    return commands.check(predicate)


def if_repl_role_exists():
    """Check if replacement role is set up."""

    async def predicate(ctx: commands.Context):

        guild = ctx.guild

        cog = ctx.cog
        if cog:
            config = cog.config

            repl = await config.guild(guild).repl_id()

            if repl:
                return True

            raise TvMCommandFailure("Replacement role is not set up!")

    return commands.check(predicate)


def if_in_private_channel():
    """Check if the command is used in user's private channel."""

    async def predicate(ctx: commands.Context):

        channel = ctx.channel

        overwrites = channel.overwrites_for(ctx.author)

        if overwrites.send_messages:
            return True

        raise TvMCommandFailure(
            "This command can only be used in your private channel."
        )

    return commands.check(predicate)


def if_game_started():
    """Check if the game started."""

    async def predicate(ctx: commands.Context):

        cog = ctx.cog
        if cog:
            config = cog.config

            if await config.guild(ctx.guild).get_raw("cycle", "number") > 0:
                return True

            raise TvMCommandFailure(
                "Game has not started yet. Please contact a host if the"
                " game has started and you're still getting this error."
            )

    return commands.check(predicate)
