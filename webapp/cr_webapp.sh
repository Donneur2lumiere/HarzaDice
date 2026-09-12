#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# --- Android SDK ---
: "${ANDROID_HOME:=/usr/lib/android-sdk}"
export ANDROID_HOME
export PATH="$ANDROID_HOME/platform-tools:$PATH"
[ -d "$ANDROID_HOME" ] || { echo "ERREUR: ANDROID_HOME introuvable: $ANDROID_HOME"; exit 1; }

# --- Dossier web dédié (Capacitor refuse webDir=".") ---
WEB_DIR=www
mkdir -p "$WEB_DIR"
test -f "$WEB_DIR/index.html" || { echo "ERREUR: $WEB_DIR/index.html manquant"; exit 1; }

# --- npm ---
[ -f package.json ] || npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android

# --- Capacitor init (non-interactif via </dev/null) ---
npx cap init HarzaDice org.harzadice --web-dir="$WEB_DIR" </dev/null

# --- Plateforme android (idempotent) ---
[ -d android ] || npx cap add android

# --- local.properties pour Gradle ---
echo "sdk.dir=$ANDROID_HOME" > android/local.properties

# --- Sync + build release ---
npx cap sync android
cd android
./gradlew assembleRelease

# --- Rappel emplacement APK ---
echo "APK: $(pwd)/app/build/outputs/apk/release/app-release.apk"
