import discord
import json
from datetime import datetime

from services.api import UserProgressGameInfo, UserCompletionRecent, UserProfile, UserCompletionProgress, GameUnlocks
from utils.image import get_discord_color
from utils.datetime import ordinal
from config.config import api_key, api_username, DISCORD_IMAGE

from utils.custom_logger import logger

async def process_achievements(users, api_username, api_key, achievements_channel, mastery_channel):
    achievement_embeds = []
    mastery_embeds = []
    for user in users:
        try:
            user_completion = get_user_completion(user, api_username, api_key)
            if user_completion.achievements:
                profile, game_details, game_achievements = get_user_profile_and_achievements(user_completion)
                mastery_count = -1
                for game_id, achievements in game_achievements.items():
                    game = game_details[game_id]
                    process_game_achievements(game, user_completion, achievements, profile, achievement_embeds)
                    if game.is_completed():
                        mastery_count += 1
                        process_game_mastery(game, user_completion, profile, mastery_embeds, mastery_count)
            else:
                logger.info(f'No achievements found for user {user}')
        except Exception as e:
            logger.error(f'Error processing user {user}: {e}')

        logger.info(f'Finished fetching achievements for user {user}')

    await send_achievement_embeds(achievement_embeds, achievements_channel)
    await send_mastery_embeds(mastery_embeds, mastery_channel)

def get_user_completion(user, api_username, api_key):
    user_completion = UserCompletionRecent(user, api_username, api_key)
    logger.info(f'Starting to get achievements for user {user}')
    return user_completion

def get_user_profile_and_achievements(user_completion):
    profile = UserProfile(user_completion.user, api_username, api_key)
    game_details, game_achievements = get_achievements(user_completion)
    return profile, game_details, game_achievements

def process_game_achievements(game, user_completion, achievements, profile, achievement_embeds):
    achievements.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"))
    for i, achievement in enumerate(achievements):
        embed = create_achievement_embed(game, user_completion.user, achievement, profile, i+1, len(achievements))
        achievement_embeds.append((datetime.strptime(achievement.date, "%Y-%m-%d %H:%M:%S"), embed))

def process_game_mastery(game, user_completion, profile, mastery_embeds, mastery_count):
    user_progress = UserCompletionProgress(user_completion.user, api_username, api_key)
    game_unlocks = GameUnlocks(api_username, api_key, game.id)
    unlock_distribution = game_unlocks.get_distribution()
    highest_unlock = unlock_distribution.get_highest_unlock()
    progress = user_progress.get_progress()
    mastered_count = ordinal(int(progress.count_mastered()) - mastery_count)
    mastery_time = game.days_since_last_achievement()
    mastery_percentage = round((highest_unlock / game.total_players_hardcore) * 100, 2)
    if game_progress := next(
        (result for result in progress.results if result.game_id == game.id),
        None,
    ):
        logger.info(f"{user_completion.user} has mastered {game.title}! {game.total_achievements} achievements have been earned in {mastery_time}! {highest_unlock} out of {game.total_players_hardcore} players have mastered the game! ({mastery_percentage}%)")
        mastery_embed = create_mastery_embed(game, user_completion.user, profile, game_progress, mastered_count, mastery_time, highest_unlock, mastery_percentage)
        mastery_embeds.append((datetime.strptime(game_progress.highest_award_date, "%Y-%m-%dT%H:%M:%S%z"), mastery_embed))

async def send_achievement_embeds(achievement_embeds, achievements_channel):
    achievement_embeds.sort(key=lambda x: x[0])
    if achievement_embeds:
        logger.info(f"Sending {len(achievement_embeds)} embeds to {achievements_channel}")
        for embed in achievement_embeds:
            await achievements_channel.send(embed=embed[1])  # Send each embed individually

async def send_mastery_embeds(mastery_embeds, mastery_channel):
    mastery_embeds.sort(key=lambda x: x[0])
    if mastery_embeds:
        logger.info(f"Sending {len(mastery_embeds)} mastery embeds to {mastery_channel}")
        for embed in mastery_embeds:
            await mastery_channel.send(embed=embed[1])  # Send each embed individually

def get_game_details(game_id, username, api_username, api_key):
    try:
        return UserProgressGameInfo(
            game_id, username, api_username, api_key
        ).get_game()
    except Exception as e:
        logger.error(f'Error getting game progress details for game {game_id}: {e}')

