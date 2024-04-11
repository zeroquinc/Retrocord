import discord

from services.api import UserCompletionByDate, UserProfile

from utils.image_utils import get_most_common_color
from utils.time_utils import get_now_and_yesterday_epoch
from config.config import DISCORD_IMAGE, RETRO_DAILY_IMAGE

from utils.custom_logger import logger

async def process_daily_overview(users, api_username, api_key, channel):
    all_embeds = []
    for user in users:
        try:
            yesterday, now = get_now_and_yesterday_epoch()
            user_completion = UserCompletionByDate(user, api_username, api_key, yesterday, now)
            profile = UserProfile(user, api_username, api_key)
            achievement_count, daily_points, daily_retropoints = count_daily_points(user_completion)
            max_achievement = find_max_achievement(user_completion)
            fav_game, fav_game_achievements, fav_url = favorite_game(user_completion)
            logger.info(f"{user} has earned {achievement_count} achievements today, totaling {daily_points} points and {daily_retropoints} RetroPoints. Their favorite game is {fav_game} with {fav_game_achievements} achievements.")
            embed = create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, fav_game, fav_url)
            all_embeds.append(embed)
        except Exception as e:
            logger.error(f'Error processing user {user}: {e}')

    if all_embeds:
        logger.info(f"Sending {len(all_embeds)} embeds to {channel}")
        for i in range(0, len(all_embeds), 10):
            await channel.send(embeds=all_embeds[i:i+10])

def count_daily_points(user_completion):
    achievements = user_completion.get_achievements()  # replace get_achievements() with the actual method or attribute
    if achievements:  # checks if the sequence is not empty
        achievement_count = len(achievements)
        daily_points = sum(achievement.points for achievement in achievements)
        daily_retropoints = sum(achievement.retropoints for achievement in achievements)
    else:
        achievement_count = 0
        daily_points = 0
        daily_retropoints = 0

    # Format daily_points and daily_retropoints if they are greater than or equal to 10000
    daily_points = format(daily_points, ',').replace(',', '.') if daily_points >= 10000 else str(daily_points)
    daily_retropoints = format(daily_retropoints, ',').replace(',', '.') if daily_retropoints >= 10000 else str(daily_retropoints)

    return achievement_count, daily_points, daily_retropoints

def find_max_achievement(user_completion):
    achievements = user_completion.get_achievements()  # replace get_achievements() with the actual method or attribute
    if achievements:  # checks if the sequence is not empty
        max_achievement = max(achievements, key=lambda achievement: (achievement.points, achievement.retropoints)) # Find the achievement with the most points, if there are multiple, the one with the highest RetroPoints is chosen
    else:
        max_achievement = None
    return max_achievement

def favorite_game(user_completion):
    achievements = user_completion.get_achievements()  # replace get_achievements() with the actual method or attribute
    # Initialize an empty dictionary to store game counts and URLs
    game_counts = {}
    for achievement in achievements:
        # If the game title is already in the dictionary, increment its count
        if achievement.game_title in game_counts:
            game_counts[achievement.game_title][0] += 1
        # If the game title is not in the dictionary, add it with a count of 1 and store the URL
        else:
            game_counts[achievement.game_title] = [1, achievement.game_url]
    # Find the game with the most achievements
    if game_counts:  # checks if the dictionary is not empty
        favorite_game = max(game_counts, key=lambda x: game_counts[x][0])
        return favorite_game, game_counts[favorite_game][0], game_counts[favorite_game][1]
    else:
        return None, None, None  # Return None if the dictionary is empty
    
def create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, fav_game, fav_url):
    most_common_color = get_most_common_color(profile.profile.user_pic_unique)
    
    # Create a base Embed object
    embed = discord.Embed(
        title='',
        description='',
        color=most_common_color
    ).set_footer(
        text=f"Total Points: {profile.profile.total_points_format} • Total RetroPoints: {profile.profile.total_true_points_format}",
        icon_url=profile.profile.user_pic_unique
    ).set_author(
        name=f"Daily Overview for {profile.profile.user}",
        icon_url=RETRO_DAILY_IMAGE
    ).set_image(
        url=DISCORD_IMAGE
    )

    # Conditionally add fields based on max_achievement
    if max_achievement is not None:
        embed = embed.set_thumbnail(
            url=max_achievement.badge_url
        ).add_field(
            name="Game of the Day", value=f"[{fav_game}]({fav_url})", inline=False
        ).add_field(
            name="Achievement of the Day", value=f"[{max_achievement.title}]({max_achievement.url}) ({max_achievement.points}) ({max_achievement.retropoints_format})", inline=False
        ).add_field(
            name="Points", value=f"{daily_points} ({daily_retropoints})", inline=True
        ).add_field(
            name="Unlocks", value=achievement_count, inline=True
        )
    else:
        embed.description = 'Nothing has been earned today.'

    return embed