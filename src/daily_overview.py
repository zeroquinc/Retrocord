import discord

from services.api import UserCompletionByDate, UserProfile
from utils.image_utils import get_discord_color
from utils.time_utils import get_now_and_yesterday_epoch
from config.config import DISCORD_IMAGE, RETRO_DAILY_IMAGE
from utils.custom_logger import logger

def format_points(points):
    return format(points, ',').replace(',', '.') if points >= 10000 else str(points)

async def process_daily_overview(users, api_username, api_key, channel):
    all_embeds = []
    for user in users:
        try:
            yesterday, now = get_now_and_yesterday_epoch()
            user_completion = UserCompletionByDate(user, api_username, api_key, yesterday, now)
            profile = UserProfile(user, api_username, api_key)
            achievements = user_completion.get_achievements()
            achievement_count, daily_points, daily_retropoints = count_daily_points(achievements)
            max_achievement = find_max_achievement(achievements)
            fav_game_details = favorite_game(achievements)
            logger.info(f"{user} has earned {achievement_count} achievements today, totaling {daily_points} points and {daily_retropoints} RetroPoints. Their favorite game is {fav_game_details[0]} with {fav_game_details[1]} achievements.")
            embed = create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, *fav_game_details)
            all_embeds.append(embed)
        except Exception as e:
            logger.error(f'Error processing user {user}: {e}')

    if all_embeds:
        logger.info(f"Sending {len(all_embeds)} embeds to {channel}")
        for i in range(0, len(all_embeds), 10):
            await channel.send(embeds=all_embeds[i:i+10])

def count_daily_points(achievements):
    achievement_count = len(achievements) if achievements else 0
    daily_points = sum(achievement.points for achievement in achievements) if achievements else 0
    daily_retropoints = sum(achievement.retropoints for achievement in achievements) if achievements else 0
    return achievement_count, format_points(daily_points), format_points(daily_retropoints)

def find_max_achievement(achievements):
    return max(achievements, key=lambda achievement: (achievement.points, achievement.retropoints), default=None)

def favorite_game(achievements):
    game_counts = {}
    for achievement in achievements:
        game = game_counts.setdefault(achievement.game_title, [0, achievement.game_url, achievement.remap_console_name(), 0, 0])
        game[0] += 1
        game[3] += achievement.points
        game[4] += achievement.retropoints
    if game_counts:
        return extract_favorite_game(game_counts)
    return None, None, None, None, None, None

def extract_favorite_game(game_counts):
    favorite_game = max(game_counts, key=lambda x: game_counts[x][0])
    fav_details = game_counts[favorite_game]
    return favorite_game, fav_details[0], fav_details[1], fav_details[2], format_points(fav_details[3]), format_points(fav_details[4])

def create_embed(profile, achievement_count, daily_points, daily_retropoints, max_achievement, fav_game, fav_game_achievements, fav_url, fav_console_name, fav_game_points, fav_game_retropoints):
    embed_color = get_discord_color(max_achievement.badge_url if max_achievement else profile.profile.user_pic_unique)
    embed = discord.Embed(title='', description='', color=embed_color).set_footer(
        text=f"Total Points: {profile.profile.total_points_format} • Total RetroPoints: {profile.profile.total_true_points_format}",
        icon_url=profile.profile.user_pic_unique
    ).set_author(
        name=f"Daily Overview for {profile.profile.user}",
        icon_url=RETRO_DAILY_IMAGE
    ).set_image(
        url=DISCORD_IMAGE
    )
    if max_achievement:
        embed.set_thumbnail(url=max_achievement.badge_url)
        embed.description = (
            f"[{profile.profile.user}]({profile.profile.user_url}) has earned **{achievement_count}** achievements today.\n\n"
            f"[{fav_game}]({fav_url}) ({fav_console_name}) is the game with the most earned **({fav_game_achievements})** achievements today.\n"
            f"**{fav_game_points}** Points and **{fav_game_retropoints}** RetroPoints.\n\n"
            f"[{max_achievement.title}]({max_achievement.url}) from [{max_achievement.game_title}]({max_achievement.game_url}) ({max_achievement.remap_console_name()}) is the top achievement of the day.\n"
            f"**{max_achievement.points}** Points and **{max_achievement.retropoints_format}** RetroPoints.\n\n"
            f"***{daily_points}** Points and **{daily_retropoints}** RetroPoints have been earned in total today.*"
        )
    else:
        embed.description = 'Nothing has been earned today.'
    return embed