def get_achievements(user_completion):
    try:
        achievements = user_completion.get_achievements()
        game_ids = set()
        game_details = {}
        game_achievements = {}

        for achievement in achievements:
            game_ids.add(achievement.game_id)
            logger.info(f"{user_completion.user} has earned an achievement: {achievement.title} ({achievement.points}) ({achievement.retropoints}) for {achievement.game_title}")
            if achievement.game_id not in game_achievements:
                game_achievements[achievement.game_id] = []
            game_achievements[achievement.game_id].append(achievement)

        logger.debug(f'Found {len(game_ids)} unique game IDs in achievements')

        for game_id in game_ids:
            logger.info(f'Getting game progress details for game {game_id}')
            game = get_game_details(game_id, user_completion.user, api_username, api_key)
            game_details[game_id] = game
            logger.info(f'Got game progress details for game {game_id}')

        return game_details, game_achievements
    except Exception as e:
        logger.error(f'Error getting achievements for user {user_completion.user}: {e}')

def create_achievement_embed(game, user, achievement, profile, current, total):
    completion = game.total_achievements_earned - total + current
    percentage = (completion / game.total_achievements) * 100
    unlock_percentage = (game.achievements[achievement.title]['NumAwardedHardcore'] / game.total_players_hardcore) * 100 if game.total_players_hardcore else 0
    most_common_color = get_discord_color(achievement.badge_url)

    # Load emoji mappings
    with open('emoji.json') as f:
        emoji_mappings = json.load(f)
    # Get the emoji ID based on console name, with a general emoji if no specific match is found
    console_name = game.remap_console_name()
    emoji_id = emoji_mappings.get(console_name.lower())
    emoji = f"<:{console_name}:{emoji_id}>" if emoji_id else ":video_game:"

    embed = discord.Embed(
        description=(
            f"**[{achievement.game_title}]({achievement.game_url})** "
            f"{emoji}\n\n"
            f"{achievement.description}\n\n"
            f"Unlocked by **{game.achievements[achievement.title]['NumAwardedHardcore']}** out of "
            f"**{game.total_players_hardcore}** players (**{unlock_percentage:.2f}%**)"
        ),
        color=most_common_color
    )

    # Check if achievement type is 'Missable'
    achievement_title = (
        f"[{achievement.title}]({achievement.url}) (m)"
        if achievement.type == "missable"
        else f"[{achievement.title}]({achievement.url})"
    )

    embed.add_field(name="Achievement", value=achievement_title, inline=True)
    embed.add_field(name="Points", value=f"**{achievement.points}** ({achievement.retropoints_format})", inline=True)
    embed.add_field(name="Completion", value=f"{completion}/{game.total_achievements} (**{percentage:.2f}%**)", inline=True)
    embed.set_image(url=DISCORD_IMAGE)
    embed.set_thumbnail(url=achievement.badge_url)
    embed.set_footer(text=f"{user} • Unlocked on {achievement.date_amsterdam}", icon_url=profile.profile.user_pic_unique)
    embed.set_author(name=f"{achievement.mode} Achievement Unlocked", icon_url=achievement.game_icon)
    return embed

def create_mastery_embed(game, user, profile, game_progress, mastered_count, mastery_time, highest_unlock, mastery_percentage):
    most_common_color = get_discord_color(game.image_icon)
    
    # Load emoji mappings
    with open('emoji.json') as f:
        emoji_mappings = json.load(f)
    # Get the emoji ID based on console name, with a general emoji if no specific match is found
    console_name = game.remap_console_name()
    emoji_id = emoji_mappings.get(console_name.lower())
    emoji = f"<:{console_name}:{emoji_id}>" if emoji_id else ":video_game:"

    embed = discord.Embed(
        description=(
            f"**[{game.title}]({game.url})** "
            f"{emoji}\n\n"
            f"This is [{user}]({profile.profile.user_url})'s **{mastered_count}** mastery!\n\n"
            f"Mastered in {mastery_time}\n\n"
            f"Mastered by {highest_unlock} out of {game.total_players_hardcore} players "
            f"({mastery_percentage}%)"
        ),
        color=most_common_color
    )

    embed.set_footer(
        text=f"{user} • Mastery achieved on {game_progress.highest_award_date_format}",
        icon_url=profile.profile.user_pic_unique
    )
    embed.add_field(name="Achievements", value=f"{game.total_achievements}", inline=True)
    embed.add_field(name="Points", value=f"{game.total_points} ({game.calculate_total_true_ratio()})", inline=True)
    embed.set_author(name="Game Mastered", icon_url=game.image_icon)
    embed.set_image(url=DISCORD_IMAGE)
    embed.set_thumbnail(url=game.image_icon)

    return embed