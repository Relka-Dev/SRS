# Journal de bord - SRS

Bienvenue dans mon journal de bord, le compagnon essentiel de mon projet de diplôme. À travers ces pages, je partage mes réflexions quotidiennes, mes défis et mes progrès dans le développement de mon projet. Suivez mon parcours alors que je trace ma route vers la réussite, jour après jour.

## Structure
La structure des journées du journal de bords suit le schema suivant :  
- Résumé de la veille
- Déroulement des activités de la journée, questionnements etc.
- Résumé du travail de la journée
- Bilan personnel

## Prélude

### Architecture du projet

Avant de commencer le projet de diplôme je voulais mettre en place l'environnement de développement ainsi que l'architecture du projet.
Ayant trois composant à développer au cours de ce travail, je ne savais pas comment procéder au niveau du versionning et stockage du projet. J'avais deux options :

1. Créer un projet par composant.
2. Avoir un seul projet avec des sous répertoire pour les composants.

Afin de trancher j'ai envoyé un mail à Monsieur Zanardi, il m'a conseillé de faire un seul répertoire afin de simplifier la correction ainsi que l'architecture de mon travail.

Afin de partir sur de bonnes bases j'ai demandé à ChatGPT l'architecture adéquate pour mon projet. J'ai trouvé que la réponse qu'il m'a donné était parfaite, l'ajout des tests directement dans les répertoire des composant ajout à la lisibilité et la crédibilité du projet.

