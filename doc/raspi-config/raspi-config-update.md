# Comment mettre à jour la station au sol à partir du GitHub

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)

---

## Accès à distance au Raspberry Pi en SSH

Se connecter au Wi-Fi du Raspberry Pi (`gaul-sas`) avec un ordinateur. Le mot de passe est `saspassword`. Puis accéder au Raspberry Pi en SSH avec:

```bash
ssh gaul@gaul-sas.local
```

_Are you sure you want to continue connecting (yes/no/\[fingerprint\])?_ \
\> yes

_password:_ saspassword

(Voir la [documentation officielle](https://www.raspberrypi.com/documentation/computers/remote-access.html) en cas de problème)

## **NOUVELLE MÉTHODE AUTOMATIQUE**

Une fois connecté à la station au sol à distance en SSH, lancer le script de mise à jour:

```bash
bash ~/Station-au-sol/tools/raspi_update.sh
```

En cas de problème pour exécuter le script, entrer:

```bash
chmod +x ~/Station-au-sol/tools/raspi_update.sh
```

## Ancienne méthode: connecter la station au sol à internet

S'assurer qu'un réseau Wi-Fi avec internet est disponible et accessible par le Raspberry Pi. Je conseille de créer un point d'accès (hotspot) avec un téléphone ou un ordinateur pour faciliter le processus.

**Pour ajouter une connexion Wi-Fi au Raspberry Pi à partir du terminal:**

Scanner les réseaux Wi-Fi disponibles:

```bash
sudo nmcli device wifi list
```

Puis se connecter au réseau désiré avec:

```bash
sudo nmcli device wifi connect <Nom Wi-FI> password <Mot de passe Wi-Fi>
```

**Si le réseau a déjà été configuré, on peut simplement enlever le hotspot, et le Raspberry Pi devrait se reconnecter automatiquement**

```bash
sudo nmcli con delete gaul-sas
```

### IMPORTANT: Se reconnecter à la station au sol

Si on était connecté à la station au sol en SSH, il faut se reconnecter après avoir créé le point d'accès. Pour ce faire, il faut:

1. Se connecter au point d'accès Wi-Fi (ssid: **gaul-sas**, password: **saspassword**)
2. Puis se reconnecter en SSH (voir [Accès à distance au Raspberry Pi en SSH](#accès-à-distance-au-raspberry-pi-en-ssh)).

## Mettre à jour la station à partir du GitHub

<!-- Il y a deux options pour mettre à jour la station au sol:

**Option 1:**

Utiliser le script:

```bash
cd ~/Station-au-sol/scripts/
chmod +x raspi_update.sh
./raspi_update.sh
```

**Option 2:** -->

Fermer le backend de la station avec:

```bash
sudo killall node
```

Aller dans le répertoire qui contient le repo GitHub:

```bash
cd ~/Station-au-sol/
```

Récupérer les fichiers à partir du GitHub (se connecter avec un token GitHub au besoin):

```bash
git pull
```

Installer les nouvelles dépendances du projet:

```bash
cd backend/
npm install
```

Puis redémarrer:

```bash
sudo reboot
```

## Note pour Spaceport America Cup

Le code pour la station au sol se trouve sur la branche `sac24`, donc il faut probablement retourner sur la branche main si on veut utiliser la station après SAC.

Pour changer de branche:

```bash
git switch <BRANCH NAME>
```

---

Retour aux [guides pour configurer le Raspberry Pi](./raspi-config.md)
