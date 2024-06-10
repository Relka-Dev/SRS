# Installation de la documentation

Suivez les étapes suivantes pour démarrer le serveur `mkdocs` de documentation.

## Créez l'environnement virtuel

```sh
python -m venv env
```

### Activez l'environnement virtuel

**Windows**

```sh
.\env\Scripts\activate
```
**macOS/Linux**

```sh
source env/bin/activate
```
## Installez les dépendances

```sh
pip install -r requirements.txt
```

## Démarrer le serveur

### Avec la génération PDF

**Windows**

```sh
set ENABLE_PDF_EXPORT=1
```
**macOS/Linux**

```sh
export ENABLE_PDF_EXPORT=1
```

### Construction du server

```sh
mkdocs build
```

### Démarrage

```sh
mkdocs serve
```