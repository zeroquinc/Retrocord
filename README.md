# Retrocord

This bot is designed to keep track of your achievements and share them with your friends on Discord.

Support for:

[RetroAchievements](https://retroachievements.org)
[Sony PSN](https://www.playstation.com)

Some features:

* Achievement embeds with configurable intervals for multiple users
* Daily Overview embeds for multiple users
* Clickable links to the RetroAchievement site
* Set Completion
* Amount of Points & RetroPoints
* Achievement of the Day & Game of the Day!

## Examples

<table>
  <tr>
    <td>
      <img src="https://github.com/zeroquinc/Retrocord/assets/39315068/4eaaefb7-3a87-452a-86f8-d1ed0f2ddc41" alt="image1">
    </td>
    <td>
      <img src="https://github.com/zeroquinc/Retrocord/assets/39315068/75f3bfa2-c08a-4852-819a-71f6fccfaa0e" alt="image2">
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/zeroquinc/Retrocord/assets/39315068/e06d49ee-5e5d-4205-8899-1dfb5aedb0c5" alt="image3">
    </td>
    <td>
      <img src="https://github.com/zeroquinc/Retrocord/assets/39315068/5aa85411-27a1-4063-98b5-144f1f46b434" alt="image4">
    </td>
  </tr>
</table>

## Getting your PSN API Key

To get started you need to obtain npsso <64 character code>. You need to follow the following steps

1. Login into your My PlayStation account.

2. In another tab, go to https://ca.account.sony.com/api/v1/ssocookie

3. If you are logged in you should see a text similar to this

```
{"npsso":"<64 character npsso code>"}
```

This npsso code will be used in the api for authentication purposes. The refresh token that is generated from npsso lasts about 2 months.
From: https://psnawp.readthedocs.io/en/latest/additional_resources/README.html#getting-started

## Getting Started

To get started with Retrocord, follow these steps:

1. Clone the repository to your local machine or download the latest release
2. Navigate to the project directory
3. Install the dependecies with `pip install -r requirements.txt`
4. Navigate to `/config/`, rename `config_example.py` to `config.py` and fill in the variables
5. Run the bot: `python3 bot.py &`
