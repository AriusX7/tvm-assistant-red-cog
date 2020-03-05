<h1 align="center"><a href="index">Main Index</a></h1>

<p align="center">
  <a href="#prerequisities">Prerequisities</a>
  •
  <a href="#step-1">Step 1</a>
  •
  <a href="#step-2">Step 2</a>
  •
  <a href="#step-3">Step 3</a>
  •
  <a href="#step-4">Step 4</a>
  •
  <a href="#optional-step">Optional Step</a>
  •
  <a href="#step-5">Step 5</a>
  •
  <a href="#step-6">Step 6</a>
  •
</p>

Follow the steps below to quicky set up the bot for your game. You must have `administrator` permissions to use some of the commands. If you're a player looking to check the commands you can use, see [General](commands-reference#general) and [Misc](commands-reference#misc) sections.

## Prerequisites

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

**Note:** The stuff written inside `<>` and `[]` are called parameters. `<>` means required parameter, `[]` means optional. For example, if there is `<number>` written, simply enter a number, like `12`, without the `<>`. More on types of parameters [here](parameters).

## Step 1

Configure TvM settings. The following are configurable:

- [`-tvm changena`](commands-reference#-tvm-changena): Toggle if user can change their night action once submitted. Defaults to `True`.
- [`-tvm total <number>`](commands-reference#-tvm-total-number): Total number of players that can sign-up for the game. Defaults to `12`.

## Step 2

Use [`-tvm setroles`](commands-reference#-tvm-setroles) command. It will create `Host`, `Player`, `Replacement`, `Spectator` and `Dead` roles and assign you the `Host` role automatically. Feel free to change the name, color and other properties of these roles. [More about roles.](commands-reference#roles)

## Step 3

Use [`-tvm setchannels`](commands-reference#tvm-setchannels) command. It will create sign-ups and night action (host-only) channels. Feel free to move the channels around or change their names. You can also change channel permissions but it may accidentally break some settings. [More about channels.](commands-reference#channels)

## Step 4

Use the [`-logchannel [channel]`](commands-reference#-logchannel-channel) command. If you just use `-logchannel`, the bot will create a new channel called `log`. You can also set a channel you've already created as the log channel. Simply mention the channel in the command like this: `-logchannel #channel-name`. All message edits and deletes from **public** channels will be logged in the log channel. [More about logging.](commands-reference#logging)

We're done with basic configuration! You can lock the TvM settings with the [`-tvm lock`](commands-reference#-tvm-lock) command. Now we have to wait till people sign-up. Follow the steps below once you've got enough players to start the game.

## Optional Step

The bot has a command to randomly assign a role to a player. See [`-rand <roles>`](commands-reference#-rand-roles) command.

## Step 5

Create `Player`, `Mafia` and `Spectator` chats.

First, use the [`-playerchats`](commands-reference#-playerchats-category_name) command. It will also create channels for mafia members, as the bot doesn't know who is town and who is mafia. You can remove them manually.

Second, use [`-mafiachat <mafia1> [mafia2 [mafia3..]]`](commands-reference#mafiachat-mafia1-mafia2-mafia3) command to create a mafia chat. Example of this command: `-mafiachat Arius#5544 Ligi @Siris#4421`

You can edit the name of player and mafia channels but are recommended to not do so. You can move channels across categories but make sure you choose the **Keep Permissions** option. **Do not change channel permissions.**

Third, use [`-specchat [channel]`](commands-reference#-specchat-channel) command to create a spectator chat. People with `Spectator` and `Dead` roles can see the spec chat.

You can change names, permissions, etc., without any consequences.

By now, you would have set up all the user channels. Use the commands below only after you've given users their role, flavor, etc., and are ready to start the game.

## Step 6

Create cycle 1 channels. See [`-cycle [number]`](commands-reference#-cycle-number) and [`-night`](commands-reference#-night) for more information.

---

Congratulations, all the work is now complete! Just use the `cycle` and `night` commands once every new cycle to keep the game running smoothly.
