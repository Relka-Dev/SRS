---
title: "Installation du Système de Reconnaissance Spatiale"
author: "Svoboda Karel Vilém"
affiliation: "CFPT Informatique"
date: "2024-06-10"
---

# Installation du Système de Reconnaissance Spatiale

Ce fichier explique les étapes d'installation du projet.

## Caméras wifi

Le système vise à mettre en place des caméras WiFi compactes pour la surveillance ou pour d'autres applications nécessitant la capture et la diffusion en temps réel de flux vidéo. Le cœur du système, un Raspberry Pi Zero 2 W, exécute un serveur Python Flask.

### Composants requis

| Composant                                    | Fonction                    |
|----------------------------------------------|-----------------------------|
| Raspberry Pi Zero 2 W                        | Serveur (Python Flask)      |
| Raspberry Pi Camera Module 3                 | Module de Caméra            |
| MediaRange Power Bank 2600 mAh               | Batterie externe            |
| SanDisk ExtremePro microSD A1                | Carte mémoire               |

### Impression du support

Le support permet de maintenir les composants en place.

#### Détails

- Temps d'impréssion : Environ 8 heures
- Imprimante 3D : Creality CR20PRO
- Carte mémoire requise.

#### Étapes pour l'impression

1. Installation de CURA.
    1. Téléchargez le fichier d'installation depuis [le site d'ultimaker](https://ultimaker.com/de/software/ultimaker-cura/).
    2. Démarrez CURA
    3. Ajoutez votre imprimante, sois par réseau, sois en ajoutant manuellement votre modèle. Puis appuyez sur next.
    4. Continez sans changer les paramètres et terminez l'installation.
2. Ajoutez le fichier `.std` à CURA.
    1. Dans CURA, appuyez sur **Files > Open File(S)**
    2. Naviguez jusqu'au fichier `std`. Son lien dans le projet est `./docs-server/docs/supports/srs-support-0.2.stl`.
3. Démarrer l'impression.
    1. Cliquez sur le support présent dans l'espace 3D.
    2. Appuyez sur `Scale(s)`
    3. Passez la valeur `y` à **50**.
    4. Appuyez sur `Slice`.
    5. Appuyez sur `Save to disk`.
5. Lancez l'impression.
    1. Mettez la **carte mémoire** dans l'imprimante et lancez l'impression.

### Installtion des Raspberry

Ce chapitre explique l'installation logicielle des Rapberry.

1. Installation de Pi Imager
    1. Installer l'application depuis [le site de Raspberry](https://www.raspberrypi.com/software/).

#### Installation de l'OS

1. Insérez la carte mémoire dans le lecteur.
2. Cliquez sur `Choose a device`.
    1. Cliquez sur `Raspberry Zero W 2`
3. Cliquez sur `Choose à OS`.
    1. Séléctionnez `Raspberry Pi OS (other)`
    2. Cliquez sur `Raspberry Pi OS (Legacy), 64 bits`, assurez vous que ce soit la version Bulleseye.
4. Cliquez sur `Choose storage`.
    1. Cliquez sur votre support d'installation.
5. Cliquez sur `Next`.
    1. Sur la fenêtre `Use OS calibration`, cliquez sur `Edit Settings`.
    2. Dans `General Settings`, définissez un nom d'utilisateur et un mot de passe. Puis, ajoutez les données du réseau Wifi.
    3. Dans `Service`, activez `ssh`.

#### Installation de l'environnement


1. Activez la fonctionnalité `legacy camera`
```
sudo raspi-config
Interface Options -> Enable Legacy Camera -> Yes -> Reboot
```

2. Clonez le projet sur le serveur
```
sudo apt install git
git clone https://gitlab.ictge.ch/karel-svbd/srs.git
```

3. Naviguez jusqu'au projet des cameras.
```shell
cd srs/src/cameras_wifi/src/
```

4. Créez un environnement virtuel et activez le.
```shell
sudo apt install python3-venv
python -m venv venv
source venv/bin/activate
```

5. Installez les dépendances.

```shell
pip install -r requirements.txt
```

6. Installation des librairies vidéo

```shell
sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y
```

7. Démarrez le serveur.
```shell
python3 ./app.py
```

### Lancement automatique et passage en service

Création du service qui se lance automatiquement au démarrage du serveur.

1. Créez le fichier de service.
```bash
sudo nano /etc/systemd/system/srs.service
```

2. Copiez et collez le contenu suivant dans l'éditeur nano, remplacez les liens pour correspondre à ceux de votre arborescence :
    - ⚠️ Remplacez les `karelsvbd` par votre propre nom d'utilisateur ⚠️
```ini
[Unit]
Description=Exécuter mon script Python au démarrage
After=network.target

[Service]
User=karelsvbd
WorkingDirectory=/home/karelsvbd
ExecStart=/bin/bash -c 'source /home/karelsvbd/venv/bin/activate && python /home/karelsvbd/app.py'
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Sauvegardez et quittez l'éditeur (Ctrl+X, puis Y, puis Entrée).

4. Recharger les services systemd.
```bash
sudo systemctl daemon-reload
```

5. Activer et démarrer le service.
```bash
sudo systemctl enable srs.service
sudo systemctl start srs.service
```

6. Vérifiez l'état du service :
```bash
sudo systemctl status srs.service
```

## Serveur

### Informations sur le serveur de développement

```
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04 LTS
Release:	24.04
Codename:	noble
```

### Installation

Voici la procédure étape par étape afin de bien installer le projet sur votre serveur.

1. Clonez le projet sur le serveur  
```shell
git clone https://gitlab.ictge.ch/karel-svbd/srs.git
```

2. Naviguez jusqu'au projet des cameras.  
```shell
cd ./src/serveur/src/
```

3. Créez un environnement virtuel et activez le.  
```shell
python -m venv venv
source ./venv/bin/activate
```

3. Installez les dépendances.  
```shell
pip install -r requirements.txt
```

4. Installez Yolov5  
```shell
sudo apt update
sudo apt install python3 python3-pip git

git clone https://github.com/ultralytics/yolov5.git
cd yolov5

python3 -m venv yolov5_env
source yolov5_env/bin/activate

pip install -r requirements.txt

cd ..
```

5. Démarrez le serveur.  
```shell
python3 ./app.py
```

## Application

### Informations sur l'ordinateur de développement

```
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04 LTS
Release:	24.04
Codename:	noble
```

### Installation


1. Clonez le projet sur le serveur

```
git clone https://gitlab.ictge.ch/karel-svbd/srs.git
```

2. Naviguez jusqu'au projet des cameras.

```shell
cd ./src/serveur/src/
```

3. Créez un environnement virtuel et activez le.

```shell
python -m venv venv
source ./venv/bin/activate
```

3. Installez les dépendances.

```shell
pip install -r requirements.txt
```

4. Installez Yolov5  
```shell
sudo apt update
sudo apt install python3 python3-pip git

git clone https://github.com/ultralytics/yolov5.git
cd yolov5

python3 -m venv yolov5_env
source yolov5_env/bin/activate

pip install -r requirements.txt

cd ..
```

5. Démarrez l'application.
```shell
python3 ./main.py
```