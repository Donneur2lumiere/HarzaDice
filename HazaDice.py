import discord
from discord.ext import commands
import random
import re

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Définition des variables globales pour les effets
CAS1 = ''
CAS2 = 'Désarmé, -1 Ԭ si dragone, Si 2* dragone casse ou -2 Ԭ'
CAS3 = 'Arme brisée'
CAS4 = 'Chute -1🎲, & -1 Ԭ pour se relever, -1🎲 -1 Ԭ sup pour 2M'
CAS5 = 'Se blesse ɸ4, C 1M 1*Đ, 2M D 2*Đ'
CAS6 = 'Perte de doigt, -1🎲 Permanent'
CAS6D = 'Le projectile rebondit Blessure T2 ɸ4, Hémoragie = Σ☠ ou Σ⛤'
CAS7 = 'S’assomme = fin du combat pour vous'

def lancer_de(des, nombre=1):
    des_probas = {
        'R': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 2, 7, 4, 2]},
        'O': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 1, 8, 3, 3]},
        'N': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 1, 7, 3, 4]},
        'V': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 1, 6, 2, 6]},
        'B': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [2, 1, 5, 1, 7]}
    }
    values = des_probas[des]['values']
    weights = des_probas[des]['weights']
    return random.choices(values, weights=weights, k=nombre)

def parser_commande(commande):
    type_arme = commande.split('+')[0]
    pattern = r'(\d+)([RONVB])'
    matches = re.findall(pattern, commande)
    return type_arme, matches

def calculer_somme_et_effet(resultats, type_arme):
    global CAS1

    # Définir le dictionnaire 'effets' AVANT de l'utiliser
    effets = {
        'C': {1: CAS1, 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
        'M': {1: CAS1, 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
        'D': {1: CAS1, 2: CAS2, 3: CAS3, 4: CAS4, 5: CAS6, 6: CAS6D, 7: CAS7}
    }

    nb_etoiles = resultats.count('⛤')
    nb_tetes_de_mort = resultats.count('☠')

    if nb_etoiles > nb_tetes_de_mort:
        valeur_symboles = 4
        nb_symboles_restants = nb_etoiles - nb_tetes_de_mort
        max_cas = max(effets[type_arme].keys())
        nb_symboles_restants = min(nb_symboles_restants, max_cas)
        symboles_restants = ['⛤'] * nb_symboles_restants
        CAS1 = 'Vous avez gagné 4 touches !'
    elif nb_tetes_de_mort > nb_etoiles:
        valeur_symboles = -2
        nb_symboles_restants = nb_tetes_de_mort - nb_etoiles
        max_cas = max(effets[type_arme].keys())
        nb_symboles_restants = min(nb_symboles_restants, max_cas)
        symboles_restants = ['☠'] * nb_symboles_restants
        CAS1 = 'Vous avez perdu 2 touches et votre adversaire en a gagné 1'
    else:
        valeur_symboles = 0
        symboles_restants = []
        nb_symboles_restants = 0

    somme_numerique = sum(r for r in resultats if isinstance(r, int))
    total = somme_numerique + valeur_symboles

    if nb_etoiles > nb_tetes_de_mort and nb_symboles_restants > 0:
        effet = effets[type_arme].get(nb_symboles_restants, '')
        partie = "Défenseur"
    elif nb_tetes_de_mort > nb_etoiles and nb_symboles_restants > 0:
        effet = effets[type_arme].get(nb_symboles_restants, '')
        partie = "Attaquant"
    else:
        effet = ''
        partie = ''

    return total, symboles_restants, effet, partie

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='roll')
async def roll(ctx, *, commande: str):
    try:
        type_arme, matches = parser_commande(commande)
        resultats = []
        for nombre, des in matches:
            resultats.extend(lancer_de(des, int(nombre)))

        total, symboles_restants, effet, partie = calculer_somme_et_effet(resultats, type_arme)
        symboles_restants_str = ''.join(str(s) for s in symboles_restants)

        # Messages personnalisés en fonction du nom d'utilisateur
        username = ctx.author.display_name
        if username == "Lightbringer":
            message = f"Le Grand Architecte de l'Univers {username} a lancé {commande}\n"
        elif username == "UN-AUTRE-NOM":
            message = f"UN-AUTRE-TEXTE  {username} a lancé {commande}\n"
        
        else:
            message = f"{username} a lancé {commande}\n"

        if symboles_restants:
            message += f"Total = {total} & {symboles_restants_str}     :     {resultats}\n"
        else:
            message += f"Total = {total}     :     {resultats}\n"

        if partie:
            message += f"{partie} : {effet}"

        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Erreur : {e}. Veuillez vérifier votre commande.")

bot.run('TOKEN-HERE')
