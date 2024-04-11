# Composant : Caméras WiFi

## Introduction
Le système vise à mettre en place des caméras WiFi compactes pour la surveillance ou pour d'autres applications nécessitant la capture et la diffusion en temps réel de flux vidéo. Le cœur du système, un Raspberry Pi Zero 2 W, exécute un serveur Python Flask.

## Hardware
Le matériel a été choisi spécifiquement pour qu'il soit en adéquation avec les besoins du projet. Les composants sont volontairement simples d'utilisation afin de minimiser le temps passé sur l'éléctronique.

| Composant                                    | Fonction                    | Prix     | Fournisseur                                            |
|----------------------------------------------|-----------------------------|----------|--------------------------------------------------------|
| Raspberry Pi Zero 2 W                        | Serveur (Python Flask)      | 29.10 CHF | [Digitec](https://www.digitec.ch/fr/s1/product/raspberry-pi-zero-2-w-carte-de-developpement-kit-17346864) |
| Raspberry Pi Camera Module 3 Wide Angle 120° | Module de Caméra            | 45.50 CHF | [Digitec](https://www.digitec.ch/fr/s1/product/raspberry-pi-camera-module-3-wide-angle-120-camera-module-electronique-24041966?ip=raspberry+camera) |
| MediaRange Power Bank 2600 mAh               | Batterie externe            | 13.95 CHF | [Fnac](https://www.fnac.com/mp28798913/MediaRange-Power-Bank-Banque-d-alimentation-2600-mAh-1-A-USB-sur-le-cable-Micro-USB-gris-blanc/w-4) |
| SanDisk ExtremePro microSD A1                | Carte mémoire               | 13.00 CHF | [Digitec](https://www.digitec.ch/fr/s1/product/sandisk-extremepro-microsd-a1-microsdhc-32-go-u3-uhs-i-carte-memoire-6613018) |

**Coût total:** 101.55 CHF

## Dépendances externes

| Nom              | Description                                 | Utilisation | pypi.org          |
|------------------|---------------------------------------------|-------------------|----------------|
| Flask            | Framework Web pour Python                   | Serveur mettant à disposition le Web-Service | [Flask](https://pypi.org/project/Flask/)            |
| JWT              | Implémentation de JSON Web Tokens           | Gestion de la sécurité par génération de clé | [JWT](https://pypi.org/project/PyJWT/)              |
| OpenCV (cv2)     | Bibliothèque de vision par ordinateur       | Capture des frames des cameras | [OpenCV](https://pypi.org/project/opencv-python/)   |
| Face Recognition| Bibliothèque de reconnaissance faciale     | Génération des points du visage quand une personne est détectée | [Face Recognition](https://pypi.org/project/face-recognition/) |

## Installation

| Système | Version

## Sécurité (JWT)

Le serveur gère l'authentification par la création de JWT (JSON web token).

### 1. Connexion
Pour effectuer une première connexion, il faut commencer par appeler le endpoint **/login**. 

```py
@app.route('/login')
def login():
    """
    Route permettant à se connecter

    Returns:
        str: JWT généré
    """
    auth = request.authorization

    if auth and auth.password == app.config['CLIENT_PASSWORD'] and auth.username == app.config['CLIENT_USERNAME']:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
```