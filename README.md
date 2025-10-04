# HarzaDice
Special dice for the role-playing game "Monde". CC BY-SA-NC.
Une application pour lancer des dés avec des règles personnalisées dans l'univers "Monde".

## Description

Cette application permet de lancer des dés avec des règles personnalisées pour les jeux de rôle et autres jeux de société. Elle prend en charge différents types de dés et applique des règles spécifiques pour le calcul des résultats.
Les dé sont de 4 couleurs relétant le talent, la chance ou les difficultés dans un combat.
Classé par ordre croissant R Rouge, O Orange, N Noir, V Vert, B Bleu
chaque dé n'a que 4 valeurs Fumble (crâne) Critique (étoile) 1 & 2 (touches)
On indique le type d'arme utiliser pour varier les critiques
Les résultats Fumble & Critique s'annulent.
S'ils en reste (quelquesoit le nombre) Critique rajoute 4 touches
Fumble -1 et offre 1 touche a l'adversaire 
En revanche s'il le nombre de Fumble & Critique cela ouvre des Cas critique (désarmement etc...)
Il suffit aprés de multiplier le nombre de touche par l'index de dégat de l'arme.
Cela garantit des combats expếditif et calculable de tête

## utilisation
lancer HazaDice.py
entrer le type d'arme et le nombre de dé voulu
Par exemple :
C+5R+5N+2B   (lance 5 dé rouge, 5 noirs et 2 bleus avec une arme courte)
ce qui pourrait renvoyer renvoyer :
Résultat = 10 & ⛤⛤ ; Défenseur Cas1 : [ 0,'⛤', 2, 2, 2, '⛤', 2, '⛤', 2, 0, '☠', 2 ]


## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/dice-roller.git

## Discord : 
A VENIR



[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC BY--NC--SA 4.0-lightgrey.svg
