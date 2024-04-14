"""	
This is an example configuration file. You should rename this file to config.py and fill in the values.

api_key: Your RetroAchievements API key
api_username: Your RetroAchievements username that belongs to the API key
token: Your Discord bot token
users: A list of RetroAchievements usernames to track, for example ["User1", "User2", "User3"]

DISCORD_IMAGE: The image URL to use for Discord embeds, this uses a transparent image by default to set a max width, recommended not to change
RETRO_DAILY_IMAGE: The image URL to use for the daily RetroAchievements embed, this is a placeholder by default

ACHIEVEMENTS_CHANNEL_ID: The Discord channel ID to send achievement updates to
DAILY_OVERVIEW_CHANNEL_ID: The Discord channel ID to send the daily RetroAchievements embed to
API_INTERVAL: The number of minutes to wait between Achievement requests, default is 15 minutes, minimum is 1 minute
"""

api_key = ""
api_username = ""
token = ''
users = []

DISCORD_IMAGE = "https://i.postimg.cc/KvSTwcQ0/undefined-Imgur.png"
RETRO_DAILY_IMAGE = "https://i.imgur.com/P0nEGGs.png"

ACHIEVEMENTS_CHANNEL_ID = ""
DAILY_OVERVIEW_CHANNEL_ID = ""
MASTERY_CHANNEL_ID = ""
API_INTERVAL = 15