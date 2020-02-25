# TvM Assistant

TvM Assistant is a Discord bot with utility functions to make hosting TvMs easier. You can invite it to your server by using [this link](https://discordapp.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot). Inviting the bot will give it `Manage Channels`, `Manage Roles`, `Manage Messages`, `Add Reactions` and `Embed Links` permissions in addition to `Read` and `Send` messages perm.

---

It has the following commands:

**Note:** The stuff written inside `<>` and `[]` are called parameters. `<>` means required parameter, `[]` means optional. More on types of parameters below.

## Roles Setup

`-tvm hostrole <role>`: Set the host role.

`-tvm playerrole <role>`: Set the player role.

`-tvm specrole <role>`: Set the spectator role.

`-tvm deadrole <role>`: Set the dead player role.

`-tvm replrole <role>`: Set the replacement role.

`-tvm setroles`: Set up all the 5 roles automatically.

## Channels

`-tvm nachannel <channel>`: Set the channel where night actions are relayed.

`-tvm signup <channel>`: Set sign-ups channel.

`-playerchats [category_name]`: Set up private channels for all players. It also sets up individual channels for players who are mafia. Remove those manually. You can also specify a category name for the channels. Alias: `-pc [category_name]`

`-mafiachat <user1> <user2>...`: Set up mafia chat for users specified. Example: `-mafiachat Arius#5544 @Ligi Siris#4421`. Alias: `-mafchat user1 user2...`

`-specchat [channel]` : Create spectator chat or fix permissions of an existing channel.

## TvM Specific Settings

`- tvm changena`: Toggle if user can change their night action once submitted. Defaults to `True`.

`-tvm total <number>`: Total number of players that can sign-up for the game. Defaults to `12`.

`-tvm signopen`: Allow people to sign-up. On by default.

`-tvm signclose`: Close sign-ups.

`-tvm lock`: Lock these and role and channel settings (commands that begin with `tvm`). Useful once the configuration is done so you don't accidentally mess things up mid-game.

`-tvm unlock`: Unlock TvM settings.

`-tvm settings`: View TvM settings. Alias: `-tvm show`

## User Commands

`-in [ignored]`: Sign-up for the TvM. Automatically assigns the Player role and removes Spec and Replacement roles, if necessary. You can type anything you want after `-in`.

`-out [ignored]`: Sign-out of the TvM or spectate it. Automatically assigns the Spectator role and removes Player and Replacement roles, if necessary. You can type anything you want after `-out`. Alias: `-spec`

`-repl [ignored]`: Sign-up as a replacement. Automatically assigns the Replacement role and removes Player and Spectator roles, if necessary. You can type anything you want after `-repl`.

`-nightaction <action>`: Your night action. It can only be used in your own private channel. `action` can be any text. You may not be able to update your night action if host has disabled that setting. Alias: `-na <action>`

## Misc

`-host <user>`: Give the specified user `host` role.

`-rand <players> <roles>`: Randomly assign a role to a player from the pool. The command should follow the pattern used in this example: `-rand "player1name, player2name, player3name, ..." role1, role2, role3, ...`. Notice the quotes (`"`). Number of players should be equal to number of roles. You can duplicate roles.

## Parameters

### User

`user` can be user ID or name (case and spaces sensitive) with or without discriminator. It's generally a good practice to include the discriminator or use the user ID. `search` command can be useful for getting the ID or the full username.

### Role

`role` must be the role ID or name (case and spaces sensitive). `role info` command can be useful for getting the ID or the full name.

### Channel

`channel` can be channel ID or name (case and spaces sensitive).

### Miscellaneous

`ignored`: text, supports markdown, is ignored by the bot
`action`: text, supports markdown
`players`: list of comma-separated player names. Must be enclosed within double quotes.
`roles`: list of comma-separated role names
`case_number`: a number
`category_name`: text, doesn't support markdown

## Credits

Town of Salem: Bot logo
[Trusty-cogs](https://github.com/TrustyJAID/Trusty-cogs): Logging events
