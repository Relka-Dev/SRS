# Composant : Caméras WiFi

Le système vise à mettre en place des caméras WiFi compactes pour la surveillance ou pour d'autres applications nécessitant la capture et la diffusion en temps réel de flux vidéo. Le cœur du système, un Raspberry Pi Zero 2 W, exécute un serveur Python Flask.

## Informations sur l'ordinateur
```
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```

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

Voici la procédure étape par étape afin de bien installer le projet sur votre serveur.

1. Clonez le projet sur le serveur

```
git clone https://gitlab.ictge.ch/karel-svbd/srs.git
```

2. Naviguez jusqu'au projet des cameras.

```shell
cd ./src/cameras_wifi/src/
```

3. Créez un environnement virtuel et activez le.

```shell
python -m venv venv
source ./venv/bin/activate
```

3. Installez les dépendances.

*Note : si vous avez l'impression que certaines étapes prennent du temps c'est normal. Surtout les étapes `Building wheel`. Cela peut vous prendre facilement 2 heures. Si le problème perciste, utilisez les commandes `apt` afin d'installer les modules globalement un par un.*
```shell
pip install -r requirements.txt
```

4. Démarrez le serveur.
```shell
python3 ./app.py
```

## Authentification

### Connexion

Endpoint: `http://localhost:4298/login`

#### Description

Connectez-vous à l'API et générez un jeton. Passez les identifiants de connexion via l'authentification basique pour recevoir un jeton d'utilisation de l'API.

#### Requête

- Méthode: `GET`
- Authentification: Basique

#### Paramètres

- Nom d'utilisateur: `SRS-Server`
- Mot de passe: `QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT`

#### Réponse

- Statut: 200 OK
- Corps: JSON contenant un jeton JWT

#### Tests

##### Statut de réponse 200 OK
```js
pm.test("Statut de réponse 200 OK", function () {
    pm.response.to.have.status(200);
});
```

##### Contient un jeton JWT
```js
pm.test("La réponse contient un jeton JWT", function () {
    pm.response.to.have.jsonBody('token');
});
```

