# Configuration de la station au sol

Étape précédente: [Configuration de la carte SD](./raspi-config-flash-sd.md)

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)

---

Une fois le système d'exploitation du Raspberry Pi installé et à jour, il faut télécharger et installer les fichiers et logiciels nécessaires au fonctionnement de la station au sol.

## Accès à distance au Raspberry Pi en SSH

Entrer dans le terminal d'un ordinateur connecté sur le même réseau Wi-Fi que le Raspberry Pi:

```bash
ssh gaul@gaul-sas.local
```

_Are you sure you want to continue connecting (yes/no/\[fingerprint\])?_ \
\> yes

_password:_ saspassword

(Voir la [documentation officielle](https://www.raspberrypi.com/documentation/computers/remote-access.html) en cas de problème)

## Installation de Node.js

Node.js permet d'exécuter le backend de la station au sol écrit en Javascript.

Ajouter la source:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
```

Installer Node.js et npm:

```bash
sudo apt install -y nodejs npm
```

## Télécharger le code de la station au sol à partir de GitHub

Tous les fichiers nécessaires pour la station au sol se trouvent sur GitHub.

Entrer la commande pour cloner le repo (publique ou privé):

```bash
git clone https://github.com/GAULAvionique2024-2025/Station-au-sol.git
```

Ensuite, changer de répertoire:

```bash
cd Station-au-sol/backend
```

Puis installer les dépendances du projet:

```bash
npm install
```

## Configuration du mode kiosque

Pour ouvrir automatiquement l'interface de la station au sol au démarrage du Raspberry Pi, il faut le configurer en mode kiosque:

[Tutoriel - How to use Raspberry Pi in kiosk mode](https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/)

Configurer Wayfire, qui est utilisé pour afficher le bureau du Raspberry Pi:

```bash
sudo nano ~/.config/wayfire.ini
```

Ajouter les lignes:

```
[autostart]
chromium = chromium-browser --app=http://localhost:8080 --noerrdialogs --no-first-run --enable-features=OverlayScrollbar

screensaver = false
```

Ensuite `ctrl` + `x`, `y`, puis `Enter` pour sauvegarder le fichier.

## Configuration du mode point d'accès (hotspot) Wi-Fi

Pour permettre aux autres appareils de se connecter à la station au sol et accéder à l'interface, il faut configurer l'antenne Wi-Fi en mode hotspot:

[Tutoriel - Setup wifi hotspot](https://www.baeldung.com/linux/setup-wifi-hotspot) \
[Documentation nmcli](https://developer-old.gnome.org/NetworkManager/stable/nmcli.html)

La commande à exécuter est:

```bash
sudo nmcli device wifi hotspot con-name gaul-sas ssid gaul-sas password saspassword
```

**Explication de la commande:** \
_nmcli:_ Network Manager Command Line Interface \
_device wifi:_ Pour gérer le Wi-Fi \
_hotspot:_ Pour créer un hotspot \
_con-name gaul-sas:_ Le nom de la configuration \
_ssid gaul-sas:_ Le nom du réseau \
_password saspassword:_ Le mot de passe du réseau

---

### S'il y a l'erreur `Error: NetworkManager is not running`

Ouvrir les paramètres du Raspberry Pi avec:

```bash
sudo raspi-config
```

Aller dans `Advanced Options` \
Puis dans `Network Config` \
Puis choisir `NetworkManager`

Et relancer le Raspberry Pi:

```bash
sudo reboot
```

---

### IMPORTANT: Se reconnecter à la station au sol

Si on était connecté à la station au sol en SSH, il faut se reconnecter après avoir créé le point d'accès. Pour ce faire, il faut:

1. Se connecter au point d'accès Wi-Fi (ssid: **gaul-sas**, password: **saspassword**)
2. Puis se reconnecter en SSH (voir [Accès à distance au Raspberry Pi en SSH](#accès-à-distance-au-raspberry-pi-en-ssh)).

---

### Comment se connecter à un autre réseau Wi-Fi

En mode point d'accès (hotspot), le Raspberry Pi n'a pas accès à internet, donc il peut être utile en général de se connecter à un réseau Wi-Fi qui a accès à internet.

Pour se connecter à un nouveau réseau Wi-Fi, scanner les réseaux disponibles:

```bash
nmcli device wifi list
```

Puis se connecter au réseau Wi-Fi désiré:

```bash
nmcli device wifi connect <Nom Wi-FI> password <Mot de passe Wi-Fi>
```

**Si le réseau a déjà été configuré, il suffit d'enlever le hotspot et le Raspberry Pi va se connecter au réseau Wi-Fi disponible:**

```bash
sudo nmcli connection delete gaul-sas
```

**Note:** après avoir changé le Wi-Fi, il faut se reconnecter en SSH (voir [Se reconnecter à la station au sol](#important-se-reconnecter-à-la-station-au-sol))

## Lancer le backend et mettre le mode point d'accès automatiquement au démarrage

Pour lancer le backend de la station et pour activer le mode point d'accès (hotspot) automatiquement au démarrage du Raspberry Pi:

[Tutoriel - How to run a program on your Raspberry Pi at startup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

Exécuter la commande:

```bash
sudo nano /etc/rc.local
```

Ajouter les lignes avant `exit 0`:

```bash
# Start node.js
sudo node /home/gaul/Station-au-sol/backend/server.mjs &
# Set hotspot
sudo nmcli device wifi hotspot con-name gaul-sas ssid gaul-sas password saspassword &
```

\* _le '&' est important à la fin pour indiquer que les commandes sont à exécuter en arrière plan._

Ensuite `ctrl` + `x`, `y`, puis `Enter` pour sauvegarder le fichier.

Pour tester si tout fonctionne:

```bash
sudo reboot
```

On peut ensuite se connecter au Raspberry Pi sur le Wi-Fi _'**gaul-sas**'_ avec le mot de passe _'**saspassword**'_, puis accéder au site web de l'interface sur [http://gaul-sas.local:8080](http://gaul-sas.local:8080)

\* _Sur Android, il faut entrer l'adresse IP du Raspberry Pi pour accéder à l'interface. Donc il suffit d'exécuter `ping gaul-sas.local` sur une machine Windows pour récupérer l'adresse IP du Raspberry Pi._

---

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)
