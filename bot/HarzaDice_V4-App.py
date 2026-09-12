import discord
from discord.ext import commands
import random
import re
import asyncio
# Version 0.4
# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Définition des variables globales pour les effets
CAS1 = ''
CAS2 = 'Désarmé, -1 ‬ si dragone, Si 2* dragone casse ou -2 ‬'
CAS3 = 'Arme brisée'
CAS4 = 'Chute -1🎲, & -1 ‬ pour se relever, -1🎲 -1 ‬ sup pour 2M'
CAS5 = 'Se blesse ⚄4, C 1M 1*Đ, 2M D 2*Đ'
CAS6 = 'Perte de doigt, -1🎲 Permanent'
CAS6D = 'Le projectile rebondit Blessure T2 ⚄4, Hémoragie = Σ☠ ou Σ⛤'
CAS7 = "S'assomme = fin du combat pour vous"

MESSAGES_AMBIANCE = {
    671409208373280788: "Hackeurman vient de nouveau frapper avec un retantissant (jet)",
    742676044112330813: "Avec (jet) ce zozo vas encore chouiner",
    1094258141245489152: "La ptite salope de Masskor a encore tout déglingué avec (jet)",
    1333027720333889660: "Hadrien a obtenu (jet) mais il a surement triché",
    556759904967458816: "Sa grandeur a de nouveau obtenu (jet)",
    700716543822004224: "Bouc sort de sa barbe au moins (jet) il n’est pas en forme.",
    671401755577155584: "Sournoisement Washrog glisse (jet) c’est incroyable",
    600405837135085569: "D’un décalage temporel sort (jet)",
    220302752985776128: "Et paf (jet) les orks sont pourtant interdit ici !",
    371397762673278977: "Avec (jet) peu on dire qu’elle couche avec leMJ ?",
    1212016821369315369: "Le Max s’offre au minimum (jet) Honteux !",
    1164164874130178138: "L’impitoyable tueur de cochon sort (jet) Vengeance !!!",
    690544117343715329: "Le Grand Architecte de l’Univers (jet)",
}

def lancer_de(des, nombre=1):
    des_probas = {
        'R': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 3, 8, 2, 2]},
        'O': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 2, 6, 5, 2]},
        'N': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [1, 1, 6, 5, 3]},
        'V': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [2, 1, 4, 5, 4]},
        'B': {'values': ['⛤', '☠', 0, 1, 2], 'weights': [3, 1, 3, 4, 5]}
    }
    values = des_probas[des]['values']
    weights = des_probas[des]['weights']
    return random.choices(values, weights=weights, k=nombre)

def parser_commande(commande):
    # L'arme est imposee a 'M' (Moyenne) sur Discord : l'utilisateur ne tape
    # que le declencheur et les des (couleur + nombre), ex: "5R+5N+2B".
    type_arme = 'M'
    pattern = r'(\d*)([RONVB])'
    matches = [(n or '1', d.upper()) for n, d in re.findall(pattern, commande, re.IGNORECASE)]
    return type_arme, matches

def calculer_somme_et_effet(resultats, type_arme):
    global CAS2, CAS3, CAS4, CAS5, CAS6, CAS7

    nb_etoiles = resultats.count('⛤')
    nb_tetes_de_mort = resultats.count('☠')

    effets = {
        'C': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
        'M': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5, 6: CAS6, 7: CAS7},
        'D': {2: CAS2, 3: CAS3, 4: CAS4, 5: CAS5}
    }

    if nb_etoiles > nb_tetes_de_mort:
        valeur_symboles = 4
        nb_symboles_restants = nb_etoiles - nb_tetes_de_mort
        symboles_restants = ['⛤'] * nb_symboles_restants
        if nb_symboles_restants == 1:
            effet = "Vous avez gagné 4 touches !"
            partie = "Attaquant"
        else:
            effet = effets[type_arme].get(nb_symboles_restants, "")
            partie = "Défenseur"
    elif nb_tetes_de_mort > nb_etoiles:
        valeur_symboles = -2
        nb_symboles_restants = nb_tetes_de_mort - nb_etoiles
        symboles_restants = ['☠'] * nb_symboles_restants
        if nb_symboles_restants == 1:
            effet = "Vous avez perdu 2 touches et votre adversaire en a gagné 1"
            partie = "Attaquant"
        else:
            effet = effets[type_arme].get(nb_symboles_restants, "")
            partie = "Attaquant"
    else:
        valeur_symboles = 0
        symboles_restants = []
        nb_symboles_restants = 0
        effet = ""
        partie = ""

    somme_numerique = sum(r for r in resultats if isinstance(r, int))
    total = somme_numerique + valeur_symboles

    return total, symboles_restants, effet, partie


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='purge')
async def purge(ctx, nombre: int = 30):
    if ctx.author.id != 123456789012345678:
        await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        return

    await ctx.channel.purge(limit=nombre + 1)
    message = await ctx.send(f"✅ {nombre} messages ont été supprimés.")
    await asyncio.sleep(3)
    await message.delete()


@bot.command(name='r')
async def r(ctx, *, commande: str):
    try:
        type_arme, matches = parser_commande(commande)
        resultats = []
        for nombre, des in matches:
            resultats.extend(lancer_de(des, int(nombre)))

        total, symboles_restants, effet, partie = calculer_somme_et_effet(resultats, type_arme)
        symboles_restants_str = ''.join(str(s) for s in symboles_restants)

        username = ctx.author.display_name
        message = MESSAGES_AMBIANCE.get(ctx.author.id)
        if message is None:
            message = f"{username} a lancé {commande}\n"
        else:
            message = message.replace("(jet)", commande) + "\n"

        if symboles_restants:
            message += f"Total = {total} & {symboles_restants_str}     :     {resultats}\n"
        else:
            message += f"Total = {total}     :     {resultats}\n"

        if partie:
            message += f"{partie} : {effet}"

        await ctx.send(message)
        try:
            await ctx.message.delete()
        except discord.DiscordException:
            pass
    except Exception as e:
        await ctx.send(f"Erreur : {e}. Veuillez vérifier votre commande.")

bot.run('TOKEN-HERE')
