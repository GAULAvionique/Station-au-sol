#!/bin/bash

echo "=== Arrêt du logiciel ==="
sudo killall node

cd ~/Station-au-sol/ || { echo "Erreur : dossier Station-au-sol introuvable"; exit 1; }

echo
echo "=== Information de connexion à un point d'accès Wi-Fi ==="
read -p "Entrez le nom (SSID) du point d'accès Wi-Fi : " WIFI_SSID
read -s -p "Entrez le mot de passe du point d'accès Wi-Fi : " WIFI_PASS

echo
echo "=== Sélection de la branche Git à utiliser ==="
read -p "Entrez le nom de la branche à utiliser (irec ou main) : " GIT_BRANCH

echo
echo "L'accès à distance via SSH va être interrompu, la station au sol devrait redémarrer après s'être mise à jour."
echo "Veuillez ensuite vous reconnecter à son point d'accès Wi-Fi (gaul-sas), puis en SSH."
echo
echo "Rappel de la commande de connexion SSH :"
echo "ssh gaul@gaul-sas.local"
echo "Écrire 'yes' si vous êtes invité à accepter la clé d'hôte."
echo "Le mot de passe est : saspassword"
echo
echo "En cas de problème, redémarrez la station au sol manuellement et reconnectez-vous à son point d'accès Wi-Fi (gaul-sas)."
echo
echo "=== Début de la mise à jour ==="

sudo nmcli device wifi rescan

sudo nmcli device wifi connect "$WIFI_SSID" password "$WIFI_PASS"

sleep 5

git fetch
git switch "$GIT_BRANCH"
git pull

cd backend/ || { echo "Erreur : dossier backend/ introuvable"; exit 1; }
npm install

sudo reboot