##### Erreur d'authentification - Identifiants incorrects
```js
pm.test("Erreur d'authentification - identifiants incorrects", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'John Doe',
            password: 'Ceci est un faux mdp'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Mot de passe manquant (Identifiants incorrects)
```js
pm.test("Erreur d'authentification - mot de passe manquant (identifiants incorrects)", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'John Doe',
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Mot de passe manquant (Identifiants corrects)
```js
pm.test("Erreur d'authentification - mot de passe manquant (identifiants corrects)", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'SRS-Server',
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Nom d'utilisateur manquant (Identifiants corrects)
```js
pm.test("Erreur d'authentification - username manquant (identifiants corrects)", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            password: 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Nom d'utilisateur manquant (Identifiants incorrects)
```js
pm.test("Erreur d'authentification - username manquant (identifiants incorrects)", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            password: 'Ceci est un faux mdp'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Nom d'utilisateur correct - Mot de passe erroné
```js
pm.test("Erreur d'authentification - username correct - mdp erroné", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'SRS-Server',
            password: 'Ceci est un faux mdp'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

##### Erreur d'authentification - Nom d'utilisateur erroné - Mot de passe correct
```js
pm.test("Erreur d'authentification - username erroné - mdp correct", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'Ceci est un faux username',
            password: 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(401);
    });
});
```

### Implémentation

#### Constantes de l'application
⚠️ Changer ces données si le serveur rentre en production ⚠️  
- *SECRET_KEY* : Sert à la génération et à la lecture des JWT.
- *CLIENT_USERNAME* : Nom d'utilisateur à donner lors de l'authentification.
- *CLIENT_PASSWORD* : Mot de passe à donner lors de l'authentification.
```py
app.config['SECRET_KEY'] = 'dMbgbnTDxK82SE3Bn2XgcMFTqmdLZWn9'
app.config['CLIENT_USERNAME'] = 'SRS-Server'
app.config['CLIENT_PASSWORD'] = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
```

#### Route

Afin d'accéder à la connexion, la route `/login` est appelée.  

1. Récupération des données d'authentification.
2. Vérification si auth est pas null.
3. Vérification que les données de connexion sont correctes.
4. Génération des réponses
    - Si correct : Génération d'un token d'une durée de vie de **24 heures** et retour du JSON.
    - Si erreur : Retour du JSON avec le code d'erreur adéquat.
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

## Détection de visages

### Détecter

Endpoint: `/detect`

#### Description

Détecte les visages dans le champ de vision de la caméra.

#### Requête

- Méthode: `POST`

#### Paramètres

- Image: Données de l'image du cadre capturé

#### Réponse

- Statut: 200 OK
- Corps: JSON contenant les données faciales détectées

#### Tests

##### Statut 200 OK : Assure que le statut de la réponse est 200.
```js
pm.test("Statut de réponse 200 OK", function () {
    pm.response.to.have.status(200);
});
```
##### Contient les données attendues : Vérifie que le corps de la réponse contient les données faciales attendues.

```js
pm.test("La réponse contient les données attendues", function () {
    var jsonData = pm.response.json();

    pm.expect(jsonData.nb_faces).to.be.above(-1);
    pm.expect(jsonData.nb_profiles).to.be.above(-1);
    pm.expect(jsonData.faces_data).to.be.an("array");
    pm.expect(jsonData.profiles_data).to.be.an("array");
});
```

##### Statut 403 KO : Token manquant
```js
pm.test("Erreur de Params - Token manquant", function () {
    pm.sendRequest({
        url: 'http://192.168.1.26:4298/detect',
        method: 'GET',
    }, function (err, res) {
        pm.expect(res).to.have.status(403);
    });
});
```

##### Statut 403 KO : Faux token
```js
pm.test("Erreur de Params - Faux token", function () {
    pm.sendRequest({
        url: 'http://192.168.1.26:4298/detect?token=ceciestuntokenincorrect',
        method: 'GET',
    }, function (err, res) {
        pm.expect(res).to.have.status(403);
    });
});
```

### Implémentation

#### Class Detection
Cette classe sert de librairie à la logique du traitement facial.

##### Detection des faces et des profils

Grâce à l'utilisation des algorithmes de **Haar**, cette fonction permet de détecter les **visages** et les **profils** dans une image.

1. Récupération des cascades (faces et profile)
2. Conversion des images en gris pour simplifier le traitement.
3. Récupération des faces et des profils dans l'image en niveau de gris.
4. Retourne la taille et la position des visage.

```py
@staticmethod
    def detect_faces_and_profiles(image):
        """
        Permet de détecter les faces et profiles

        Args:
            image: L'image à analyser pour détecter les profils et faces

        Returns:
            faces: Tableau contenant les coordonées et tailles des faces
            profiles: Tableau contenant les coordonées et tailles des profiles
        """
        face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
        profile_cascade = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        profiles = profile_cascade.detectMultiScale(gray, 1.1, 4)
        return faces, profiles
```

##### Récupération des encodages des visages
Grâce à la librairie **face_recognition**, on récupères les données faciales dans l'image.

1. Récupération de la position des visages.
2. Récupération des encodage dans l'image en fonction de l'emplacement des visages.
3. Retour des encodages.

```py
@staticmethod
    def get_face_encodings(image):
        """
        Récupère les données faciales de la personne dans l'image

        Args:
            image: L'image à analyser avec les faces

        Returns:
            face_encodings : Données des visages
        """
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        return face_encodings
```

#### Décorateur (Sécurité JWT)
Cette fonction permet d'en décorer une autre afin de la rendre accessible uniquement si un token JWT est présent dans la request.

1. Récupération du **token** dans les paramètres.
2. Vérification du JWT par l'utilisation de la clé secrète.

*Note: Quand la fonction jwt.decode() ne trouve pas de correspondance, elle crée une erreur*

```py
def token_required(f):
    """
    Fonction décoratrice permettant de forcer une autre fonction d'être identifié par JWT

    Args:
        f : Fonction à décorer
    
    Returns:
        f : Fonction décorée
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        # Try catch car jwt.decode retourne une erreur en cas de non correspondance
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
```


#### Route 

La route `/detect` permet d'accèder aux fonctions de détection.

1. Prise d'une photo en utilisant la camera du server présente à l'index **0**.
2. Libération de la mémoire.
3. Création de la queue asyncrone.
4. Création du process pour la création d'encodage asyncrone.
    - Target : La fonction de récupération des encodage asyncrone.
    - Args : Queue pour le stockage des encodage à la fin des traitements.
5. Démarrage de la procédure. 
6. Attente de la fin de la procédure.
7. Passage des données dans un tableau pour tous les visages et pour les profils.
8. Création du tableau final puis passage en JSON pour la réponse.

```py
@app.route('/detect', methods=['GET'])
@token_required
def detect():
    """
    Route permettant d'avoir les information sur les personnes présentes dans la vue de la camera

    Returns:
        Json: Résultat de l'interprétation de l'image
    """
    # CAP_V4L2 permet d'éviter une erreur
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    ret, frame = camera.read()
    camera.release()

    if ret:
        result_queue = Queue()
        process = Process(target=detect_worker, args=(frame, result_queue))
        process.start()
        process.join()

        faces, profiles, faces_encodings = result_queue.get()

    faces_data = []
    for ((x, y, w, h), encoding) in zip(faces, faces_encodings):
        face_data = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'encoding': encoding.tolist()
        }
        faces_data.append(face_data)
    
    profiles_data = []
    for (x, y, w, h) in profiles:
        profile_info = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        }
        profiles_data.append(profile_info)

    return jsonify({
        'nb_faces': len(faces),
        'faces_data': faces_data,
        'nb_profiles': len(profiles),
        'profiles_data': profiles_data
    })
```

#### Création des encogages (Fonctionnement asyncrone)
Cette fonction permet d'appeler les fonctions de la librairie détection de façon asyncrone.
1. Récupération des données des faces et visages grâce aux Algorithmes de Haar.
2. Récupération des encodages des visages.
3. Ajout des résultats dans la variable result_data.
4. Ajout des résultats dans la queue asyncrone.

```py
def detect_worker(image, result_queue):
    """
    Fonction asychrone
    Récupères les données dans l'image (Faces et profiles)

    Args:
        image: image à analyser
        result_queue (Queue): Queue des contenant les résultats des autres instances de la fonction
    """
    faces, profiles = Detection.detect_faces_and_profiles(image)
    faces_encodings = Detection.get_face_encodings(image)
    result_data = (faces, profiles, faces_encodings)
    result_queue.put(result_data)
```

## Collection (Postman)
Afin d'accèder à la collection ainsi qu'à plus de détails postman veuillez cliquer [ici](../../src/cameras_wifi/tests/SRS-cameras.postman_collection.json).



