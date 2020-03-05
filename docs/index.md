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
  <a href="">Introduction</a>
  •
  <a href="quickstart.md">Quickstart</a>
  •
  <a href="commands-reference.md">Commands Reference</a>
  •
  <a href="parameters.md">Parameters</a>
  •
  <a href="#self-hosting">Self Hosting</a>
  •
  <a href="#credits">Credits</a>
</p>

## Introduction

TvM Assistant is a Discord bot with utility commands to make hosting TvMs easier. You can invite it to your server by using [this link](https://discordapp.com/api/oauth2/authorize?client_id=680383600725590020&permissions=268494928&scope=bot). Inviting the bot will give it `Manage Channels`, `Manage Roles`, `Manage Messages`, `Add Reactions` and `Embed Links` permissions in addition to `Read` and `Send` messages perm.

## Quickstart

Detailed instructions on how to quickly set up the bot in your server can be found [here](quickstart.md).

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
