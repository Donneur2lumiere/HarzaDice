# HarzaDice - Webapp + APK Android via Capacitor

L'application web (HTML/JS) reprend la même logique et la même UI que la version desktop Tkinter, dans un format portable et encapsulable en APK Android.

## Contenu

- `harzadice_core.js` : logique métier (port JS fidèle de `harzadice_core.py` — mêmes probabilités, même calcul des cas critiques). Hasard "cryptographique suffisant mais pas réel" via `crypto.getRandomValues`.
- `index.html` : interface (5 boutons colorés + type d'arme + LANCER/Oublie), identique en comportement à la version Tkinter.

## Test rapide (navigateur)

Ouvrir `index.html` dans un navigateur — aucun build requis.

## Build APK Android (via Capacitor)

Prérequis : Node.js et Android Studio (SDK) installés.

```bash
cd webapp

# 1. Créer un projet Capacitor
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init HarzaDice org.harzadice --web-dir=.

# 2. Ajouter la plateforme Android
npx cap add android

# 3. Synchroniser les assets web
npx cap sync

# 4. Build de l'APK debug
cd android
./gradlew assembleDebug
# APK produit dans android/app/build/outputs/apk/debug/app-debug.apk
```

L'APK est une WebView Android encapsulant la webapp. Aucune compilation CPython, aucun Buildozer/p4a — la logique tourne en JavaScript natif dans la WebView.
