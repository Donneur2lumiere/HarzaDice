# HarzaDice 🎲

Special dice for the role-playing game **« Monde »**.

Application permettant de lancer des dés avec des règles personnalisées dans l'univers « Monde ». Deux interfaces coexistent : un **bot Discord** (Python, interface CLI) et une **webapp** HTML/JS servant à la fois de version PC (navigateur) et d'APK Android (via Capacitor).

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
├── bot/                 # Bot Discord (Python, discord.py) — interface CLI
│   └── HazaDice.py          # Version 0.4 (de référence, case-insensitive, TOKEN)
├── webapp/              # Interface web HTML/JS — version PC (navigateur) + APK Android
│   ├── www/                  # index.html (UI responsive) + harzadice_core.js (logique métier)
│   ├── lancer.py             # Lanceur multiplateforme (Win/Linux/macOS) — serveur local + navigateur
│   ├── lancer.sh             # Raccourci Linux/macOS
│   ├── lancer.bat            # Raccourci Windows
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
python3 HazaDice.py
```

Le token Discord doit être fourni dans la variable `TOKEN` du fichier `bot/HazaDice.py`.

Dans Discord, entrer le déclencheur et les dés (couleur + nombre), ex : `!r 5R+5N+2B`. L'arme est imposée à `M` (Moyenne) ; une lettre seule vaut 1 dé (`!r n` = 1 Noir). Le message de commande est effacé après le résultat.

### Interface web / PC (navigateur)

**Lancement automatisé** (recommandé) — un seul script démarre le serveur local et ouvre le navigateur :

```bash
cd webapp
./lancer.sh          # Linux / macOS
cd webapp
lancer.bat           # Windows
```

Le serveur tourne sur `http://localhost:8000`. Un bouton **Quitter** (dans la marge basse du cadre) arrête le serveur et ferme l'onglet. Ctrl+C dans le terminal fonctionne aussi.

**Ouverture manuelle** (sans serveur) : ouvrir `webapp/www/index.html` dans un navigateur — aucun build requis. Attention : ouvrir le fichier directement via `file://` bloque le chargement du JS externe, le mode serveur (`lancer.py`) est préférable.

Clic sur un dé de couleur pour incrémenter le nombre de dés, choisir le type d'arme (boutons radio poussoir), puis **LANCER !**. Re-cliquer **LANCER !** relance le même nombre de dés ; **Oublie...** remet à zéro.

La barre de mode en haut permet de simuler la résolution d'un écran de téléphone : **Portrait** (390×760), **Paysage** (760×390) ou **Plein écran**. Sur mobile réel, cette barre est masquée (le viewport gère l'orientation).

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
