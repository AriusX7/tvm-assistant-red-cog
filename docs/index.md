<h1 align="center">
  <a href="https://discord.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot">
  Invite!
  </a>
  <br>
</h1>

<p align="center">
  <a href="#introduction">Introduction</a>
  •
  <a href="#features">Features</a>
  •
  <a href="quickstart">Quickstart</a>
  •
  <a href="commands-reference">Commands Reference</a>
  •
  <a href="parameters">Parameters</a>
  •
  <a href="#self-hosting">Self Hosting</a>
  •
  <a href="#credits">Credits</a>
</p>

## Introduction

TvM Assistant is a Discord bot with utility commands to make hosting TvMs easier. You can invite it to your server by using [this link](https://discord.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot). Inviting the bot will give it `Manage Channels`, `Manage Roles`, `Manage Messages`, `Add Reactions` and `Embed Links` permissions in addition to `Read` and `Send` messages perm.

## Features

- Creates necessary setup roles and channels
- In-built logging which detects and ignores private channels
- Manages sign ups, sign outs and replacements
- Supports quick creation of player, mafia and spectator chats
- Manages cycle channels
- Relays night actions to a single host-only channel
- Vote counts and time since day/night started
- And more!

Suggest a feature by sending me a message on Discord (Arius#5544).

## Quickstart

Detailed instructions on how to quickly set up the bot in your server can be found [here](quickstart).

## Commands Reference

All bot commands are documented in detail [here](commands-reference).

## Parameters

Various parameters used in bot commands are explained in detail [here](parameters).

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
