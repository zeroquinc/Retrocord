import discord

from services.api import UserCompletionByDate, UserProfile

from utils.image_utils import get_discord_color
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
            fav_game, fav_game_achievements, fav_url, fav_console_name, fav_game_points, fav_game_retropoints = favorite_game(user_completion)
            logger.info(f"{user} has earned {achievement_count} achievements today, totaling {daily_points} points and {daily_retropoints} RetroPoints. Their favorite game is {fav_game} with {fav_game_achievements} achievements.")
            embed = create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, fav_game, fav_game_achievements, fav_url, fav_console_name, fav_game_points, fav_game_retropoints)
            all_embeds.append(embed)
        except Exception as e:
            logger.error(f'Error processing user {user}: {e}')

    if all_embeds:
        logger.info(f"Sending {len(all_embeds)} embeds to {channel}")
        for i in range(0, len(all_embeds), 10):
            await channel.send(embeds=all_embeds[i:i+10])

def count_daily_points(user_completion):
    achievements = user_completion.get_achievements()
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
    achievements = user_completion.get_achievements()
    if achievements:  # checks if the sequence is not empty
        max_achievement = max(achievements, key=lambda achievement: (achievement.points, achievement.retropoints)) # Find the achievement with the most points, if there are multiple, the one with the highest RetroPoints is chosen
    else:
        max_achievement = None
    return max_achievement

def favorite_game(user_completion):
    achievements = user_completion.get_achievements()
    # Initialize an empty dictionary to store game counts, URLs, console names, points, and retropoints
    game_counts = {}
    for achievement in achievements:
        # If the game title is already in the dictionary, increment its count and add the points and retropoints
        if achievement.game_title in game_counts:
            game_counts[achievement.game_title][0] += 1
            game_counts[achievement.game_title][3] += achievement.points
            game_counts[achievement.game_title][4] += achievement.retropoints
        # If the game title is not in the dictionary, add it with a count of 1, store the URL, console name, points, and retropoints
        else:
            game_counts[achievement.game_title] = [1, achievement.game_url, achievement.remap_console_name(), achievement.points, achievement.retropoints]
    # Find the game with the most achievements
    if game_counts:  # checks if the dictionary is not empty
        favorite_game = max(game_counts, key=lambda x: game_counts[x][0])
        fav_game_points = game_counts[favorite_game][3]
        fav_game_retropoints = game_counts[favorite_game][4]
        # Format fav_game_points and fav_game_retropoints if they are greater than or equal to 10000
        fav_game_points = format(fav_game_points, ',').replace(',', '.') if fav_game_points >= 10000 else str(fav_game_points)
        fav_game_retropoints = format(fav_game_retropoints, ',').replace(',', '.') if fav_game_retropoints >= 10000 else str(fav_game_retropoints)
        return favorite_game, game_counts[favorite_game][0], game_counts[favorite_game][1], game_counts[favorite_game][2], fav_game_points, fav_game_retropoints
    else:
        return None, None, None, None, None, None  # Return None if the dictionary is empty
    
def create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, fav_game, fav_game_achievements, fav_url, fav_console_name, fav_game_points, fav_game_retropoints):
    # Set Embed color based on max_achievement
    if max_achievement is not None:
        embed_color = get_discord_color(max_achievement.badge_url)
    else:
        embed_color = get_discord_color(profile.profile.user_pic_unique)
    
    # Create a base Embed object
    embed = discord.Embed(
        title='',
        description='',
        color=embed_color
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
        )
        embed.description = f"""[{profile.profile.user}]({profile.profile.user_url}) has earned **{achievement_count}** achievements today.

        [{fav_game}]({fav_url}) ({fav_console_name}) is the game with the most earned achievements today.\n**{fav_game_achievements}** achievements worth **{fav_game_points}** Points and **{fav_game_retropoints}** RetroPoints.

        [{max_achievement.title}]({max_achievement.url}) from [{max_achievement.game_title}]({max_achievement.game_url}) ({max_achievement.remap_console_name()}) is the top achievement of the day.\n**{max_achievement.points}** Points and **{max_achievement.retropoints_format}** RetroPoints.
        
        ***{daily_points}** Points and **{daily_retropoints}** RetroPoints have been earned in total today.*

        """
    else:
        embed.description = 'Nothing has been earned today.'

    return embed