from collections import namedtuple

import discord
from redbot.core.commands import Context
from redbot.core.commands.help import HelpSettings, RedHelpFormatter
from redbot.core.i18n import cog_i18n, Translator
from redbot.core.utils.chat_formatting import pagify

_ = Translator("TvM", __file__)

EmbedField = namedtuple("EmbedField", "name value inline")
COMMANDS_REFERENCE = "https://ariusx7.github.io/tvm-assistant/commands-reference"
QUICKSTART = "https://ariusx7.github.io/tvm-assistant/quickstart"


@cog_i18n(_)
class TvMHelpFormatter(RedHelpFormatter):
    """Class for TvM bot's help command.

    It is intended to display TvM, Logging and License commands only.
    """

    def __init__(self, bot):
        self.bot = bot

    async def format_bot_help(self, ctx: Context, help_settings: HelpSettings):
        """Format the default help message"""

        coms_ = await self.get_bot_help_mapping(ctx, help_settings)
        if not coms_:
            return

        if not await ctx.embed_requested():
            return await ctx.send("Please enable embeds!")

        tagline = self.get_default_tagline(ctx)

        emb = {
            "embed": {"title": "", "description": ""}, "footer": {"text": ""}, "fields": []
        }

        emb["embed"]["description"] = (
            f"Please visit [this page]({COMMANDS_REFERENCE}) for full list of commands."
            f"\nSet up the bot for your server by following this [quickstart guide]({QUICKSTART})."
        )
        emb["footer"]["text"] = tagline

        cog_text = ""

        # Really hacky way to ensure order of cogs.
        coms = []
        while len(coms) < 3:
            for j, k in coms_:
                cog_names = [c[0] for c in coms]
                if j == "TvM" and "Logging" not in cog_names:
                    coms.append((j, k))
                if j == "Logging":
                    if "TvM" in cog_names:
                        coms.append((j, k))
                if j is None:
                    if "Logging" in cog_names:
                        coms.append((j, k))
                        break

        for cog_name, data in coms:
            if cog_name in ["TvM", "Logging", None]:
                title = cog_name or 'License'
                if title == "Logging":
                    title = "Logging"
            else:
                continue

            def shorten_line(a_line: str) -> str:
                if len(a_line) < 70:  # embed max width needs to be lower
                    return a_line
                return a_line[:67] + "..."

            cog_text = "\n".join(
                shorten_line(
                    f"{ctx.clean_prefix}**{name}**"
                    f" {command.format_shortdoc_for_context(ctx)}"
                )
                for name, command in sorted(data.items())
            )

            for i, page in enumerate(
                pagify(cog_text, page_length=600, shorten_by=0)
            ):
                title_ = f"**{title}**" if i < 1 else f"**{title} (continued)**"

                field = EmbedField(title_, page, False)
                emb["fields"].append(field)

        await self.make_and_send_embeds(ctx, emb, help_settings)

    async def make_and_send_embeds(self, ctx, embed_dict: dict, help_settings: HelpSettings):

        pages = []

        page_char_limit = help_settings.page_char_limit
        page_char_limit = min(page_char_limit, 5500)  # Just in case someone was manually...

        author_info = {
            "name": f"{ctx.me.display_name} {_('Help')}",
            "icon_url": ctx.me.avatar_url,
        }

        # Offset calculation here is for total embed size limit
        # 20 accounts for# *Page {i} of {page_count}*
        offset = len(author_info["name"]) + 20
        foot_text = embed_dict["footer"]["text"]
        if foot_text:
            offset += len(foot_text)
        offset += len(embed_dict["embed"]["description"])
        offset += len(embed_dict["embed"]["title"])

        # In order to only change the size of embeds when neccessary for this rather
        # than change the existing behavior for people uneffected by this
        # we're only modifying the page char limit should they be impacted.
        # We could consider changing this to always just subtract the offset,
        # But based on when this is being handled (very end of 3.2 release)
        # I'd rather not stick a major visual behavior change in at the last moment.
        if page_char_limit + offset > 5500:
            # This is still neccessary with the max interaction above
            # While we could subtract 100% of the time the offset from page_char_limit
            # the intent here is to shorten again
            # *only* when neccessary, by the exact neccessary amount
            # To retain a visual match with prior behavior.
            page_char_limit = 5500 - offset
        elif page_char_limit < 250:
            # Prevents an edge case where a combination of long cog help and low limit
            # Could prevent anything from ever showing up.
            # This lower bound is safe based on parts of embed in use.
            page_char_limit = 250

        field_groups = self.group_embed_fields(embed_dict["fields"], page_char_limit)

        color = await ctx.embed_color()
        page_count = len(field_groups)

        if not field_groups:  # This can happen on single command without a docstring
            embed = discord.Embed(color=color, **embed_dict["embed"])
            embed.set_author(**author_info)
            embed.set_footer(**embed_dict["footer"])
            pages.append(embed)

        for i, group in enumerate(field_groups, 1):
            embed = discord.Embed(color=color, **embed_dict["embed"])

            # if page_count > 1:
            #     description = _(
            #         "*Page {page_num} of {page_count}*\n{content_description}"
            #     ).format(content_description=embed.description, page_num=i, page_count=page_count)
            #     embed.description = description

            embed.set_author(**author_info)

            prev_field = None
            for idx, field in enumerate(group):
                if prev_field:
                    prev_name = prev_field.name.replace("**", "")
                    name = field.name.replace("**", "")
                    merge_str = f"{prev_field.value}{field.value}"
                    if len(merge_str) > 1024:
                        merge = False
                    else:
                        merge = True
                    if prev_name in name and merge:
                        embed = embed.set_field_at(
                            idx-1, name=f"**{prev_name}**", value=merge_str
                        )
                    else:
                        embed.add_field(**field._asdict())
                else:
                    embed.add_field(**field._asdict())
                # embed.add_field(**field._asdict())
                prev_field = field

            embed.set_footer(**embed_dict["footer"])
            if page_count > 1:
                footer_text = f"Page {i} of {page_count} | {embed.footer.text}"
                footer_icon_url = embed.footer.icon_url
                embed.set_footer(text=footer_text, icon_url=footer_icon_url)

            pages.append(embed)

        await self.send_pages(ctx, pages, embed=True, help_settings=help_settings)
