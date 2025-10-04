import random
import re

def lancer_de(des, nombre=1):
    # Définir les valeurs et leurs poids pour chaque dé
    des_probas = {
        'R': {
            'values': ['⛤', '☠', 0, 1, 2],
            'weights': [1, 2, 7, 4, 2]
        },
        'O': {
            'values': ['⛤', '☠', 0, 1, 2],
            'weights': [1, 1, 8, 3, 3]
        },
        'N': {
            'values': ['⛤', '☠', 0, 1, 2],
            'weights': [1, 1, 7, 3, 4]
        },
        'V': {
            'values': ['⛤', '☠', 0, 1, 2],
            'weights': [1, 1, 6, 2, 6]
        },
        'B': {
            'values': ['⛤', '☠', 0, 1, 2],
            'weights': [2, 1, 5, 1, 7]
        }
    }

    # Obtenir les valeurs et poids pour le dé spécifié
    values = des_probas[des]['values']
    weights = des_probas[des]['weights']

    # Lancer le dé le nombre de fois spécifié
    results = random.choices(values, weights=weights, k=nombre)
    return results

def parser_commande(commande):
    # Extraire le type d'arme
    type_arme = commande[0]
    # Utiliser une expression régulière pour trouver toutes les occurrences de la forme <nombre><lettre>
    pattern = r'(\d+)([RONVB])'
    matches = re.findall(pattern, commande[2:])  # Ignorer les 2 premiers caractères (type_arme et '+')
    return type_arme, matches

def calculer_somme_et_effet(resultats, type_arme):
    # Compter le nombre de ⛤ et ☠
    nb_etoiles = resultats.count('⛤')
    nb_tetes_de_mort = resultats.count('☠')

    # Calculer la valeur des symboles restants
    if nb_etoiles > nb_tetes_de_mort:
        valeur_symboles = 4
        symboles_restants = ['⛤'] * (nb_etoiles - nb_tetes_de_mort)
        nb_symboles_restants = nb_etoiles - nb_tetes_de_mort
    elif nb_tetes_de_mort > nb_etoiles:
        valeur_symboles = -1
        symboles_restants = ['☠'] * (nb_tetes_de_mort - nb_etoiles)
        nb_symboles_restants = nb_tetes_de_mort - nb_etoiles
    else:
        valeur_symboles = 0
        symboles_restants = []
        nb_symboles_restants = 0

    # Calculer la somme des valeurs numériques
    somme_numerique = 0
    for resultat in resultats:
        if isinstance(resultat, int):
            somme_numerique += resultat

    # Total
    total = somme_numerique + valeur_symboles

    # Déterminer l'effet en fonction du type d'arme et du nombre de symboles restants
    effets = {
        'C': {2: 'Cas1', 3: 'Cas2', 4: 'Cas3', 5: 'Cas4', 6: 'Cas5'},
        'M': {2: 'Cas1', 3: 'Cas2', 4: 'Cas3', 5: 'Cas4', 6: 'Cas5'},
        'D': {2: 'Cas1', 3: 'Cas2', 4: 'Cas3', 5: 'Cas4'}
    }

    if nb_etoiles > nb_tetes_de_mort:
        # Défenseur
        effet = effets[type_arme].get(nb_symboles_restants, '')
        partie = "Défenseur"
    elif nb_tetes_de_mort > nb_etoiles:
        # Attaquant
        effet = effets[type_arme].get(nb_symboles_restants, '')
        partie = "Attaquant"
    else:
        effet = ''
        partie = ''

    return total, symboles_restants, effet, partie

def main():
    commande = input("Entrez votre commande de lancer de dés (par exemple, D+3N+1B) : ")
    type_arme, matches = parser_commande(commande)

    resultats = []
    for nombre, des in matches:
        nombre = int(nombre)
        results = lancer_de(des, nombre)
        resultats.extend(results)

    # Calculer la somme et l'effet selon les nouvelles règles
    total, symboles_restants, effet, partie = calculer_somme_et_effet(resultats, type_arme)

    # Afficher les résultats
    symboles_restants_str = ''.join(str(s) for s in symboles_restants)
    print(f"Résultat = {total} & {symboles_restants_str} ; {partie} {effet} : {resultats}")

if __name__ == "__main__":
    main()
