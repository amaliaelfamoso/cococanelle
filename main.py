import discord
from discord.ext import commands
import os
#from keep_alive import keep_alive

prefix = "!"  

# Définir les intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True  # Activer l'intent message_content

# Création du bot avec les intents
bot = commands.Bot(command_prefix=prefix, intents=intents)

# ID du salon récompense où le message sera envoyé
reward_channel_id = 1221823292290367488  # Remplacez ceci par l'ID de votre salon récompense

# Dictionnaire des paires salon-rôle
channels_and_roles = {
    1219393758349754388: 1221771417058541668,   # ID_du_salon_2: ID_du_rôle_2 SELFIES
    1220168897890881566: 1221771419990626424,  # ID_du_salon_3: ID_du_rôle_3 OUFTITS
    1219393826121322577: 1221771414596747365,   # ID_du_salon_4: ID_du_rôle_4 COMMENTAIRES 
    1219399629507137587: 1221771395990683728,  # ID_du_salon_7: ID_du_rôle_7 NUDES F
    1219399614592061521: 1221771393767706625,   # ID_du_salon_8: ID_du_rôle_8 NUDES H
    1219399689980481588: 1221771390575706112,  # ID_du_salon_9: ID_du_rôle_9 NUDES A
    1219399712159825940: 1221771387450953808,   # ID_du_salon_10: ID_du_rôle_10 NUDES C
    1219399736801492992: 1221771385429299261,  # ID_du_salon_11: ID_du_rôle_11 COMMENTAIRES NUDES
    1219393702083166298: 1221773145002868778,  # ID_du_salon_12: ID_du_rôle_12 ANIMAUX
    1219395527800786984: 1221773148282945606,   # ID_du_salon_13: ID_du_rôle_13 OTAKU
    1219393564337897612: 1220381889412726815,  # ID_du_salon_14: ID_du_rôle_14 ARTISTE
    1219395563796303924: 1221771431956709469,   # ID_du_salon_15: ID_du_rôle_15 NERD
    1219393733980848199: 1221771429180211241,  # ID_du_salon_16: ID_du_rôle_16 MEME
    1220751254360162447: 1221771425518583883,   # ID_du_salon_17: ID_du_rôle_17 ATHLETE
    1219393641676537856: 1221771422482038834,  # ID_du_salon_18: ID_du_rôle_18 GOURMET
    1219395156160155678: 1221771409148215407,   # ID_du_salon_19: ID_du_rôle_19 ANECDOTE
    1219395949043122256: 1221771406451281941,  # ID_du_salon_20: ID_du_rôle_20 DÉBAT
    # Ajoutez ici les autres paires salon-rôle

}

# Dictionnaire pour stocker les compteurs de messages pour chaque salon
message_counts = {channel_id: {} for channel_id in channels_and_roles}

# Seuil pour l'attribution du rôle
role_threshold = 5  # Seuil pour le nombre de messages

# Incrémenter le compteur de messages pour chaque message envoyé
@bot.event
async def on_message(message):
    for channel_id, role_id in channels_and_roles.items():
        if message.author != bot.user and message.channel.id == channel_id:
            member_id = message.author.id
            if member_id not in message_counts[channel_id]:
                message_counts[channel_id][member_id] = 0
            message_counts[channel_id][member_id] += 1
            await check_role_threshold(channel_id, role_id)  # Vérifier si un rôle doit être attribué après chaque message
            break  # Sortir de la boucle une fois que le salon est trouvé
    await bot.process_commands(message)

# Tâche asynchrone pour vérifier le seuil et attribuer le rôle
async def check_role_threshold(channel_id, role_id):
    for member_id, count in message_counts[channel_id].items():
        member = bot.get_guild(1218600144887615489).get_member(member_id)  # Obtenir l'objet membre à partir de l'ID de l'utilisateur
        if member:
            # Vérifier si le membre a déjà le rôle
            if count >= role_threshold and role_id not in [role.id for role in member.roles]:
                # Retirer le rôle à tous les membres qui l'ont déjà
                for guild_member in member.guild.members:
                    if role_id in [role.id for role in guild_member.roles]:
                        await guild_member.remove_roles(discord.Object(role_id))

                # Attribuer le rôle au membre
                role_to_assign = member.guild.get_role(role_id)
                if role_to_assign:
                    await member.add_roles(role_to_assign)
                    print(f"Rôle attribué à {member.name}")

                    # Envoyer un message dans le salon récompense
                    reward_channel = bot.get_channel(reward_channel_id)
                    if reward_channel:
                        await reward_channel.send(f"Félicitations {member.mention} ! Tu as obtenu le rôle **{role_to_assign.name}** pour avoir contribué au salon ainsi qu'un boost d'xp.")

# Événement de connexion
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")

#keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
