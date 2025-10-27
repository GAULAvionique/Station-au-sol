# Configuration de la carte SD

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)

---

La station au sol possède un Raspberry Pi 4B, il faut alors installer et configurer un système d'exploitation qui va faire fonctionner le backend et l'affichage de l'interface.

## Installation de Raspberry Pi OS

Insérer la carte SD du Raspberry Pi dans un ordinateur.

Lancer [Raspberry Pi Imager](https://www.raspberrypi.com/software/) v1.8.4

_Modèle :_ Raspberry Pi 4 \
_Système d'exploitation :_ Raspberry Pi OS (32-bit) \
_Stockage :_ SD CARD

_Would you like to apply OS customization settings?_ \
\> Modifier réglages

**Général**

_Nom d'hôte :_ gaul-sas

**\[X\] Définir nom d'utilisateur et mot de passe** \
_Nom d'utilisateur :_ gaul \
_Mot de passe :_ saspassword

**\[X] Configurer le Wi-Fi** \
_SSID :_ \<Nom du hotspot Wi-FI\> \
_Mot de passe :_ \<Mot de passe du hotspot Wi-Fi\>

(Je conseille de créer un hotspot avec un téléphone ou un ordinateur pour plus facilement accéder au Raspberry Pi en [SSH](https://www.raspberrypi.com/documentation/computers/remote-access.html) par la suite)

_Pays Wi-fi :_ CA

_Fuseau horaire :_ America/Toronto \
_Type de clavier :_ ca

**Services**

\[x\] Activer SSH \
(x) Utiliser un mot de passe pour l'authentification

\> Enregistrer

\> Oui

_Toutes les données sur le périphérique de stockage vont être supprimées._ \
_Voulez-vous vraiment continuer ?_ \
\> Oui

## Mise en marche et mise à jour du Raspberry Pi

Mettre la carte SD dans le Raspberry Pi et l'allumer.

Attendre que le Raspberry Pi ouvre (quand la DEL verte arrête de clignoter), puis entrer dans le terminal d'un ordinateur connecté sur le même réseau Wi-Fi que le Raspberry Pi:

```bash
ssh gaul@gaul-sas.local
```

_Are you sure you want to continue connecting (yes/no/\[fingerprint\])?_ \
\> yes

_password:_ saspassword

(Voir la [documentation officielle](https://www.raspberrypi.com/documentation/computers/remote-access.html) en cas de problème)

Une fois connecté en SSH au Raspberry Pi, mettre à jour les packages avec:

```bash
sudo apt update && sudo apt full-upgrade -y
```

Puis redémarrer le Raspberry Pi:

```bash
sudo reboot
```

---

Prochaine étape: [Configuration de la station au sol](./raspi-config-setup-sas.md)

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)
