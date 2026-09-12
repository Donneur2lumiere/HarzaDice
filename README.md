# HarzaDice 🎲

Special dice for the role-playing game **« Monde »**.

Application permettant de lancer des dés avec des règles personnalisées dans l'univers « Monde ». Trois interfaces coexistent : un **bot Discord** (Python), une **application desktop** (Tkinter), et une **webapp** encapsulable en APK Android via Capacitor.

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

---

## 📖 Règles du jeu

Les dés sont de 4 couleurs reflétant le talent, la chance ou les difficultés dans un combat. Classés par ordre croissant :

| Couleur | Code | Talent |
|---------|------|--------|
| Rouge   | `R`  | + faible |
| Orange  | `O`  |  |
| Noir    | `N`  |  |
| Vert    | `V`  |  |
| Bleu    | `B`  | + fort |

Chaque dé n'a que 4 valeurs : **Fumble** (💀 crâne), **Critique** (★ étoile), **1** et **2** (touches).

On indique le type d'arme pour varier les critiques. Les résultats Fumble & Critique s'annulent :
- S'il reste des **Critiques** → +4 touches chacun
- S'il reste des **Fumbles** → -1 et offre 1 touche à l'adversaire
- Si le nombre de Fumble & Critique ouvre des cas critiques → désarmement, etc.

On multiplie ensuite le nombre de touches par l'index de dégât de l'arme. Cela garantit des combats expéditifs et calculables de tête.

### Exemple

Commande : `C+5R+5N+2B` (5 dés rouges, 5 noirs, 2 bleus, arme courte)

Résultat possible :
```
Résultat = 10 & ★★ ; Défenseur Cas1 : [ 0,'★', 2, 2, 2, '★', 2, '★', 2, 0, '💀', 2 ]
```

---

## 🗂️ Structure du dépôt

```
HarzaDice/
├── bot/                 # Bot Discord (Python, discord.py)
│   ├── HarzaDice_V4-App.py   # Version 0.4 (dernière, case-insensitive)
│   ├── HazaDice_V4.py        # Version 0.4 avec variable TOKEN
│   └── HazaDice_V2.py        # Version 2 (historique)
├── desktop/             # Application PC (interface graphique Tkinter)
│   └── HarzaDice.py         # GUI : 5 boutons colorés + type d'arme + LANCER/Oublie
├── webapp/              # Webapp HTML/JS + build APK Android (Capacitor)
│   ├── www/                  # index.html + harzadice_core.js (logique métier)
│   ├── android/              # Projet Android Capacitor (gradle, manifest, ressources)
│   ├── capacitor.config.json
│   ├── cr_webapp.sh          # Script de build release
│   └── package.json
├── assets/              # appicon.png
├── docs/                # README détaillé, LICENSE, PRIVACY_POLICY, TERMS_OF_SERVICE
└── .gitignore
```

---

## 🚀 Utilisation

### Bot Discord

```bash
cd bot
python3 HarzaDice_V4-App.py
```

Le token Discord doit être fourni via la variable d'environnement `DISCORD_TOKEN` (voir `bot/HazaDice_V4.py` pour la version avec variable `TOKEN`).

Dans Discord, entrer le type d'arme et le nombre de dés voulu, ex : `C+5R+5N+2B`.

### Application PC (Tkinter)

```bash
cd desktop
python3 HarzaDice.py
```

Clic gauche sur un dé de couleur pour incrémenter le nombre de dés de cette couleur, choisir le type d'arme, puis **LANCER !**. Re-cliquer **LANCER !** relance le même nombre de dés ; **Oublie...** remet à zéro.

### Webapp (navigateur)

Ouvrir `webapp/www/index.html` dans un navigateur — aucun build requis.

### Build APK Android

Prérequis : Node.js et Android SDK installés.

```bash
cd webapp
./cr_webapp.sh    # npm install + cap sync + gradle assembleRelease
# APK produit dans webapp/android/app/build/outputs/apk/release/app-release.apk
```

---

## 📦 Installation

```bash
git clone https://github.com/Donneur2lumiere/HarzaDice.git
cd HarzaDice
```

### Bot Discord — dépendances Python

```bash
pip install discord.py
```

### Webapp — dépendances Node

```bash
cd webapp
npm install
```

---

## 🔐 Sécurité

Le `.gitignore` exclut systématiquement les fichiers sensibles :
- `*.keystore`, `keystore.properties` — le keystore Android reste local, jamais commité
- `.env`, `secrets.*` — tokens et secrets
- `node_modules/` — dépendances régénérées via `npm install`

---

## 📄 Licence

[![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
