import discord
from datetime import datetime

from services.api import UserProgressGameInfo, UserCompletionRecent, UserProfile, UserCompletionProgress
from utils.image_utils import get_discord_color
from config.config import api_key, api_username, DISCORD_IMAGE

from utils.custom_logger import logger

async def process_achievements(users, api_username, api_key, achievements_channel, mastery_channel):
    achievement_embeds = []
    mastery_embeds = []
    for user in users:
        try:
            user_completion = UserCompletionRecent(user, api_username, api_key)
            if user_completion.achievements:  # Check if user_completion is not empty before making another API call
                profile = UserProfile(user, api_username, api_key)
                game_details, game_achievements = get_achievements(user_completion)
                for game_id, achievements in game_achievements.items():
                    game = game_details[game_id]
                    achievements.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
                    for i, achievement in enumerate(achievements):
                        embed = create_embed(game, user_completion.user, achievement, profile, i+1, len(achievements))
                        achievement_embeds.append((datetime.strptime(achievement.date, "%Y-%m-%d %H:%M:%S"), embed))
                    if game.is_completed():
                        user_progress = UserCompletionProgress(user, api_username, api_key)
                        progress = user_progress.get_progress()
                        mastered_count = progress.count_mastered()
                        game_progress = next((result for result in progress.results if result.game_id == game.id), None)
                        if game_progress:
                            mastery_embed = create_mastery_embed(game, user_completion.user, profile, game_progress, mastered_count)
                            mastery_embeds.append((datetime.now(), mastery_embed))
        except Exception as e:
            logger.error(f'Error processing user {user}: {e}')

    # Sort by 'date' attribute, converting to datetime if necessary
    achievement_embeds.sort(key=lambda x: x[0])
    mastery_embeds.sort(key=lambda x: x[0])

    if achievement_embeds:
        logger.info(f"Sending {len(achievement_embeds)} embeds to {achievements_channel}")
        for i in range(0, len(achievement_embeds), 10):
            await achievements_channel.send(embeds=[embed[1] for embed in achievement_embeds[i:i+10]])

    if mastery_embeds:
        logger.info(f"Sending {len(mastery_embeds)} mastery embeds to {mastery_channel}")
        for i in range(0, len(mastery_embeds), 10):
            await mastery_channel.send(embeds=[embed[1] for embed in mastery_embeds[i:i+10]])

def get_game_details(game_id, username, api_username, api_key, game_details_cache):
    cache_key = (game_id, username, api_username, api_key)
    if cache_key in game_details_cache:
        logger.debug(f'Using cached game details for game {game_id}')
        return game_details_cache[cache_key]

    try:
        game = UserProgressGameInfo(game_id, username, api_username, api_key).get_game()
        logger.debug(f'Fetched game details for game {game_id}')
        game_details_cache[cache_key] = game
        return game
    except Exception as e:
        logger.error(f'Error getting game details for game {game_id}: {e}')

def get_achievements(user_completion):
    try:
        achievements = user_completion.get_achievements()
        game_ids = set()
        game_details = {}
        game_achievements = {}
        game_details_cache = {}

        for achievement in achievements:
            game_ids.add(achievement.game_id)
            logger.info(f"{user_completion.user} has earned an achievement: {achievement.title} ({achievement.points}) ({achievement.retropoints}) for {achievement.game_title}")
            if achievement.game_id not in game_achievements:
                game_achievements[achievement.game_id] = []
            game_achievements[achievement.game_id].append(achievement)

        for game_id in game_ids:
            game = get_game_details(game_id, user_completion.user, api_username, api_key, game_details_cache)
            game_details[game_id] = game

        return game_details, game_achievements
    except Exception as e:
        logger.error(f'Error getting achievements for user {user_completion.user}: {e}')

def create_embed(game, user, achievement, profile, current, total):
    completion = game.total_achievements_earned - total + current
    percentage = (completion / game.total_achievements) * 100
    unlock_percentage = (game.achievements[achievement.title]['NumAwardedHardcore'] / game.total_players_hardcore) * 100 if game.total_players_hardcore else 0
    most_common_color = get_discord_color(achievement.badge_url)
    embed = discord.Embed(description=f"**[{achievement.game_title}]({achievement.game_url})** ({game.remap_console_name()}) \n\n{achievement.description}\n\nUnlocked by {game.achievements[achievement.title]['NumAwardedHardcore']} out of {game.total_players_hardcore} players ({unlock_percentage:.2f}%)", color=most_common_color)
    
    # Check if achievement type is 'Missable'
    achievement_title = f"[{achievement.title}]({achievement.url}) (m)" if achievement.type == "missable" else f"[{achievement.title}]({achievement.url})"

    embed.add_field(name="Achievement", value=achievement_title, inline=True)
    embed.add_field(name="Points", value=f"{achievement.points} ({achievement.retropoints_format})", inline=True)
    embed.add_field(name="Completion", value=f"{completion}/{game.total_achievements} ({percentage:.2f}%)", inline=True)
    embed.set_image(url=DISCORD_IMAGE)
    embed.set_thumbnail(url=achievement.badge_url)
    embed.set_footer(text=f"{user} • Unlocked on {achievement.date_amsterdam}", icon_url=profile.profile.user_pic_unique)
    embed.set_author(name=f"{achievement.mode} Achievement Unlocked", icon_url=achievement.game_icon)
    return embed

def create_mastery_embed(game, user, profile, game_progress, mastered_count):
    most_common_color = get_discord_color(game.image_icon)
    embed = discord.Embed(description=f"**This is {user}'s {mastered_count}th mastery!**", color=most_common_color)
    embed.set_footer(text=f"{user} • Mastery achieved on {game_progress.highest_award_date_format}", icon_url=profile.profile.user_pic_unique)
    embed.add_field(name="Game", value=f"[{game.title}]({game.url}) ({game.remap_console_name()})", inline=True)
    embed.add_field(name="Achievements", value=f"{game.total_achievements}", inline=True)
    embed.add_field(name="Points", value=f"{game.total_points}", inline=True)
    embed.set_author(name=f"Game Mastered", icon_url=game.image_icon)
    embed.set_image(url=DISCORD_IMAGE)
    embed.set_thumbnail(url=game.image_icon)
    return embed