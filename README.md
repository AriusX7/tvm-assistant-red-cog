<h1 align="center">
  <br>
  <a href="https://ariusx7.github.io/tvm-assistant/">
  <img src="https://i.imgur.com/v9WAfJi.jpg" alt="TvM Assistant">
  <br>
  </a>
  TvM Assistant
  <br>
</h1>

<h4 align="center">Makes hosting TvMs easier!</h4>

<p align="center">
  <a href="#introduction">Introduction</a>
  •
  <a href="#quickstart">Quickstart</a>
  •
  <a href="#commands-reference">Commands Reference</a>
  •
  <a href="#parameters">Parameters</a>
  •
  <a href="#self-hosting">Self Hosting</a>
  •
  <a href="#credits">Credits</a>
</p>

## Introduction

TvM Assistant is a Discord bot with utility functions to make hosting TvMs easier. You can invite it to your server by using [this link](https://discordapp.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot). Inviting the bot will give it `Manage Channels`, `Manage Roles`, `Manage Messages`, `Add Reactions` and `Embed Links` permissions in addition to `Read` and `Send` messages perm.

## Quickstart

Follow the steps below to quicky set up the bot for your game. You must have `administrator` permissions to use some of the commands. If you're a player looking to check the commands you can use, see [General](#general) and [Misc](#misc) sections.

### Prerequisites

Beginning with the bot setup, firstly, make sure you've [invited the bot](https://discordapp.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot) to your TvM server. Secondly, check if the bot created a role named "TvM Assistant" with the following permissions:

- Manage Channels
- Manage Roles
- Manage Messages
- Read Messages
- Send Messages
- Embed Links
- Add Reactions

These permissions are necessary for the bot to work. If the role is missing, you can create a role manually or reinvite (after kicking) the bot using [this link](https://discordapp.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot). If any permission is missing, please add it manually.

Now that the bot is the server and has the necessary permissions, let's begin the setup.

**Note:** The stuff written inside `<>` and `[]` are called parameters. `<>` means required parameter, `[]` means optional. For example, if there is `<number>` written, simply enter a number, like `12`, without the `<>`. More on types of parameters [below](#parameters).

### Step 1

Configure TvM settings. The following are configurable:

- [`-tvm changena`](#-tvm-changena): Toggle if user can change their night action once submitted. Defaults to `True`.
- [`-tvm total <number>`](#-tvm-total-number): Total number of players that can sign-up for the game. Defaults to `12`.

### Step 2

Use [`-tvm setroles`](#-tvm-setroles) command. It will create `Host`, `Player`, `Replacement`, `Spectator` and `Dead` roles and assign you the `Host` role automatically. Feel free to change the name, color and other properties of these roles. [More about roles.](#roles)

### Step 3

Use [`-tvm setchannels`](#tvm-setchannels) command. It will create sign-ups and night action (host-only) channels. Feel free to move the channels around or change their names. You can also change channel permissions but it may accidentally break some settings. [More about channels.](#channels)

### Step 4

Use the [`-logchannel [channel]`](#-logchannel-channel) command. If you just use `-logchannel`, the bot will create a new channel called `log`. You can also set a channel you've already created as the log channel. Simply mention the channel in the command like this: `-logchannel #channel-name`. All message edits and deletes from **public** channels will be logged in the log channel. [More about logging.](#logging)

We're done with basic configuration! You can lock the TvM settings with the [`-tvm lock`](#-tvm-lock) command. Now we have to wait till people sign-up. Follow the steps below once you've got enough players to start the game.

### Optional Step

The bot has a command to randomly assign a role to a player. See [`-rand <roles>`](#-rand-roles) command.

### Step 5

Create `Player`, `Mafia` and `Spectator` chats.

First, use the [`-playerchats`](#-playerchats-category_name) command. It will also create channels for mafia members, as the bot doesn't know who is town and who is mafia. You can remove them manually.

Second, use [`-mafiachat <mafia1> [mafia2 [mafia3..]]`](#mafiachat-mafia1-mafia2-mafia3) command to create a mafia chat. Example of this command: `-mafiachat Arius#5544 Ligi @Siris#4421`

You can edit the name of player and mafia channels but are recommended to not do so. You can move channels across categories but make sure you choose the **Keep Permissions** option. **Do not change channel permissions.**

Third, use [`-specchat [channel]`](#-specchat-channel) command to create a spectator chat. People with `Spectator` and `Dead` roles can see the spec chat.

You can change names, permissions, etc., without any consequences.

By now, you would have set up all the user channels. Use the commands below only after you've given users their role, flavor, etc., and are ready to start the game.

### Step 6

Create cycle 1 channels. See [`-cycle [number]`](#-cycle-number) and [`-night`](#-night) for more information.

---

Congratulations, all the work is now complete! Just use the `cycle` and `night` commands once every new cycle to keep the game running smoothly.

## Commands Reference

**Note:** The stuff written inside `<>` and `[]` are called parameters. `<>` means required parameter, `[]` means optional. For example, if there is `<number>` written, simply enter a number, like `12`, without the `<>`. More on types of parameters [below](#parameters).

### General

These commands can be used by everyone, unless otherwise stated.

#### `-in [ignored]`

Sign-up for the TvM. Automatically assigns the Player role and removes Spec and Replacement roles, if necessary. You can type anything you want after `-in`.

*Hosts, don't use this command.*

#### `-out [ignored]`

Sign-out of the TvM or spectate it. Automatically assigns the Spectator role and removes Player and Replacement roles, if necessary. You can type anything you want after `-out`. Alias: `-spec`

*Hosts, don't use this command.*

#### `-repl [ignored]`

Sign-up as a replacement. Automatically assigns the Replacement role and removes Player and Spectator roles, if necessary. You can type anything you want after `-repl`.

*Hosts, don't use this command.*

#### `-votecount [channel]`

Counts votes! The bot can automatically detect voting channels. However, it may not be able to detect the correct channel in some cases. Please specify the vote channel in such cases! Alias: `-vc [channel]`

#### `-timesince`

Tells time elapsed since day/night channel was opened. The bot can automatically detect if it's day or night.

#### `-nightaction <action>`

Your night action. It can only be used in your own private channel. `action` can be any text. You may not be able to update your night action if host has disabled that setting. Alias: `-na <action>`

*Can only be used by players.*

### Roles

These commands require administrator permission or the host role.

#### `-tvm hostrole <role>`

Sets `role` as the host role.

*The bot asks for confirmation before making changes.*

#### `-tvm playerrole <role>`

Sets `role` as the player role.

*The bot asks for confirmation before making changes.*

#### `-tvm specrole <role>`

Sets `role` as the spectator role.

*The bot asks for confirmation before making changes.*

#### `-tvm deadrole <role>`

Sets `role` as the dead player role.

*The bot asks for confirmation before making changes.*

#### `-tvm replrole <role>`

Sets `role` as the replacement role.

*The bot asks for confirmation before making changes.*

#### `-tvm setroles`

Creates all the 5 roles and sets them as appropriate automatically. Also adds the host role to the person using command.

### Channels

These commands require administrator permission or the host role.

#### `-tvm nachannel <channel>`

Sets `channel` as the channel where night actions are relayed.

#### `-tvm signup <channel>`

Sets `channel` as the sign-ups channel.

*The bot asks for confirmation before making changes.*

#### `-tvm setchannels`

Creates `signups` and `nachannel` channels and sets them as appropriate automatically.

#### `-playerchats [category_name]`

Sets up private channels for all players. It also sets up individual channels for players who are mafia. You can remove those manually. You can also specify a category name for the channels. Alias: `-pc [category_name]`

#### `-mafiachat <mafia1> [mafia2 [mafia3..]]`

Sets up mafia chat for users specified. Example: `-mafiachat Arius#5544 Ligi @Siris#4421`. Alias: `-mafchat <mafia1> [mafia2 [mafia3..]]`

#### `-specchat [channel]`

Creates spectator chat or fix permissions of an existing channel.

### TvM Specific Settings

These commands require administrator permission or the host role.

#### `-tvm changena`

Toggle if user can change their night action once submitted. Defaults to `True`.

#### `-tvm total <number>`

Sets `number` as the total number of players that can sign-up for the game. Defaults to `12`.

#### `-tvm signopen`

Allows people to sign-up. On by default.

#### `-tvm signclose`

Closes sign-ups.

#### `-tvm lock`

Locks these, role and channel settings (commands that begin with `tvm`). Useful once the configuration is done so you don't accidentally mess things up mid-game.

#### `-tvm unlock`

Unlocks TvM settings.

#### `-tvm settings`

Shows TvM settings. Alias: `-tvm show`

### Cycle Commands

These commands require administrator permission or the host role.

#### `-cycle [number]`

Creates a `Cycle` category with three channels: day, night and voting. Night channel is not visible to anyone except hosts and the bot. The bot maintains a cycle count (which starts at 0). However, the count may be broken in some cases. You can fix the count by specifying the cycle number when using the command. Simply using the `-cycle` command is recommended unless things are broken. Make sure to only use the command once per cycle.

Make sure you have the day opening text ready before using the command. Day and vote channels will be visible to users as soon as they are created.

*The bot asks for confirmation before making changes.*

#### `-night`

Close the day and vote channels and open the night channel. Make sure you post the night starting text, minus the players ping, before using this command. Bot mentions the `Player` role once the channel is opened.

The bot may be unable to identify the correct day/night channels in some cases. In such cases, please open and close the channels yourself.

*The bot asks for confirmation before making changes.*

### Logging

These commands require administrator permission or the host role.

#### `-logchannel [channel]`

Sets or create sthe logging channel. All message edits and deletes from **public** channels will be logged in this channel.

If you just use `-logchannel`, the bot will create a new channel called `log`. You can also set a channel you've already created as the log channel. Simply mention the channel in the command like this: `-logchannel #channel-name`.

#### `-wchannel <channel>`

Whitelists `channel`. The messages in it will be logged irrespective of its permissions (as long as the bot can view this channel).

#### `-bchannel <channel>`

Blacklists `channel`. The messages in it will not be logged irrespective of its permissions. Whitelisting takes precedence over blacklisting. If a channel is in whitelist, the messages WILL BE LOGGED even if you blacklist it.

#### `-rwchannel <channel>`

Removes `channel` from the whitelist.

#### `-rbchannel <channel>`

Removes `channel` from the blacklist.

#### `-logsettings`

Displays log settings.

### Clear

#### `-clear nasubmitted`

Clears the list of users who submitted night action the current cycle.

#### `-clear player`

Removes `Player` role from the bot database.

#### `-clear spec`

Removes `Spectator` role from the bot database.

#### `-clear host`

Removes `Host` role from the bot database.

#### `-clear repl`

Removes `Replacement` role from the bot database. Alias: `-clear replacement`

#### `-clear dead`

Removes `Dead` role from the bot database.

#### `-clear signups`

Removes sign-ups channel from the bot database.

#### `-clear nachannel`

Removes night action channel from the bot database.

### Misc

These commands require administrator permission or the host role, unless otherwise stated.

#### `-host <user>`

Gives the specified user `Host` role.

#### `-rand <roles>`

Randomly assigns a role from the pool to a person with the `Player` role. The command should follow the pattern used in this example: `-rand role1, role2, role3, ...`. Number of players should be equal to number of roles. You can duplicate roles.

#### `-players`

Lists all members with `Player` role.

#### `-replacements`

Lists all members with `Replacement` role.

#### `-kill <user>`

Kills a player by automatically removing player role and adding the dead player role.

#### `-synctotal`

Sometimes the count of signups kept by the bot may not be able to the number of users who have actually signed up. Use this command to bring them into sync.

#### `-started [cycle_number]`

Sometimes the bot can't determine if the game started or not. Use this to fix the issue. `cycle_number` is the number of cycle currently on. Defaults to 1.

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
`roles`: list of comma-separated role names  
`case_number`: a number  
`category_name`: text, doesn't support markdown  
`number`: a number  
`cycle_number`: a number  

## Self Hosting

You can own your own instance of TvM Assistant easily! TvM Assistant runs on [Red](https://github.com/Cog-Creators/Red-DiscordBot), a highly modular Discord bot. Instructions to install and run Red can be found [here](https://github.com/Cog-Creators/Red-DiscordBot#installation). Once you've installed Red, follow these steps:

Replace `[p]` by the your bot's prefix in the below commands.

*Load downloader if you haven't*  
`[p]load downloader`

*Add this repo to the bot*  
`[p]repo add tvm-assist https://github.com/AriusX7/tvm-assistant`

*Install required cogs*  
`[p]cog install tvm-assist tvm`  
`[p]cog install tvm-assist tvmlog` (if you want logging)

*Load cogs*  
`[p]load tvm`  
`[p]load tvmlog` (if installed)  

And that's all! You now have your very own TvM Assistant bot!

**Note:** I update the cogs regularly to make them even better. Use `[p]cog update tvm` and `[p]cog update tvmlog` (if installed) command(s) to update my cogs.

## Credits

- Town of Salem: Bot logo
- [Trusty-cogs](https://github.com/TrustyJAID/Trusty-cogs): Logging events