- [Prompt ChatGPT](https://chat.openai.com/share/bfaa8008-c450-467b-9824-221a9e0afc67)

## 27.03.2024

Aujourd'hui j'ai décidé de dédier ma journée à la plannification de mon projet et à mettre en place mon environnement de développement.

### MkDocs
J'ai voulu commencer par reprendre la documentation que j'avais commencé sur mkdocs chez moi. J'ai cependant rencontré une erreur que je n'arrivais pas à résoudre. 

#### Prompt
```sh
mkdocs serve
ERROR    -  Config value 'theme': Unrecognised theme name: 'material'. The available installed themes are: mkdocs, readthedocs
ERROR    -  Config value 'plugins': The "with-pdf" plugin is not installed
Aborted with 2 Configuration Errors!

```

En faisant un pip list j'ai bel et bien retrouvé les deux pachets. Il semblerait qu'il aie un problème avec ma commance **mkdocs serve**. J'ai décidé de poursuivre en markdown simple puis d'intégrer mkdocs pour les rendus.

#### Prompt
```sh
(env) svoboda@ubuntu-karelsvbd:~/gitlab/srs/docs/srs$ pip list
Package                    Version
-------------------------- -----------
[...]
mkdocs-material            9.5.15
mkdocs-material-extensions 1.3.1
mkdocs-with-pdf            0.9.3
[...]

```

### Plannification

Pour avoir une plannification précise et efficace j'ai décidé de me baser sur un système de jalons en utilisant les **diagrammes de Gantt**.

Afin d'optimiser mon temps j'ai demandé à un modèle d'IA entrainé dans les diagrammes de gantt. J'ai utilisé les test ainsi que les différentes fonctionnalités prévues dans mes composants comme prompt. L'IA m'a donné un résultat satisfaisant pour les tâche cependant, pour les jalons et tâche *maîte* elle n'a pas réussi à me donner un résultat convaincant.  
[Prompt Gantt Chart GPT](https://chat.openai.com/share/f782bdf4-607b-4a6e-885a-709bcd14bebd)

#### Résultat de l'IA
![Planning IA](./ressources/images/PlanningIA.png)

#### Ajustements personnels
J'ai ajouté les *super* tâches et les jalons. Chaque jalon correspont à une version du projet.
- v0.1 : Cameras Wifi  
- v0.2 : Serveur Central  
- v0.3 : Application multiplateforme  
- v1.0 : Projet Achevé et testé  

Pour chacun des jalon, je vais effectuer une release du gitlab.

#### Planning prévisionnel final
![Planning Prévisionnel](./ressources/images/PlanningPrevisionnel.png)

### Caméras wifi
Ayant terminé la plannification, je vais à présent me concacrer au travail avec mes cameras wifi. Je vais commencer par les démarrer et essayer d'y accèder par ssh.

Lors du POC du trimestre précédent j'ai développé un serveur de camera en python flask qui permettait de récupérer en temps réel le flux video de ces dernières. Je vais directement mettre la documentation dans le rapport. Le problème avec mon projet c'est l'optimisation. Il serait meilleur en théorie, de mettre le système de détection facile directement sur les camera wifi afin de simplifier le traitement sur le serveur.  
Je vais donc utiliser le temps supplémentaire que j'ai à disposition aujourd'hui pour essayer de faire fonctionner cette partie.  
J'ai commencé par faire un code simple de **détection faciale** sur le raspberry.
Ce code **fonctionne** mais me paraît un peu lent.
```py
import cv2

haarcascade_filepath = 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(haarcascade_filepath)
cap = cv2.VideoCapture(0)

ret, img = cap.read()

if ret:
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    print(f"{len(faces)} visage(s)")

    cap.release()
else:
    print("Erreur lors de la capture de l'image.")

```
Ensuite, j'ajoute la fonctionnalité de de récuération des données de la position des visages.

```py
app = Flask(__name__)

def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces


@app.route('/faces', methods=['GET'])
def get_faces():
    image_path = 'capture.jpg' 
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    cv2.imwrite(image_path, frame)
    camera.release()

    faces = detect_faces(image_path)

    data = []
    for (x, y, w, h) in faces:
        face_data = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        }
        data.append(face_data)

    return jsonify({
        'nb_faces': len(faces),
        'faces_data': data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```


À présent que vais rajouter la récupération des données des viages. Pour ce faire, je vais utiliser la librairie [face_recognition](https://pypi.org/project/face-recognition/) et récupérer les *face encoding*.

#### Problème lors de l'installation
J'ai eu un sourcis lors de l'instalation de la librairie. 
```sh
Collecting face-recognition-models>=0.3.0
  Downloading https://www.piwheels.org/simple/face-recognition-models/face_recognition_models-0.3.0-py2.py3-none-any.whl (100.6 MB)
     |████████████████████████████████| 100.6 MB 446 kB/s eta 0:00:01Killed
```
Après avoir consulté la seconde résponse de [cette question](https://stackoverflow.com/questions/30550235/pip-install-killed). J'ai augmenté le swap size. Cela a fonctionné.

#### Implémentation des encodings

J'ai commencé par implémenter mon code que j'ai effectué lors du POC qui me donnes les données d'une image en utilisant la librairie **face_recognition**.

```py
def get_face_encodings(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings
```

Ensuite, j'ajoute les données à la liste pour le retour en JSON

```py
faces, image = detect_faces(image_path)
    face_encodings = get_face_encodings(image)

    data = []
    for ((x, y, w, h), encoding) in zip(faces, face_encodings):
        face_data = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'encoding': encoding.tolist()
        }
        data.append(face_data)
```

#### Définition d'un port spécifique

Afin de simplifier le scan du serveur quand il sera à la recherche de camera, il me faut un numéro de port qui est unique à mon projet. J'ai choisi le nombre **4298** de façon aléatoire. Après vérification sur le site [speedguide.net](https://www.speedguide.net/port.php?port=4298) ce port est prit par d'autres application mais cela n'est pas si important dans le cadre de mon projet de diplôme car le projet ne rentrera pas en production.

#### Sécurisation API

Afin de sécuriser les cameras j'ai décidé d'effectuer un JWT (json web token). Le seul problème c'est que je ne sais pas comment faire. Par conséquent, je vais regarder un [tutoriel youtube](https://www.youtube.com/watch?v=J5bIPtEbS0Q) et adapter mon travail pour mon projet.

##### Code crée grâce à la vidéo

```py

from flask import Flask, jsonify, request, make_response
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'
 
@app.route('/unprotected')
def unprotected():
    return ''

@app.route('/protected')
def protected():
    return ''

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Problème avec JWT

J'avais cette erreur :
```sh
token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
AttributeError: module 'jwt' has no attribute 'encode'
```
Le problème vennait de la libraire JWT qui était en confit avec PyJWT.

Grace à cette question sur [Stack Overflow](https://stackoverflow.com/questions/33198428/jwt-module-object-has-no-attribute-encode). J'ai pu résoudre le problème.

## Conclusion
Aujourd'hui je pense avoir bien avancé, pour un jour prévu initialement à la plannification j'ai quand même bien pu travailler avec mes cameras. Demain, je compte continuer sur cette lancée en implémentant mon système de sécurité puis les tests postman.

## 28.03.2024

#### Bilan de la veille
Hier je me suis concentré sur d'abord la **plannification** puis sur le développment du **serveur flask** pour les **cameras wifi**. Je me suis arrêté lors de la mise en place de la sécrurité avec les **JWT**.  

#### Plannification du jour
Chez moi je me suis rendu compte que pour que mon système soit fonctionnel, je dois absolument pouvoir détecter des **profils** et des **arrières de têtes** en plus des faces afin de pouvoir trouver dans l'espace où se situe la personne. Je vais commencer par ajouter cette fonctionnalité puis je vais continuer mon travail sur les **JWT**.

### Detection de profils
J'ai commencé par ajouter la Haar cascade des profils :
```py
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
```
Puis la détection :
```py
profiles = profile_cascade.detectMultiScale(gray, 1.1, 4)
```

Une fois cela fait je détecte la position et la taille du profil :
```py
profiles_data = []
    for (x, y, w, h) in profiles:
        profile_info = {
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h)
        }
        profiles_data.append(profile_info)
```

Et j'ajoute ces données dans la réponse json.

```py
return jsonify({
        'nb_faces': len(faces),
        'faces_data': faces_data,
        'nb_profiles': len(profiles),
        'profiles_data': profiles_data
    })
```

### Détection des arrières de tête
Après avoir fait des recherches, je n'ai pas trouvé de cascade pour des arrière de crâne. J'ai donc demandé à ChatGPT. Il m'a confirmé qu'il était **complexe** de faire de la reconnaissance d'arrière de crâne. Cela est dût au **manque de caractèristiques propres**. Mais c'était possible en entrainnant directement un modèle comme le **CNN**. Cependant, je préfère uniquement utiliser les **algorithmes de Haar** pour l'instant pour des question **d'optimisation de temps**.  
[Prompt ChatGPT](https://chat.openai.com/share/d28196ba-28f8-40c1-931e-4defa925785b)

### Suite du travail sur les JWT
J'ai continué à suivre le [tutoriel youtube](https://www.youtube.com/watch?v=J5bIPtEbS0Q). Grâce à ce dernier, je suis à présent capable de sécuriser les routes par système de wrap de fonctions.  
Fonction qui permet de vérifier les tokens :

```py
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        
        return f(*args, **kwargs)
        
    return decorated
```

Il suffit ensuite que je décore les fonctions qui se doivent d'être protégées.
```py
# Route en accès libre
@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can see this'})

# Route protégée par le token
@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Only available for valid tokens'})

```

Je vais à présent implémenter ce système dans mon API.

#### Implémentation dans l'API
Je commence par défir les constantes de l'application.  
⚠️ Je me permet de les mettre dans mon journal de bord mais il est impératif que dans un projet qui pourrait rentrer en production il ne faut pas le faire.

```py
# Définition de la clé secrète qui sert au chiffrement
app.config['SECRET_KEY'] = 'dMbgbnTDxK82SE3Bn2XgcMFTqmdLZWn9'
# Identifiants de connexion du serveur central
app.config['CLIENT_USERNAME'] = 'SRS-Server'
app.config['CLIENT_PASSWORD'] = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
```

La suite de l'implémentation était simple, il suffisait d'ajouter la fonction de login et à décorer la fonction detect pour la sécuriser.

#### Optimisation du code
Je me suis rendu compte que le code était lent. Il lui prend environ 3 secondes pour faire l'analyse.  
Premièrement j'ai supprimé la creation d'image intermédaire et passe directement la frame.

```py
# Code précédent
image_path = 'capture.jpg' 
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
cv2.imwrite(image_path, frame)
camera.release()

# Code optimisé
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
camera.release()
```