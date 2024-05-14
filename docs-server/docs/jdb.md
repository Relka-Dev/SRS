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

Aujourd'hui j'ai décidé de dédier ma journée à la planification de mon projet et à mettre en place mon environnement de développement.

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

### planification

Pour avoir une planification précise et efficace j'ai décidé de me baser sur un système de jalons en utilisant les **diagrammes de Gantt**.

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
Ayant terminé la planification, je vais à présent me concacrer au travail avec mes cameras wifi. Je vais commencer par les démarrer et essayer d'y accèder par ssh.

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

### Conclusion
Aujourd'hui je pense avoir bien avancé, pour un jour prévu initialement à la planification j'ai quand même bien pu travailler avec mes cameras. Demain, je compte continuer sur cette lancée en implémentant mon système de sécurité puis les tests postman.

## 28.03.2024

#### Bilan de la veille
Hier je me suis concentré sur d'abord la **planification** puis sur le développment du **serveur flask** pour les **cameras wifi**. Je me suis arrêté lors de la mise en place de la sécrurité avec les **JWT**.  

#### Planification du jour
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

### Optimisation du code
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

#### Multiprocessing
Ensuite j'ai trouvé interessant d'optimiser la génération des encoding dans le cas où il y a plusieurs visages. Pour ce faire, je vais profiter de l'architecure du raspberry pico et faire du multiprocessing.  
C'est abosulment crutial pour le traitement de plusieurs visages en même temps.  
J'avais déjà de l'expérience avec du **multithreading** mais pas spécialement en **multiprocessing** en python. Par conséquent j'ai suivi la [documentation officielle](https://docs.python.org/3/library/multiprocessing.html).  
J'ai commencé par la création de la **queue** qui me permettra de **récupérer les valeurs de mes process**. Je crée ensuite le **process** avec comme **argument mon worker** et comme **arguments du worker** j'ai passé la **frame donc l'image et la référence de la queue**. Ensuite je **démarre le processus** et récupère les **résultats du worker**.

```py
if ret:
        result_queue = Queue()
        process = Process(target=detect_worker, args=(frame, result_queue))
        process.start()
        process.join()

        faces, profiles, faces_encodings = result_queue.get()
```


J'ai ensuite crée le worker qui est la fonction qui sera exécutée en **parallèle**. La fonction reprend la **détection faciale** et la **génération des encodings**. Les résultats sont ensuite **ajoutée** dans la **queue du process princial**.
```py
def detect_worker(image, result_queue):
    faces, profiles, _ = detect_faces_and_profiles(image)
    faces_encodings = get_face_encodings(image)

    result_data = (faces, profiles, faces_encodings)
    result_queue.put(result_data)
```

### Tests Postman

Postman me permet d'avoir un client pour mon API. Les tests se lancent de façon automatique lors des requêtes.

#### Endpoint /login
Pour tester le endpoint **/login** je mets les identifiants de connexion dans la case **Authorization** :

![Login Test](./ressources/images/capturepostmantestlogin.png)

Ensuite j'écris les tests :

```js
pm.test("Statut de réponse 200 OK", function () {
    pm.response.to.have.status(200);
});

pm.test("La réponse contient un jeton JWT", function () {
    pm.response.to.have.jsonBody('token');
});
```

#### Endpoint /detect

Le problème avec ce endpoint c'est qu'il me faut impérativement le JWT qui m'est fournit lors de l'appel du login. Les tests sont par conséquent dépendants de la validité du token.

```js
pm.test("Statut de réponse 200 OK", function () {
    pm.response.to.have.status(200);
});

pm.test("La réponse contient les données attendues", function () {
    var jsonData = pm.response.json();

    pm.expect(jsonData.nb_faces).to.be.above(-1);
    pm.expect(jsonData.nb_profiles).to.be.above(-1);
    pm.expect(jsonData.faces_data).to.be.an("array");
    pm.expect(jsonData.profiles_data).to.be.an("array");
});

```

#### Problème avec les tests
J'ai pas réussi à faire les tests que je voulais. Pour le login, j'aimerais avoir un login fonctionnel et un autre sans identifiants etc. J'aimerais tester chaque cas pour éviter les failles sauf que j'y arrive pas avec les exemples de postman, selon moi il faudrait créer une requête pour chaque cas mais j'ai demandé confirmation à mes suiveurs par mail.  
**Question :**
![Question mail](./ressources/images/questionMail1.png)
**Réponse :**
![Réponse mail](./ressources/images/questionMail2.png)
##### Solution
Je vais essayer de mettre les varialbes d'authentification dans la séquence de test, je ne sais pas le faire cependant.  
J'ai pas trouvé en cherchant dans la [documentation officielle](https://learning.postman.com/docs/sending-requests/authorization/specifying-authorization-details/) j'ai du demander à chatGPT et en effet on peut faire des requêtes personnalisés dans les tests, cela va également m'aider lors du moment où je vais développer mon propre client pour mon API.  
[Prompt ChatGPT](https://chat.openai.com/share/82b7a446-9f7f-4dfe-9310-22668b566353)  
De plus, à présent que je sais que l'on peut faire des requête depuis les tests, je peux essayer de récupérer dynamiquement le token lors du test du endpoint **/detect**.  

J'ai fais un tests pour les scenarios suivants (code attentu : 401) :
1. identifiants incorrects
2. mot de passe manquant (identifiants incorrects)
2. mot de passe manquant (identifiants corrects)
3. username manquant (identifiants incorrects)
3. username manquant (identifiants corrects)
4. username correct - mdp erroné
5. username erroné - mdp correct

Je ne pense pas qu'il y aie plus d'erreurs possibles de la part de l'utilisateur. Les tests fonctionnent.

### Conclusion
J'ai bien pu travailler aujourd'hui j'ai pu mettre en application des concepts interessants comme les tests postman et le multiprocessing pour la première fois. La prochaine fois je vais me concentrer sur la documentation de l'api.

## 15.04.2024

Pour commencer après les vacances j'ai décidé de commencé par consulter mon planning.  
Selon ce dernier, j'était sensé rendre la version 0.1 de mon projet la semaine dernière. Malheureusement, étant particulièrement occupé lors de ces vacances je n'ai pas pu travailler assez efficacement pour atteindre cet objectif. Par conséquent, l'objectif principal du jour sera en premier lieu, terminer les tests postman puis, faire la documentation de l'API afin d'effectuer une release de la verion 0.1.   
*Note: Je préfère continuer selon mon planning malgrès le fait que les vacances n'y soit pas prises en compte car j'estime que mon travail sur les cameras est déjà suffisament avancé pour me le permettre.*

#### Planning prévisionnel final
![Planning Prévisionnel](./ressources/images/PlanningPrevisionnel.png)

### Erreur avec les tests postman

La dernière fois que j'ai travaillé sur le projet j'avais presque terminé les tests postman à un détail pret. Le test ci-dessous n'était pas fonctionnel. 

```js
pm.test("Réponse correcte - ", function () {
    pm.sendRequest({
        url: 'http://localhost:4298/login',
        method: 'GET',
        auth: {
            type: 'basic',
            username: 'SRS-Server',
            password: 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
        }
    }, function (err, res) {
        pm.expect(res).to.have.status(200);
    });
});
```

L'erreur en question :

![Erreur test postman](./ressources/images/testpostmanfail.png)

En effet je n'arrive pas à faire la connexion de façon dynamique. Cependant, vu l'impact faible sur la documentation du projet j'ai décidé de ne pas plus m'attarder dessus.

### Génération de la documentation postman

Ayant déjà effectué une partie de ma documenation sur postman, j'ai essayé de générer une documentation à partir de ce dernier. Le problème c'est le manque d'outil, j'ai essayé avec [ce projet](https://github.com/karthiks3000/postman-doc-gen?tab=readme-ov-file) ayant été développé par un indépendant. Le soucis c'est qu'il n'affiche pas les test et n'affiche pas correctement le markdown. J'ai donc décidé de demander à chat gpt de me générer la documentation depuis le json. Cela me permet de m'épargner une tâche chronophage car la documentation je l'ai déjà écrite, il s'agit uniquement d'un changement de format.  

[Prompt ChatGPT](https://chat.openai.com/share/1e9e9b94-864e-4d10-aafc-5770a059fe24)

![documentation générée](./ressources/images/docgenereepostman.png)

Cependant, ce projet m'a permis d'apprendre une chose qui aiderait à la mise en place de mon projet. En effet en lisant l'instlation j'ai vu cette ligne.

![installtion de dépendances](./ressources/images/installtaiondedépendances.png)

Cela peut paraître basique mais je vais pouvoir m'en servir pour simplifier la mise en place des mes serveurs. Pour la génération automatique, j'utilise la commande *pipreqs*. J'ai trouvé cette commande grâce à [cette quesiton](https://stackoverflow.com/questions/31684375/automatically-create-file-requirements-txt) sur stack overflow.

La commande m'a généré le code suivant :

```
face_recognition==1.3.0
Flask==3.0.3
PyJWT==2.8.0
PyJWT==2.8.0
```

Ce qui est faux, premièrement il manque openCV et PyJWT est présent deux fois. Je sens que le problème vient du fait que je n'utilise pas un environnement virtuel. En effet, j'ai eu quelques problèmes lors de la configuration de ce dernier. Je vais essayer de le mettre en place une nouvelle fois et pendant l'installation des dépendance je vais travailler sur la documentation.  

Mise à part ce problème de dépendance, j'ai terminé la documentation ainsi que le code. J'ai envoyé un mail à$ mes accompaganteurs afin de me faire un retour. À présent, je vais commencer le développement de mon serveur central.

### Début du travail sur le serveur central

Pour commencer, je dois effectuer une recherche automatique pour trouver les adresses ip avec mon port ouvert. Pour ce faire, je vais utiliser le code que j'ai eu l'occasion  de réaliser lors de mon POC.

Voici le code en question. Après execution, je me suis rendu compte qu'il n'était pas asyncrone :

```py
class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.IPv4Network(network)

    def scan_worker(self, port, result_queue,  timeout=0.01):
        for ip in self.network.hosts():
            print(str(ip))
            if self.check_port(ip, port, timeout):
                result_queue.put(ip)


    def scan_port(self, port, timeout=1, max_threads=100):
        """
        Scan tous les adresses du réseau.

        Args:
            port (int): Port à scanner
            timeout (float): Le temps maximum en secondes à attendre pour une réponse.
            max_threads (int): Nombre maximum d'excutions sur les ip en même temps.

        Returns:
            Liste Ports (Array): Retrourne le tableau des adresses ip avec le port ouvert
            
        """
        open_ips = []
        print("Recherche en cours!")

        result_queue = Queue()
        process = Process(target=self.scan_worker, args=(port, result_queue))
        process.start()
        process.join()

        return result_queue.get()

    def check_port(self, ip, port, timeout):
        """
        Vérifie si un port spécifié sur une adresse IP donnée est ouvert.

        Args:
            ip (str): L'adresse IP à tester.
            port (int): Le numéro de port à vérifier.
            timeout (float): Le temps maximum en secondes à attendre pour une réponse.

        Returns:
            bool: Renvoie True si le port est ouvert, sinon False.
        """
        try:
            # Vérification de l'ouverture du port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((str(ip), port))
                return True
        except (socket.timeout, socket.error):
            return False
```

Pour remédier à cela je me suis rendu sur la [page de la documentation officielle](https://docs.python.org/3/library/multiprocessing.html) pour essayer de trouver une alternative.
Malheureusement, je ne pense pas encore avoir le niveau en python pour gérer ce genre de problème. Cependant j'ai trouvé une autre solution. J'ai simplement réduit le timeout. Après plusieurs test, je n'ai pas constaté d'erreur. J'ai donc simplifié le code.

```py
class NetworkScanner:
    def __init__(self, network):
        self.network = ipaddress.IPv4Network(network)

    def scan_ips(self, port,  timeout=0.01):
        ip_with_port_open = []
        for ip in self.network.hosts():
            print(str(ip))
            if self.check_port(ip, port, timeout):
                ip_with_port_open.append(ip)

        return ip_with_port_open

    def check_port(self, ip, port, timeout):
        """
        Vérifie si un port spécifié sur une adresse IP donnée est ouvert.

        Args:
            ip (str): L'adresse IP à tester.
            port (int): Le numéro de port à vérifier.
            timeout (float): Le temps maximum en secondes à attendre pour une réponse.

        Returns:
            bool: Renvoie True si le port est ouvert, sinon False.
        """
        try:
            # Vérification de l'ouverture du port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((str(ip), port))
                return True
        except (socket.timeout, socket.error):
            return False

```
#### Application multiplateforme après ou pendant le développement du serveur central ?

En réféchissant quoi faire ensuite, je me suis posé la question s'il ne serait pas meilleur de développer l'application multiplateforme en même temps que le serveur central. Cela me permettrait d'avoir un client et avancer plus vite. De plus, quand j'ai développé des API par le passé, j'ai constaté que quand je développait mon client, il me manquait souvent des fonctionnalités et des endpoint notamment quand je faisait des crud. Pour l'instant je vais me concentrer sur le serveur mais je vais poser la question à mes suiveurs dès que possible.

#### Architecture du serveur central

Pour le développement de mon serveur central il faut que je réfléchisse comment il va fonctionner ainsi que son intéraction avec l'utilisateur. Je sais qu'en premier lieu, je dois faire un système de connexion qui pour les utilisateurs. Je pense qu'il serait interessant de commencer par une connexion par défault avec un nom d'utilisateur basique comme *admin* et un mot de passe comme *mdp*. Une fois l'utilisateur connecté, il ne peut rien faire sauf ajouter un nouvel utilisateur et un mot de passe qui eux seront sécurisé et permettront de communiquer avec ce système. 

##### Première connexion

L'utilisateur rentre ses identifiants dans la page de login, si les identifiants sont corrects, un jwt de 15 min est crée et passé à l'application.  
![première connexion](./ressources/images/premiereconnexion.png)

##### Ajout des identifiants
Une fois l'application en possession du JWT. L'utilisateur se trouve devant la page permettant d'ajouter des utilisateurs. On fois les nouveaux identifiants administrateurs entrés. Les identifiants chiffrés ainsi que le JWT sont passés dans la requête vers le serveur. Après vérification de la conformité des données, les identifiants de connexion sont ajoutés dans la BDD. Si tout s'est bien passé, l'utilisateur reçoit un message sur l'application et est redirigé vers la page de connexion.

![ajout d'utilisateur](./ressources/images/ajoututilisateur.png)

##### Seconde connexion
Cette fois-ci, l'utilisateur doit se connecter avec les identifiants sécurisés. Une fois qu'il a rentré ces derniers, les données sont chiffrés et envoyés vers le serveur. Le serveur fait ensuite une vérification au-prêt de la base de données. Si les identifiants sont corrects, le serveur crée un JWT temporaire de 24 heures permettant de se connecter aux autres fonctionnalités. Du côté de l'utilisateur, il est redirigé vers la page d'acceuil de l'application.

![seconde connexion](./ressources/images/secondeconnexion.png)

#### Gestion de la première connexion

Afin de créer cet endpoint, il faut en premier lieu que je sache s'il s'agit bel et bien de la première connexion. Pour ce faire, j'ai décidé de vérifier si la base de données est bel et bien vide. J'ai donc crée une classe `DatabaseClient` qui me servira de client de base de données.

```py
class DatabaseClient:
    pass
```

Je crée une première route `initalize` qui servira à la première connexion.

```py
def initialize(self):
        self.db_client = DatabaseClient(self.DB_HOST, self.DB_NAME, self.DB_USER, self.DB_PASSWORD)

        self.app.add_url_rule('/initialize', 'initialize', self.intialize, methods=['GET'])

    def initialize(self):
        if self.db_client.isAdminTableEmpty():
            pass
        else:
            return jsonify({'erreur': 'Impossible d\'ajouter l\'admin quand un autre est déjà présent.'}), 402
```

Et je vérifie que la table est vide.

```py
def isAdminTableEmpty(self):
        self.cursor.execute("SELECT * FROM Admin")
        results = self.cursor.fetchall()
    
        if len(results) == 0:
            return True
        else:
            return False
```

J'ai ensuite créer une classe jwt_library qui me servira de bibliothèque pour les fonctionnalités liés aux JWT.

```py
class JwtLibrary:
    @staticmethod
    def GenerateJwtForInitialization(username):
        SECRET_KEY = 'S[26dF9RmVM/#{GT'
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, SECRET_KEY)

        return token
```

Et pour terminer, j'implémente cette fonction dans ma route.

```py
def initialize(self):
        auth = request.authorization
        if auth and auth.password == self.DEFAULT_PASSWORD and auth.username == self.DEFAULT_USERNAME:
            if self.db_client.isAdminTableEmpty():
                return jsonify({'message': JwtLibrary.GenerateJwtForInitialization(auth.username)}), 200
            else:
                return jsonify({'erreur': 'Impossible d\'ajouter l\'admin quand un autre est déjà présent.'}), 402
        else:
            return jsonify({'erreur': 'Identifiants de connexion manquants ou erronés'}), 403
```

Il ne me reste plus qu'à tester avec postman.

![Test initialize postman](./ressources/images/testinitiallizepostman.png)

Avec cela, j'ai terminé la génération des JWT de 15 min pour les initializations.

### Conclusion
Je pense avoir bien avancé aujourd'hui, non seulement j'ai terminé les serveur des cameras wifi mais j'ai également débuté le travail sur le serveur central. Demain je vais me concentrer sur la doc des partie que j'ai développé puis je vais continuer le développement du serveur central en commançant par le endpoint login.

## 16.04.2024
Pour débuter la journée je vais commencer par documenter la création des token JWT pour l'initialization du serveur. Ensuite, je vais continuer à travailler sur la procédure d'ajout du premier utilisateur.

Après réflexion, je vais uniquement débuter la structure de ma documentation car je préfère mettre en place le système d'initialisation au complet et m'assurer que ce dernier fonctionne avant de me lancer dans la doc.

#### Suite de l'initialisation
À présent, il me faut implémenter la seconde partie, l'ajout d'intifiants. Après réflexion, je ne peux pas faire en sorte que le serveur force des critères de mot de passe car cela voudrait dire que ces derniers passerait en clair depuis le client. Je vais donc implémenter cette partie dans l'application direcement. 

Je commance par implémenter la route qui permettra d'ajouter le premier admin. Je l'ai appleé `/first_admin` et mit en méthode POST.
![ajout d'utilisateur](./ressources/images/ajoututilisateur.png)

Pour la gestion et la vérification du token JWT, j'utilise encore une fois la fonction décoratrice et l'ajoute dans ma classe jwt_library.

##### Vérification du mot de passe
Comme précisé avant, je ne peux pas vérifier la force des mots de passes (nombre de charatères, diversité etc.) cependant, je me demande s'il y a pas une façon de vérifier si un string, le mot de passe, est crypté ou non. J'ai trouvé une question correspondante sur Stack Overflow. Je vais essayer d'implémenter le code fournit.

[Question Stack Overflow](https://stackoverflow.com/questions/7000885/python-is-there-a-good-way-to-check-if-text-is-encrypted)

Après avoir effectuer plusieurs tests sur Postman avec des methodes de chiffrement différentes, je n'ai pas réussi à faire fonctionner la fonction. Par conséquent, je décide de ne pas l'implémenter.

##### Implémetantion du second token JWT
Je commance par créer une autre clé secrète pour ajouter de la sécurité ainsi qu'une seconde fonction de génération et un décorateur. Je donne une expiration de 24 heures au token.

```py
__SECRET_KEY_FOR_API = 'qEcYfxQzC3bS'

@staticmethod
    def generateJwtForAPI(username):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JwtLibrary.__SECRET_KEY_FOR_API)

        return token

def API_token_required(f):
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
                data = jwt.decode(token, JwtLibrary.__SECRET_KEY_FOR_INITIALIZATION, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 403
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 403
            return f(*args, **kwargs)

        return decorated
        
```

Les nouvelles fonctionnalités ajoutée, je peux à présent implémenter la connexion.

### Connexion administrateur

Pour la connexion de l'administrateur je crée la route `admin_login`. Si l'utilisateur transmet le bon mot de passe et le bon nom d'utilisateur, un JWT est créé.

```py
def admin_login(self):
        if not self.db_client.isAdminTableEmpty():
            username = request.args.get('username')
            password = request.args.get('password')
            
            if not username or not password:
                return jsonify({'erreur': 'Mauvais paramètres, utilisez (username, password) pour le nom d\'utilisateur et le mot de passe respectivement.'}), 400
            
            if self.db_client.adminLogin(username, password):
                return jsonify({'token': JwtLibrary.generateJwtForAPI(username)}), 200
            else:
                return jsonify({'erreur': 'Les identifiants de connexion sont erronés'}), 400
        else:
            return jsonify({'erreur': 'Aucun administrateur n\'est présent dans le système.'}), 403
```
![JWT admin](./ressources/images/jwtadmin.png)

À présent que j'ai terminer l'initialisation, je vais la documenter.

### Recherche automatique des cameras
Ayant terminé l'initialisation, je peux me concentrer sur la recherche automatique des cameras ainsi que l'appel automatique de leurs endpoint. Il me faut trouver une façon pour stocker les adresses ip quand le serveur trouve les cameras. Je pensais de stocker les réseaux dans une table dédiées avec un *timestamp* indiquant le dernier scan effectué ainsi que les cameras reliés dans une autre table. Chaque fois que le endpoint est appelé. une vérification au niveau du timestamp est effectuée et si ce timestamp est dépassé de disons... 10 minutes, une nouvelle recherche est effectuée permettant de mettre de à jour la bade de données des cameras. La même chose se produit s'il y a une erreur de communication avec une des cameras. Pour résumer donc :

À chaque appel, l'utilisateur envoie son réseau.

#### Si la base de données est vide (Pas de correspondance au niveau du network)

1. Recherche dans la table network une correspondance.
2. Recherche des cameras sur le réseau.
3. Ajout des ip des cameras dans la base de données.
4. Appel des endpoint des camera.
5. Interprétation des données.   

*Note : Si aucune camera n'est trouvée alors l'opération est intérompue et l'API retourne le message correspondant.*  

![Scan réseau sans correspondance](./ressources/images/scanreseausanscorrespondance.png)


##### Implémentation
Je commence par créer une nouvelle classe `camera_server_client.py` qui me servira à intéragir avec les apis des cameras. Je crée ensuite les constantes avec les identifiants de connexion ainsi que le port.

```py
class CameraServerClient():
    __CLIENT_USERNAME = 'SRS-Server'
    __CLIENT_PASSWORD = 'QNaAXEjuNBqdhF6HFjggsDmhLZVeWSzT'
    __CAMERAS_SERVER_PORT = 4298
```

J'ajoute une fonction qui me permet de scanner les cameras sur le réseau.

```py
def lookForCameras(self):
        self.camerasIPs = self.networkScanner.scan_ips(self.__CAMERAS_SERVER_PORT)
        return self.camerasIPs
```

Ensuite, une fonction me permettant d'appeler automatiquement les endpoint permettant d'obtenir les Tokens de toutes les cameras.

```py
def getCamerasTokens(self):
        if len(self.camerasIPs) == 0:
            return None

        tokens = []
        for cameraip in self.camerasIPs:
            camera_url = "http://{ip}:{port}".format(ip = cameraip, port = self.__CAMERAS_SERVER_PORT)
            print(camera_url)
            auth = (self.__CLIENT_USERNAME, self.__CLIENT_PASSWORD)
            response = requests.get(f"{camera_url}/login", auth=auth)

            if response.status_code == 200:
                tokens.append(response.json().get('token'))
            else:
                print("Échec de l'obtention du token JWT pour l'ip : {ip}:".format(ip=cameraip), response.status_code)
            
        return tokens
```

### Maj de la base de données

J'ai bien avancé sur la logique de mon application cependant, afin de pouvoir continuer je dois réfléchir sur la structure de la ma base de données afin en premier lieu, l'adapter à l'utilisation des JWT des camera en ajoutant un champs à leur table.

#### Ajustement de la position des cameras par l'utilisateur
Afin de pouvoir effectuer les calcul de la position des utilisateurs je dois connaitre la position des cameras. Pour ce faire, je dois ajouter les champs **position** qui indiquera la position relative par rapport au mur et **orientation** qui déterminera l'orientation de la camera. Cependant, je veux faire en sorte que les camera puisse se situer dans le réeau sans forcément avoir de position indiquées afin de laisser la possibiliter à l'utilisateur de les ajuster.

#### Ajout de réseau
J'ai crée le endpoint `/add_network` permettant d'ajouter un réseau à la base de données. J'ai fais en sorte d'éviter les erreurs et les duplications.

##### Route
```py
@JwtLibrary.API_token_required
    def add_network(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400
        
        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
            return jsonify({'erreur': 'Le réseau fournit n\'est pas valide ou n\'est pas accessible'}), 400
        
        if not self.db_client.addNetwork(ip, subnetMask):
            return jsonify({'erreur': 'Le réseau fournit est est déjà dans la base de données'}), 400
        
        return jsonify({'tkt': 'ok'}), 200
```

##### Vérification de la conformité du réseau

Afin de m'assurer que le réseau passé par l'utilisateur est confirme et existe bel et bien j'ai créé la fonction `is_network_valid` fans la classe `network_scanner`.  
Je commence par vérifier la confirmité du format.
```py
        try:
            ipaddress.IPv4Network(network)
        except ValueError:
            return False
```
Puis je vérifie l'existance du réseau grâce à un ping sur le routeur
```py
        try:
            # Ping du routeur
            timeout = 0.1
            result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), router_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
```

Une fois toutes ces confition remplies, le réseau est ajouté dans la base de données.

### Conclusion
J'ai réussi à continuer sur ma lancée des jours précédents, cependant, je sens que je suis un peu brouillon dans ma façon de penser. Il faut que je plannifie plus mes actions dans le futur.  
Demain je vais me conctrer sur l'ajout des cameras de façon dynamique dans la base de données.

## 17.04.2024
Comme précisé hier, aujourd'hui je vais commencer par ajouter les cameras de façon dynamique dans la base de données. Ensuite, je vais procéder à l'installation de la seconde camera.

### Ajout dynamique des cameras dans la base de données
Pour ce faire, je vais continuer à développer mon endpont `cameras_data` qui ne serais pas réelement utilisé dans le projet final, il me permet juste de développer les fonctionnalités que je vais implémenter une fois l'architecture de mon projet terminée.  
Je récupère les tokens dans un dictionnaire dans la fonction `getCamerasTokens`.
```py
tokens_for_ip = {}
        for cameraip in self.camerasIPs:
        [...]
        if response.status_code == 200:
                tokens_for_ip[camera_url] = response.json().get('token').
```
![réussite dict](./ressources/images/reussitedict.png)

J'ajoute ensuite trois fonctions dans ma classe `DatabaseClient`.
1. `getNetworkIdByIpAndSubnetMask` qui me permettra de récupérer l'id du réseau en utilisant l'adresse IP et le masque de sous réseau.
2. `addCameras` qui ajoutera les cameras dans la base et utilisera la fonction au dessus pour trouver le réseau relié. Pour l'ajout de camera, uniquement cette fonction sera appelée par la route.
3. `checkIfCameraExists` qui vérifira si une camera est déjà présente dans la base en se basant sur son ip et le réseau.

J'ai implémenté les fonctions et le résultat fonctionne. L'ajout dynamique des cameras dans la base est terminée.

![db camera implementation](./ressources/images/dbCameraImplémentation.png)

### Ajout d'une seconde camera

Afin de vérifier que mon système fonctionne, il faut que je créer une seconde camera. Cependant, le temps d'installtion de opencv est conséquent. J'en profite pour réfléchir à l'architecture de l'application.

### Discussion avec Monsieur Zanardi
1. Il m'a confirmé qu'il serait meilleur de développer l'application multiplateforme en parallèle de l'API afin de terminer un maximum de fonctionnalités avant la fin du projet.
2. Il m'a consillé d'ajouter la date d'expiration avec les JWT dans la base de données avec les cameras, comme ça on peut appeler automatiquement le endpoint pour les regénérer en cas de besoin.
3. Il m'a consiller de créer un diagramme général de mon projet et de spécifier dans la document de quel partie il s'agissait.
4. Trouver un outil afin de générer un disgramme de classes.

### Début du développment de l'application multiplateforme
L'application sera développée en Kivy python. Pour l'implémentation, j'ai decidé de faire deux user story afin de m'aider dans l'organisation de mon développement.

#### Initialisation

![initialisation](./ressources/images/userstory1_intialisation.jpg)

##### Page 1 : Recherche de serveur

Cette page va servir d'indication visual à l'utilisateur que le système est à la recherche d'un serveur. Une fois le serveur trouvé, il sera automatiquement redirigé.

###### Implémentation graphique

![](./ressources/images/recherchedeserveurform.png)

```
<ServerResearchWindow>
    name: "Research"
    
    GridLayout:
        cols: 1
        
        Label:
            text: "Recherche de serveur"
            font_size: '24sp' 
            bold: True
        Image:
            source: 'Ressources/logo.png'
        Label:
            text: "Veuillez patienter"
```

###### Implémentation

Je commence par créer la classe `NetworkScanner`. Je vais reprendre le code que j'ai utilisé dans mon serveur. Cependant j'ajoute une fonction statique me permettant de récupérer le réseau local de l'utilisateur.

```py
@staticmethod
    def get_local_network():
        ip = socket.gethostbyname(socket.gethostname())
        return '.'.join(ip.split('.')[:-1]) + '.0/24'
```

J'ajoute la recherche en asyncrone du réseau.

```py
def on_enter(self):
    Clock.schedule_once(self.run_network_scan)

def run_network_scan(self, dt):
    self.networkScanner = NetworkScanner()
    Clock.schedule_once(lambda dt: self.async_scan_ips(self.SERVER_PORT), 0)

def async_scan_ips(self, port):
    ip_serveur = self.networkScanner.scan_ips(port)
```
Si un réseau est trouvé, il est redirigé vers la page suivante, sinon, un message d'erreur apparait et un bouton s'active lui permettant de réessayer. L'ip du serveur est stockée dans une variable de l'application.

```py
if ip_serveur:
            app = App.get_running_app()
            app.ip_serveur = ip_serveur
            self.manager.current = "main"
        else:
            self.ids.state_label.text = "Erreur: Aucun serveur SRS trouvé sur votre réseau."
            self.ids.state_label.color = (1, 0, 0, 1) 
            self.ids.retry_button.disabled = False
```

###### Vérification de l'initialisation
J'ai ajouté un endpoint permettant de savoir si le serveur est initialisé.

```py
def is_set_up(self):
        if self.db_client.isAdminTableEmpty():
            return jsonify({'erreur': 'Le serveur n\'est pas configuré'}), 400
        else:
            return jsonify({'message': 'Le serveur est configuré'}), 200
```
Je l'appèle ensuite afin de choisir vers quel page j'envoie l'utilisateur.

```py
if serverClient.is_server_set_up():
                self.manager.current = "main"
            else:
                self.manager.current = "initializeLogin"
```

##### Transmission des données
Je devais trouver une façon de transmettre l'ip du serveur de façon globale dans l'application. J'ai donc crée une propriété à la classe main et je la met à jour quand il y en a le besoin.

```py
class MyMainApp(App):
    server_ip = None

    def build(self):
        # Retourne l'interface utilisateur chargée à partir du fichier app.kv
        return kv

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def get_server_ip(self):
        return self.server_ip
```

### Conclusion
Je pense avoir bien avancé aujourd'hui. J'ai débuté le développement de l'application en parallèle à l'api et je pense que c'était le bon choix. J'ai l'impression de progresser bien plus vite et ça m'a enlevé une pression liée au rendu de l'api. Demain je vais faire la suite de l'initialisation.

## 18.04.2024
Comme indiqué hier, aujourd'hui je vais commencer par terminer la séquence de l'initialisation.

### Page 2 : Première connexion

#### Interface

J'ai commencé par développer l'interface graphique.

![Page d'initialisation](./ressources/images/pageinitialisation.png)
```
<InitializeLoginWindow>
    name: "initializeLogin"

    GridLayout:
        rows: 2

        GridLayout:
            cols: 1

            Label:
                font_size: '30sp' 
                text: "Page d'initialisation"
                bold: True


            Image:
                source: 'Ressources/logo.png'

        GridLayout:
            cols: 1
        
            Label:
                text: "Veuillez entrer les identifiants d'initialisation."
                font_size: '24sp' 
                bold: True

            TextInput:
                id: username_textInput
                hint_text: "Nom d'utilisateur"
                font_size: '20sp' 

            TextInput:
                id: password_textInput
                hint_text: "Mot de passe"
                font_size: '20sp' 

            Button:
                id: submit_button
                text: "Se connecter"
                bold: True

```

#### Sécurisation du input

J'ajoute ensuite la désactivation du bouton *Se connecter* si un des input est vide.
```py
    def update_boutton(self):
        username = self.ids.username_textInput.text
        password = self.ids.password_textInput.text

        if username == "" or password == "":
            self.ids.submit_button.disabled = True
        else:
            self.ids.submit_button.disabled = False
```

Et j'appelle cette fonction à chaque changement de texte.
```
TextInput:
    id: username_textInput
    [...]
    on_text: root.update_boutton()

TextInput:
    id: password_textInput
    [...]
    on_text: root.update_boutton()
```

#### Appel du création du client api

Je commence par ajouter une fonction dans la classe `ServerClient` qui appellera le endpoint et réagira en fonction de la réponse http. Si la connection est réussi, elle stockera les données dans une variable d'instance de la classe.

```py
def initialize_login(self, username, password):
        if not self.server_ip:
            return False
        
        endpoint_url = f"{self.server_url}/initialize"
        auth = (username, password)
        
        response = requests.get(endpoint_url, auth=auth)

        if response.status_code == 200:
            print("Initialisation réussie.")
            self.initialize_token = response.json().get("token")
            return True
        elif response.status_code == 403:
            print("Identifiants de connexion manquants ou erronés.")
            return False
        elif response.status_code == 402:
            print("Impossible d'ajouter l'admin quand un autre est déjà présent.")
            return False
        else:
            print(f"Erreur inattendue: {response.status_code}")
            return False
```

En passant, j'ajoute le masquage du input de mot de passe.
```py
TextInput:
    [...]
    password: True
```

Avec cette partie terminée, je peux passer à la troisième page, l'ajout du premier admin.

### Page 3 : Ajout du premier admin
Je commence encore une fois par développer l'interface graphique. Cette fois-ci, je reprends basiquement la page précédente mais j'ajoute quelques indications pour l'administrateur.

![page d'ajout admin](./ressources/images/pageajoutpremieradmin.png)
```
<AddFirstAdminWindow>
    name: "addFirstAdmin"

    GridLayout:
        rows: 2

        GridLayout:
            cols: 1

            Label:
                font_size: '30sp' 
                text: "Page d'ajout du premier administrateur"
                bold: True


            Image:
                source: 'Ressources/logo.png'
            
            Label:
                text: "Veuillez entrer les identifiants du premier administrateur."
                font_size: '24sp' 
                bold: True
                
            
        GridLayout:
            cols: 1

            Label:
                id: status_label
                text: "Attention : Une fois le premier utilisateur ajouté, il est impossible de refaire cette procédure."
                bold: True

            TextInput:
                id: username_textInput
                hint_text: "Nom d'utilisateur"
                font_size: '20sp'
                on_text: root.update_boutton()

            TextInput:
                id: password_textInput
                hint_text: "Mot de passe"
                font_size: '20sp' 
                password: True
                on_text: root.update_boutton()

            Button:
                id: submit_button
                text: "Se connecter"
                bold: True
                disabled: True
```

Je crée la classe `AddFirstAdmin` et garde globalement la même structure pour mon application que dans le formulaire d'initialisation. La partie qui change c'est la classe `ServerClient`.
J'ajoute la fonction `add_first_admin` permettant d'appeler le endpoint eponyme.

```py
def add_first_admin(self, admin_name: str, clear_password: str):
        if not self.server_ip:
            return False

        hashed_password = ServerClient.hash_password(clear_password)
        endpoint_url = f"{self.server_url}/first_admin"
        params = {
            "username": admin_name,
            "password": hashed_password,
            "token": self.initialize_token
        }

        response = requests.post(endpoint_url, params=params)

        if response.status_code == 201:
            print("Admin ajouté avec succès.")
            return True
        else:
            return response.json().error
```

Je crée une fonction de hashage de mot de passe que j'appelle dans ma fonction d'ajout.

```py
@staticmethod
    def hash_password(password : str):
        password_bytes = password.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(password_bytes)
        hashed_password = hasher.hexdigest()
        return hashed_password
```

À présent, je dois créer la fonction de vérification de rebustesse du mot de passe. J'utilise les critères suivants :
1. Au moins 8 charactères
2. Au moins une majuscule et une minuscule
3. Au moins un chiffre
4. Au moins un charactère spécial.  

Pour ce faire je vais utiliser la librairie re me permettant de trouver des correspondances dans ma chaine.

```py
@staticmethod
def check_password_strength(password):
    # Au moins 8 charactères
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères."
    # Au moins une majuscule et une minuscule
    if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule et une lettre minuscule."
    # Au moins un chiffre
    if not re.search("[0-9]", password):
        return False, "Le mot de passe doit contenir au moins un chiffre."
    # Au moins un charactère spécial.
    if not re.search("[!@#$%^&*()-_=+{};:,<.>]", password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial parmi !@#$%^&*()-_=+{};:,<.>."
    return True, "Le mot de passe est robuste."
```

### Page 4 : Connexion

Après l'initialisation, l'utilisateur est renvoyé vers la page de connexion. Cette page va servir pour cette procédure mais également comme login classique. Encore une fois, la page ressemble aux autres formulaires.

![Login Page](./ressources/images/loginpage.png)

```
<LoginWindow>
    name: "login"

    GridLayout:
        rows: 2

        GridLayout:
            cols: 1

            Label:
                font_size: '30sp' 
                text: "Page de connexion"
                bold: True


            Image:
                source: 'Ressources/logo.png'

        GridLayout:
            cols: 1

            Label:
                id: status_label
                text: "Veuillez entrer vos identifiants"
                font_size: '24sp' 
                bold: True

            TextInput:
                id: username_textInput
                hint_text: "Nom d'utilisateur"
                font_size: '20sp'
                on_text: root.update_boutton()

            TextInput:
                id: password_textInput
                hint_text: "Mot de passe"
                font_size: '20sp' 
                password: True
                on_text: root.update_boutton()

            Button:
                id: submit_button
                text: "Se connecter"
                bold: True
                disabled: True
                on_release: root.login()
```

#### Passage en Basic auth
J'avais développé mon api pour fonctionner avec des paramêtres. Cependant, je trouve plus propre que l'authentifaction se fasse par **Basic auth**

##### Modificaiton de la route
```py
def admin_login(self):
        """
        Permet à l'administrateur de se connecter. Retourne un JWT si tout est ok.
        """
        if self.db_client.isAdminTableEmpty():
            return jsonify({'erreur': 'Aucun administrateur n\'est présent dans le système.'}), 403
        
        auth = request.authorization

        # Vérification des données de connexion
        if self.db_client.adminLogin(auth.username, auth.password):
            return jsonify({'token': JwtLibrary.generateJwtForAPI(auth.username)}), 200
        else:
            return jsonify({'erreur': 'Les identifiants de connexion sont erronés'}), 400
```

### Fin de l'implémentation de la première user story
J'ai terminé le travail sur l'initialisation. À présent, je vais développer la page principale qui servira de navigation entre les différentes fonctionnalités de l'application.

### Première fonctionnalité : Gestion des données faciales

Afin de pouvoir commencer à développer la recherche de personnes dans l'espace je dois d'abord avoir les données des personnes en question.

#### Ajout d'une personne
Je commance par l'ajout afin que je puisse développer la reconnaissance spaciale au plus vite.

##### Interface
Pour l'interface je dois premièrement avoir les éléments suivants :
1. Retour de la camera en temps réel.
2. Un bouton qui permet de prendre une photo.
3. Un text input permettant d'indiquer le nom de la personne.
4. Un spinner afin de séléctionner une "fonction" pour la personne.

![Page ajout personne](./ressources/images/pageajoutpersonne.png)

##### Récupération du flux
Grâce au composant [`Camera` de Kivy](https://kivy.org/doc/stable/api-kivy.uix.camera.html) je suis en capacité de récupérer assez facilement le flux.

Pour lancer la capture il faut définir la propriété `self.ids.qrcam.play` à `True`. Grace à cela, je suis capacité de prendre des "photos".

Pour le passage de Kivy texture en frame de opencv j'ai trouvé [ce sujet](https://stackoverflow.com/questions/68416721/kivy-camera-get-image) sur Stack Overflow.

J'ai ensuite demandé à ChatGPT s'il y a une solution pour convertir un tableau de pixel pour l'utiliser avec OpenCV.  

[Prompt ChatGPT](https://chat.openai.com/share/a9213221-d300-4392-8338-407b3bc951f0)

### Conslusion
J'ai réussi à implémenter les fonctionnalités que je voulais aujourd'hui. Pour l'instant la communication entre l'application et l'api se passe bien, je n'ai rencontré aucun problème majeur. Demain je vais commencer par l'ajout d'utilisateur.

## 19.04.2024

#### Bilan de la veille
J'avais oublié de faire ce rapport journalier cette semaine malhueureusement.
Hier j'ai travaillé sur les pages de mon application en utilisant les user story que j'ai créer par avance. Je me suis arrêté au moment où j'allais implémenter l'ajout des utilisateurs.

#### Plannification de la journée
Je vais commencer par créer la base de données des utilisateurs, une fois cela fait, je vais ajouter le endpoint et enfin l'implémenter dans mon application



### Ajout d'utilisateurs

![Page ajout story](./ressources/images/pageajoutstory.jpg)

##### Chemin rouge
Ce chemin représente la récupération des types des personnes (associés, danger etc.) afin de pouvoir les ajouter dans le spinner.
1. Appel du endpoint.  
2. Vérification JWT.
3. Query vers la bdd.
4. Récupération des données.
5. Passage des données dans la http response.
6. Ajout des types dans le spinner.

##### Chemin noir
Ce chemin permet d'ajouter une personnes dans la base.
1. Prise de la photo.
2. Séléction du type dans le spinner.
3. Indication du nom de la personne.
4. Vérification de la conformité des données faciales.
5. Récupération des encodages.
6. Appel du endpoint.
7. Vérification du JWT du serveur.
8. Ajout des données dans la bdd.
9. Retour via Http response et code.

#### Base de données
Je commence par l'implémentation de la base de données. J'étais incertain du type de stockage pour les encodages. J'ai donc posé la question à ChatGPT et selon lui le type `BLOB` correspondait le mieux.  
[Prompt ChatGPT](https://chat.openai.com/share/9ada3d6b-826e-4f31-95ae-ef39722dc492)

![UML types et personnes](./ressources/images/umlTablePersonnesEtTypes.png)

#### Ajout des routes dans l'API

##### Route rouge

Dans la classe `DatabaseClient` je crée la query.

```py
def getPersonTypes(self):
    try:
        self.cursor.execute("SELECT * FROM PersonTypes")
        return self.cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
```

J'ajoute la route dans `app.py`.
```py
self.app.add_url_rule('/person_types', 'person_types', self.person_types, methods=['GET'])

[...]

@JwtLibrary.API_token_required
def person_types(self):
    return jsonify(self.db_client.getPersonTypes()), 200
```

##### Route noir

Pour l'ajout d'utilisateurs, je commence par créer la query. Et je me rend compte que j'ai oublié d'ajouter le nom des utilisateurs. Je corrige mon erreur.

Afin d'éviter les erreurs, j'ajoute une vérification si le type de personne existe ainsi qu'un test si l'utilisateur existe déjà.

```py
    def checkIfIdPersonTypeExist(self, idPersonType):
        try:
            self.cursor.execute("SELECT * FROM PersonTypes WHERE idPersonType = %s", (idPersonType))
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def checkIfUsername(self, username):
        try:
            self.cursor.execute("SELECT * FROM Users WHERE username = %s", (username))
            results = self.cursor.fetchall()
    
            if len(results) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
```

J'implémente ensuite la query complète.

```py
    def addUser(self, idPersonType, encodings, username : str):
        try:
            if not self.checkIfIdPersonTypeExist(idPersonType):
                return False, f"Impossible d'ajouter l'utilisateur : Le type de personne n'existe pas."
            
            if self.checkIfUsername(username):
                return False, f"Impossible d'ajouter l'utilisateur : Un utilisateur avec le même nom existe déjà dans la base"
            
            self.cursor.execute("INSERT INTO srs.Users (idPersonType, encodings, username) VALUES(%s, %s, %s);", (idPersonType, encodings, username))
            self.dbConnexion.commit()
            return True, "L'utilisateur a été ajouté avec succès."
        except Exception as e:
            print(f"Error: {e}")
            return False, f"Impossible d'ajouter l'utilisateur : {e}"
```

Et pour terminer, j'ajoute la route.

```py
    @JwtLibrary.API_token_required
    def add_user(self):
        idPersonType = request.args.get('idPersonType')
        encodings = request.args.get('encodings')
        username = request.args.get('username')

        result, response = self.db_client.add_user(idPersonType, encodings, username)

        if result:
            return jsonify({'message' : response}), 200
        else:
            return jsonify({'erreur' : response}), 400
```

### Implémentation dans l'application

#### Route rouge

Je fais l'appel du endpoint avec le token de l'API. Si la requête a fonctionné, la réponse en json, cet a dire un tableau de résultat est retourné, si c'est un echec, la réponse complète est envoyée.

```py
def get_person_types(self):
        if not self.server_ip:
            return False
        
        params = {
            "token": self.API_token
        }
        
        endpoint_url = f"{self.server_url}/person_types"
        response = requests.get(endpoint_url, params=params)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response
```

Pour ajouter les données dans le spinner, je commence par faire une liste des fonctions puis je la transmet au spinner.

```py
    def get_person_types(self):
        result, response = self.server_client.get_person_types()

        if result:
            for data in response:
                self.personTypes.append(data[1])
                self.ids.function_spinner.values = self.personTypes
            return True, response
        else:
            return False, response
```

Avec ces fonctionnalités implémentée, la récupération dynamique des noms des fonctions est implémentée.

![résultat route rouge](./ressources/images/resultrouterouge.png)

#### Route noir
Pour implémenter l'ajout, il faut que je commence par ajouter la sécurisation des input. L'objectif est que la possibilité d'ajouter l'utilisateur s'active si :
1. La video est en pause
2. Un élément du spinner est séléctionné
3. Un nom est indiqué.

J'ai implémenté une fonction qui est appellée à chaque fois qu'un élément subit une modification.

```py
    def enable_add_button(self):
        username = self.ids.username_textInput.text.strip()
        function_selected = self.ids.function_spinner.text != "Sélectionnez une fonction"
        
        if username and function_selected and not self.ids.qrcam.play:
            self.ids.add_user_button.disabled = False
        else:
            self.ids.add_user_button.disabled = True
```
Une fois cela fait, dans la classe `ServerClient` j'ajoute le client du endpoint

```py
    def add_user(self, username, idPersonType, encodings):
        if not self.server_ip:
            return False, "ip du serveur manquante"

        endpoint_url = f"{self.server_url}/add_user"
        params = {
            "username": username,
            "idPersonType": idPersonType,
            "encodings": encodings,
            "token": self.API_token
        }

        response = requests.post(endpoint_url, params=params)

        if response.status_code == 201:
            return True, response.json()
        else:
            return False, response.json()
```

Pendant l'implémentation dans la route je me suis posé une question, si les fonction changent, récupérer les id du spinner afin de l'ajouter dans la base ne serait pas suffisant car ils serait erronées. Par conséquent, je développe un nouvel endpoint qui me permettera de récupérer l'id d'une fonction par son nom.

```py
@JwtLibrary.API_token_required
    def person_type_by_name(self):
        typeName = request.args.get('typeName')

        result, response = self.db_client.getPersonTypeByName(typeName)

        if result:
            return jsonify({'message' : response}), 200
        else:
            return jsonify({'erreur' : response}), 400
```

J'ai eu un problème lors du passage des encodings dans l'url. Premièrement, j'ai trouvé ça assez brouillon et les données était formées de façon étrange. J'ai donc décidé de passer les encodage des visage dans le body. Je passe également le nom de la personne et id du type de la personne. Le token je le passe toujours par url pour des quesiton d'intégration.

```py
def add_user(self, username, idPersonType, encodings):
        if not self.server_ip:
            return False, "ip du serveur manquante"

        endpoint_url = f"{self.server_url}/add_user"

        encodings_list = [encoding.tolist() for encoding in encodings]

        data = {
            "username": username,
            "idPersonType": idPersonType,
            "encodings": encodings_list,
        }

        # Encoder les données en JSON
        data_json = json.dumps(data)

        url_with_token = f"{endpoint_url}?token={self.API_token}"

        response = requests.post(url_with_token, data=data_json)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
```

### Résultat de l'ajout
Avec l'intégration dans les différents composant, l'ajout de personnes est fonctionnel.

#### Application

Je remplis toutes les données, dans cet exemple, je m'appelle **Jackes** et je suis **dangereux**. Après la pression du bouton d'ajout, la requête est envoyé vers le serveur.

![Application d'ajout](./ressources/images/applicationajout.png)

#### Base de données

Mes données ont été ajoutées dans la base, les données faciales sont dans le champs encodings et mon nom dans username.  
![Bdd Ajout](./ressources/images/bddajout.png)

### Page de modification des cameras

À présent que j'ai terminé l'ajout des utilisateurs, je peux commencer l'a modification des données des cameras. L'objectif est de pouvoir définir l'emplacement de la camera dans une pièce afin d'effectuer les calculs. Comme d'habitude je vais effectuer une user story en premier lieu.  
J'ai continué avec mon système de deux routes séparées.

**Route bleue :** Point d'entrée d'obtention des données des cameras.  
1. L'application cherche à afficher les cameras disponibles sur le réseau.
2. L'application appelle l'endpoint afin de récupérer les données
3. L'endoit vérifie si les JWT sont toujours valides via les dates d'expiration.
4. Si le JWT est valide, il recherche les adresses ip dans la bdd.
5. Si le JWT est expiré, le serveur scanne le réseau et met à jour les informations des cameras.
6. Retour des données des cameras dans la réponse.  

**Route Rouge :** Point d'entrée de mise à jour des données des cameras. Utile si l'admin veut mettre à jour le système de caméras.  
1. L'utilisateur appuye sur actualiser.
2. Le serveur fait directement une mise à jour des cameras.
3. Recherche des cameras sur le réseau.
4. Mise à jour des données dans la base.
6. Retour des données des cameras dans la réponse.

![](./ressources/images/recherchecamerastory.jpg)

#### Conclusion
J'ai terminé l'ajout des personnes, bien que ce processus a pu paraître long, j'ai appris à mieux gérer mes différentes technologies alors je pense que le était bien investi. La prochaine fois, je vais me concentrer au développement de la user story suivante.

## 22.04.2024

#### Bilan de la semaine dernière
La dernière fois que j'ai travaillé j'ai terminé l'ajout de personnes dans la base de données. Ensuite, j'ai créé une nouvelle *User Story* pour la gestion des cameras.

#### Planificaiton de la journée
J'ai eu l'occasion de réfléchir à mon système et je me suis rendu compte que je ne gérairais pas le cas où une des camera ne serait plus disponible. Je vais commencer par ça.

### Vérification de l'identité des cameras Wifi

Je vais ajouter une vérification de la disponibilité des cameras en faisant un appel à l'endpoint `/ping`. Cela me permettra de vérifier l'identité des serveurs des cameras lors de la recherche.  
L'endpoint est très basique car la vérification du token est dans la fonction décoratrice `@token_required`.

```py
@app.route('/ping', methods=['GET'])
@token_required
def ping():
    return jsonify({'Status du serveur' : 'Disponible'}), 200
```

### Ajout de la position des cameras
Afin de pouvoir définir la position des cameras, je dois prendre en compte deux facteurs - la position relative au mur et l'emplacement du mur. En suivant les conseils de Monsieur Zanardi, je dois me concentrer à ce que mon système fonctionne dans les pièces carrées. Cependant, je dois réfléchir à comment mon système fonctionne.  
J'ai décidé de fonctionner par le modèle suivant, l'utilisateur servant de point d'intersection entre les différents axes X des cameras. Si les cameras ne sont pas tout à fait au milieu des murs, suffira d'ajuster l'axe X de la camera.

![Modèle reconnaissance spaciale](./ressources/images/modeleReconnaissanceSpaciale.jpg)

J'ai commencé par créer une nouvelle table `Walls` qui contiendra des 4 postion des murs (Nord, Est, Sud et Ouest). J'ai ensuite ajouté une relation vers la table camera.  
![](./ressources/images/umlWalls.png)  
![](./ressources/images/wallsValues.png)

#### Interface

Pour l'interface, je voulais qu'elle comporte les éléments suivants :

1. *Spinner* : Permet de séléctionner une camera
2. *Scroll View* : Permet de séléctionne la position de la camera relative au mur.
3. *Spinner* : Permet d'afficher sur quel mur la camera se situe.
4. *?* : Un élément permettant de voir la postion en temps réel de la camera en fonction des données de l'utilisteur. Je compte implémenter cette vue plus tard.
5. *Button* : Permettant de mettre à jour les données des cameras.

##### Maquette

![](./ressources/images/maquetteGestionCamera.jpg)

##### Implémentation

J'ai affiché l'affichage de la valeur de la position.

![](./ressources/images/interfaceGestionCamera.png)

```
<CamerasManagementWindow>:
    name: "camerasManagement"

    FloatLayout:
        GridLayout:
            cols: 3
            size_hint: 1, 0.1  
            pos_hint: {'top': 1} 

            Button:
                text: "<- Retour"       
                on_release:
                    app.root.current = "main" 
                    root.manager.transition.direction = "right"

            Label:
                text: "Gestion des cameras"
                bold: True

            Image:
                source: 'Ressources/logo.png'

        GridLayout:
            cols: 1
            size_hint_y: 0.9

            Spinner:
                id: camera_spinner
                text: "Sélectionnez une camera"
                values: ["Fonction 1", "Fonction 2", "Fonction 3"]
                on_text: root.camera_changed()
            
            Button:
                id: update_cameras_list_button
                text: "Mettre à jour la liste des cameras"
                on_release: root.update_cameras_list()

            GridLayout:
                cols:2
            
                Label:
                    text: "Position relative au mur :" + str(position_slider.value)

                Slider:
                    id: position_slider
                    min: 0
                    max: 100
                    step: 1
                    orientation: 'horizontal'

            Spinner:
                id: wall_spinner
                text: "Sélectionnez un mur"
                values: ["Fonction 1", "Fonction 2", "Fonction 3"]
                on_text: root.camera_changed()
            
            Button:
                id: update_camera_button
                text: "Mettre à jour la camera"
                on_release: root.update_camera()
                disabled: True
                bold: True
```

#### Récupération des types de mur

##### Route 
```py
self.app.add_url_rule('/walls', 'walls', self.walls, methods=['GET'])

@JwtLibrary.API_token_required
def walls(self):
    try:
        return jsonify(self.db_client.getWalls()), 200
    except Exception as e:
        return jsonify({'erreur' : str(e)}), 500
```

##### Client BDD

```py
def getWalls(self):
    try:
        self.cursor.execute("SELECT * FROM Walls")
        return self.cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
```

##### Récupération dynamique

```py
def get_walls(self):
        result, response = self.server_client.get_walls()

        if result:
            for data in response:
                self.walls.append(data[1])
                self.ids.walls_spinner.values = self.walls
            return True, response
        else:
            return False, response
```

##### Résultat

![](./ressources/images/recuperationMurs.png)

### Gestion des adresses MAC

Afin de garantir l'identité des cameras wifi, il serait interessant de stocker leurs adresses mac. Pour ce faire, j'adapte la route `ping` et je me sert [de cet article](https://www.geeksforgeeks.org/extracting-mac-address-using-python/). Je vais uniquement récupérer les valeurx hexadéciamales car il me faut uniquement comparer la correspondance. Je me sert de la librairie uuid.

```py
@app.route('/ping', methods=['GET'])
@token_required
def ping():
    return jsonify({'Mac address' : hex(uuid.getnode())}), 200
```

![](./ressources/images/macadressping.png)

### Récupération des cameras

Pour la récupération je vais commencer par gérer le cas où le réseau n'est pas dans la base de données. Si c'est le cas il faut :
1. Vérifier si le réseau existe.
2. Rechercher les cameras.
3. Récupérer les tokens et les adresses mac.
4. Ajouter les caméras et le réseau dans la base.
5. Récupérer la liste des caméras et l'envoyer dans la résponse.

```py
@JwtLibrary.API_token_required
    def cameras(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400

        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
            return jsonify({'erreur': 'Le réseau donné est inavalide'}), 400
        

        self.cameraServerClient = CameraServerClient(ip, subnetMask)

        networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)

        # Vérification si le réseau n'existe pas
        # Recherche automatique de caméras, vérification la présence des caméras et ajout dans la base.
        if(not self.db_client.checkIfNetworkExists(ip)):
            # Recherche automatique des cameras
            self.cameraServerClient.lookForCameras()
            # Donne la liste des ip des cameras ainsi que leurs tokens
            tokens_for_ip = self.cameraServerClient.getCamerasTokens()

            if(tokens_for_ip == None):
                return jsonify({'erreur' : 'Aucune caméra présente sur le réseau'}), 400
            
            # Ajoute les cameras dans la base de données
            self.db_client.addCameras(tokens_for_ip, ip, subnetMask)

            self.db_client.addNetwork(ip, subnetMask)

            return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)), 201
```

### Conclusion

Je termine la journée avec un petit, problème. En effet les idNetwork ne s'ajoutent pas aux cameras. C'est un problème dont je vais m'occuper demain. Je vais également continuer sur la récupération des données caméras, j'hésite à modifier l'architecture de mon projet pour faire quelque chose de plus propre aux niveaux des classes.

## 23.04.2024

#### Bilan de la veille

Hier je me suis concentrer sur la page de gestion des cameras ainsi que sur la procedure liés au cameras et leurs JWT. Je me suis arrêté sur un bug qui m'empêchait de relier la base `Network` et `Cameras`.

#### Objectif de la journée

Demain étant le jour pour l'évaluation intermédiaire, je dois me concentrer sur cet aspect en premier lieu. Je vais commencer par effectuer une analyse de mon travail en utilisant le document fournit et après je vais adapater mon travail si besoin.

### Auto-évaluation intermédiaire

Dans un mail envoyé par mes suiveurs, il m'a été demandé d'effectuer une auto-évalutaion afin de me préparer pour demain.

#### Prestation professionnelle

**Qualité du travail : tavail soigné** Je pense qu'il y a des améliorations à faire au niveau des commentaires, mais je pense que la structure de mon travail via le journal de bord est assez compréhensible, notament grâce à l'utilisation des user story on peut savoir sur quoi je travaille.

**Organisation du travail : logique et très efficace** Je pense que la façon dont j'approche le travail est efficace grâce à des choix rapides et logies comme le changement des jalons (passage en développement parallèle de l'API et de l'application)

**Rythme de travail : rapide** Selon moi j'ai effectué un bon travail niveau quantité. J'avance par point clé, ce qui est motivant car je vois mon travail évoluer concrètement.

**Squelette documentation : encore du travail** Pour le squelette, j'ai une structure pour chaque composant, ayant terminé le premier, je compte faire la même chose pour le reste. Il me reste cependant les tests, pour l'instant je me concentre sur les tests postman et moins les tests fonctionnels.

**Ordre des dossiers fichiers : exemplaire** Selon moi, j'ai trouvé une bonne structure pour que le projet soit compréhensible. Pour cet étape du projet elle me paraît bonne mais je compte tout de même l'améliorer par la suite.

#### Comportement au travail

**Engagement et persévérence : appliqué, persévérent** Le travail effectué tous les jours est plutôt bon pour l'instant, la motivation de voir le projet avancer m'aide beaucoup.

**Intérêt : très intéressé** Je crois fermement que ce projet est interessant même s'il possède des failles dans son idée de départ, j'essayerais de faire mon maximum pour le rendre le meilleur possible.

**Autonomie : totalement indépendant** Cette question est assez vague, il m'arrive de demander de l'aide quand deux chemin se présentent devant moi mais je n'ai pas été bloqué à cause du travail que je dois effectuer.

**Capacité à comprendre : comprend vite et bien** Pour l'instant je n'ai pas eu de problèmes à comprendre des nouvelles technologies, par exemple les jwt sont bien fonctionnels.

**Mise à jour des outils de partage: régulier** Il y a de l'amélioration à faire à ce niveau là, pour l'instant je fais un push par jour alors que je devrais le faire par fonctionnalité. Cependant, j'effectue des release à la fin des jalons.

#### Attitude personnelle

**Collaboration : très bonne, caractère sociable** Je ne suis par certain pour cette question car je ne suis pas connu comme quelqu'un de sociable. Cependant, les critiques de mes suiveurs je les prends avec plaisir.

**Façon d'être : neutre** Pour être honnête, je ne vois pas vraiment la plus value d'être prévenant et serviable dans un travail individuel je n'ai donc malheureusement pas d'exemples à donner.

**Conscience professionnelle : respecte les consignes** Pour l'instant j'effectue mon travail dans les temps et suit le schema typique des documentations et autres journaux de bords.

**Réponse aux communications : rapide** Pour être honnête, je n'ai pas répondu à une question posée par monsieur Zanardi par mail, mais c'était pendant les vacances et je n'étais pas forcément disponible. En temps normal, je suis accessible et répond aux question si besoin.

#### Bilan

Je pense pas que j'ai besoin de faire une mise à jour de mon travail pour mieux correspondre à l'évaluation intermédiaire. Les question sont plutôt orientées vers l'organisation du travail et la façon d'être vis-à-vis du travail. Si des améliorations sont à faire, je vais les effectuer pour l'évaluation d'après.

### Bug lors de l'ajout des cameras

Je vais recherche l'origine du bug qui m'empêche d'ajouter l'ip du réseau dans la table cameras.

Le prpblème provient de la fonction suivante qui retourne None :
```py
networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)
```

L'erreur était très simple à trouver, *trop simple*. J'ajoutais pas le réseau par conséquant je n'arrivais pas à récupérer son id. J'essaye d'ajouter le network puis la camera. Avec des modificiation apportés, le code fonctionne.
#### Table Network
![](./ressources/images/tableNetworkBug.png)

#### Table Cameras
![](./ressources/images/tableCameraBug.png)

#### Résultat final fonctionnel

![](./ressources/images/resultatpostmanrecherchedynamique.png)

#### Code adapté

```py
self.db_client.addNetwork(ip, subnetMask)

self.db_client.addCameras(tokens_for_ip, self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask))
```

### Récupération et ajout d'un network et caméras
Pour implémenter cette fonctionnalité, j'ai suivi la logique suivante :

#### Récupéraion du réseau et appel de l'API

##### Vue (cameras_management_window)
```py
    def get_cameras(self):
        result, response = self.server_client.get_cameras()
```

##### Client API (server_client.py)
```py
    def get_cameras(self):
        if not self.server_ip:
            return False
        
        print(ServerClient.get_netowk_from_ip(self.server_ip))
        
        params = {
            "token": self.API_token,
            "ip": ServerClient.get_netowk_from_ip(self.server_ip),
            "subnetMask": 24
        }
        
        endpoint_url = f"{self.server_url}/cameras"
        response = requests.get(endpoint_url, params=params)
```

#### Vérification des données et choix de la procédure

Ici, il est testé si le réseau n'est pas présent dans la table, par conséquent, le réseau est ajouté et les caméras sont recherchés dans ce dernier.

##### Récupération des données et choix de la procédure (app.py)

```py
    @JwtLibrary.API_token_required
    def cameras(self):
        ip = request.args.get('ip')
        subnetMask = request.args.get('subnetMask')

        if not ip or not subnetMask:
            return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400

        if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
            return jsonify({'erreur': 'Le réseau donné est inavalide'}), 400
        

        self.cameraServerClient = CameraServerClient(ip, subnetMask)

        networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)

        # Vérification si le réseau n'existe pas
        # Recherche automatique de caméras, vérification la présence des caméras et ajout dans la base.
        if(not self.db_client.checkIfNetworkExists(ip)):
```

##### Recherche du network (database_client.py)

```py
def getNetworkIdByIpAndSubnetMask(self, ip : str, submask : str):
        try:
            self.cursor.execute("SELECT idNetwork FROM Network WHERE ip = %s AND subnetMask = %s", (ip, submask,))
            results = self.cursor.fetchone()
    
            if results:
                return results[0]
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return False
```

```py
def checkIfNetworkExists(self, ip: str):
    try:
        self.cursor.execute("SELECT * FROM Network WHERE ip = %s", (ip,))
        results = self.cursor.fetchall()

        if len(results) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False
```

#### Recherche dynamique de camera
Il est important de noter que j'ai fais exprès de développer cette recherche de façon lente car j'ai eu des problèmes de fiabilité avec un timeout plus bas. Je compte rendre cette fonctionnalité asynchrone.

##### Fonctions de recherche par socket (network_scanner.py)

```py
    def scan_ips(self, port,  timeout=0.35):
        ip_with_port_open = []
        
        for ip in self.network.hosts():
            print(str(ip) + ":" + str(port))
            if self.check_port(ip, port, timeout):
                ip_with_port_open.append(str(ip))
                break

        return ip_with_port_open

    def check_port(self, ip, port, timeout):
        """
        Vérifie si un port spécifié sur une adresse IP donnée est ouvert.

        Args:
            ip (str): L'adresse IP à tester.
            port (int): Le numéro de port à vérifier.
            timeout (float): Le temps maximum en secondes à attendre pour une réponse.

        Returns:
            bool: Renvoie True si le port est ouvert, sinon False.
        """
        try:
            # Vérification de l'ouverture du port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((str(ip), port))
                return True
        except (socket.timeout, socket.error):
            return False
```

#### Ajout du réseau et des caméras dans la base

1. Ajout du réseau
2. Ajout des cameras avec l'id du réseau

##### Vue (app.py)

```py
self.db_client.addNetwork(ip, subnetMask)

self.db_client.addCameras(tokens_for_ip, self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask))
```

##### Client BDD (database_client.py)
```py
    def addNetwork(self, ip : str, submask : str):
        # Réseau déjà présent
        if self.checkIfNetworkExists(ip):
            return False
        
        try:
            self.cursor.execute("INSERT INTO srs.Network (ip, subnetMask) VALUES (%s, %s);", (ip, submask))
            self.dbConnexion.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
```

#### Envoi de la réponse et traitement

Pour cette partie, les données sont envoyé dans une liste dans la résponse de l'API. Enuite, interprété dans un objet camera pour pouvoir les afficher.

##### Envoi de la réponse (app.py)
La réponse envoie la liste des données caméras d'un réseau.

```py
return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)), 201
```
##### Interprétation des données (server_client.py)

Si le status est 201, cela veut dire que les nouvelles données ont été crées. On charge ensuite les données et je fait une boucle sur la liste des cameras, puis je crée une liste de cameras.

```py
if response.status_code == 201
    response_data = response.content.decode('utf-8')
    cameras_data = json.loads(response_data
    cameras = []
    for camera in cameras_data
        cameras.append(Camera(camera[0],camera[1],camera[2],camera[3],camera[4],camera[5],camera[6])
    return True, cameras
else:
    return False, response
```

#### Affichage des données 

##### Interprétation visuelle (cameras_management_window.py)

Si aucune camera n'est trouvée, alors l'application se bloque et affiche le texte correspondant à l'utilisateur.  
Si une camera est trouvée. L'adresse IP est ajoutée dans le spinner afin que l'utilisateur puisse la séléctionner.

```py
def get_cameras(self):
    result, response = self.server_client.get_cameras()
    
    cameras_ips = []
    if result:
        for camera in response:
            cameras_ips.append(str(camera.ip))
        if len(cameras_ips) < 1:
            self.ids.cameras_spinner.values = []
            self.ids.cameras_spinner.text = "Aucune camera trouvée sur votre réseau"
            self.ids.cameras_spinner.disabled = True 
        else:
            self.ids.cameras_spinner.text = "Veuillez séléctionner une camera"
            self.ids.cameras_spinner.values = cameras_ips
            self.ids.cameras_spinner.disabled = False 
```

#### Résultats

##### Vue : Application multiplateforme
![](./ressources/images/recuperationcamerascenario1.png)

##### Table Network : Base de données
![](./ressources/images/tablenetworkscenario1.png)

##### Table Cameras : Base de données
![](./ressources/images/tablescenarioscenario1.png)

#### Passage de l'appel de l'API en non bloquant

J'ai commencé par mettre l'appel en thread. Je n'ai pas besoin de le mettre en multiprocessing car c'est un simple appel et non une tache lourde.

```py
def on_enter(self):
    super().on_enter()
    self.app = App.get_running_app()
    self.server_client = self.app.get_server_client()
    self.get_walls_thread = threading.Thread(target=self.get_walls)
    self.get_walls_thread.start()
    self.get_cameras_thread = threading.Thread(target=self.get_cameras)
    self.get_cameras_thread.start()
```

Le problème c'est que j'avais ces erreurs :

```
File "kivy/graphics/instructions.pyx", line 672, in kivy.graphics.instructions.Canvas.remove
File "kivy/graphics/instructions.pyx", line 674, in kivy.graphics.instructions.Canvas.remove
File "kivy/graphics/instructions.pyx", line 88, in kivy.graphics.instructions.Instruction.flag_data_update
 TypeError: Cannot change graphics instruction outside the main Kivy thread
```

Et en effet, je me suis rappelé que j'avais une erreur similaire dans un projet précédent. Il faut effectivement ajouter les fonctionnalités qui changent la vue de Kivy sur le main thread en utilisant la librairie `Clock`.

```py

Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', self.walls))

if len(cameras_ips) < 1:
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', []))
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', "Aucune camera trouvée sur votre réseau"))
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', True))
else:
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'values', cameras_ips))
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', "Veuillez séléctionner une camera"))
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'disabled', False
```

### Route bleue

Cette route permet de récupérer les cameras dans un network déjà présent dans la base. Pour ce faire, il faut suivre les étapes suivantes.

1. Vérification de l'expiration des token JWT.
    - Récupération de la date de la dernière màj dans la table network.
    - Comparaison avec la date actuelle
2. Récupération des cameras.
    - Si le JWT est périmé, nouvel appel vers les cameras est effectué pour les renouveller.
    - Si valide, passage à l'étape suivante.
3. Vérification du fonctionnement des cameras.
    - Appel d'un endpoint, si non fonctionnel, nouveau scan des cameras (chemin rouge).

![](./ressources/images/recherchecamerastory.jpg)

##### Si le network est présent mais sans camera

Je récupère la liste des cameras, et si elle est vide, je met à jour les cameras dans le réseau.
```py
cameras = self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)
# Si aucune camera n'est dans le network, recheche de cameras.
if cameras == None:
    return self.initialize_cameras_in_network(ip, subnetMask)

def initialize_cameras_in_network(self, networkip, subnetMask):
    # Recherche automatique des cameras
    self.cameraServerClient.lookForCameras()
    # Donne la liste des ip des cameras ainsi que leurs tokens
    tokens_for_ip = self.cameraServerClient.getCamerasTokens()
    if(tokens_for_ip == None):
        return jsonify({'erreur' : 'Aucune caméra active n\'est présente sur le réseau'}), 400
    
    self.db_client.addCameras(tokens_for_ip, self.db_client.getNetworkIdByIpAndSubnetMask(networkip, subnetMask))
    return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(networkip, subnetMask)), 201
```

##### Si le network a besoin d'une mise à jour des JWT
1. Je vérifie si les JWT sont valides

```py
# Test dans la route
if self.db_client.areTheCamerasInTheNetworkInNeedOfAnUpdate(networkId):

# Methode de comparaison dans le database_client
def areTheCamerasInTheNetworkInNeedOfAnUpdate(self, idNetwork):
network = self.getNetwork(idNetwork
return DatabaseClient.isOlderThan24Hours(str(network[3]))
```

2. Si expiré, mise à jour des tokens de toutes les cameras.

```py
# Dans la route, je fais une boucle sur toutes les cameras.
for camera in cameras:
    self.db_client.updateCameraToken(self.db_client.getByIdCameras(camera[0]), self.cameraServerClient.getCameraToken(camera[0]))
    self.db_client.refreshNetworkTimestamp(networkId)

# Fonctions dans database_client
def updateCameraToken(self, idCamera, token):
    try:
        self.cursor.execute("UPDATE Cameras SET JWT = %s WHERE idCamera = %s", (str(token), idCamera,))
        self.dbConnexion.commit()
        return True, "Token de la caméra mis à jour avec succès."
    except Exception as e:
        print(f"Erreur lors de la mise à jour du token de la caméra : {e}")
        return False, f"Erreur lors de la mise à jour du token de la caméra : {e}"

# Recherche d'une camera par l'id
def getByIdCameras(self, idCamera):
    try:
        self.cursor.execute("SELECT * FROM Cameras WHERE idCamera = %s", (idCamera,))
        return True, self.cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")

# Met à jour la date avec la date actuelle
def refreshNetworkTimestamp(self, idNetwork):
try:
    self.cursor.execute("UPDATE Network SET lastUpdate = %s WHERE idNetwork = %s", ('CURRENT_TIMESTAMP', idNetwork))
    self.dbConnexion.commit()
    return True, "Dernière mise à jour modifiée avec succès"
except Exception as e:
    return False, f"Erreur lors de la mise à jour de la dernière modification : {e}"

# Fonction dans camera_Server_client

# Permet d'obtenir un token par l'ip de la camera
@staticmethod
def getCameraToken(cameraIp):
    camera_url = "http://{ip}:{port}".format(ip = cameraIp, port = CameraServerClient.__CAMERAS_SERVER_PORT)
    auth = (CameraServerClient.__CLIENT_USERNAME, CameraServerClient.__CLIENT_PASSWORD)
    response = requests.get(f"{camera_url}/login", auth=auth)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print("Échec de l'obtention du token JWT pour l'ip : {ip}:".format(ip=cameraIp), response.status_code)
```
#### Conclusion

Aujourd'hui j'ai réussi à terminer la récupération des cameras. Demain, je vais commencer par la modification des données des cameras.

## 24.04.2024

#### Bilan de la veille
Hier j'ai eu l'occasion de me concentrer sur le système de récupération des cameras. De m'adapter en fonction de la situation du réseau, de la situation des cameras et ainsi de suite. J'ai également effectué une auto-évaluation intermédiaire pour préparer celle d'aujourd'hui.

#### Planification du jour
Je vais commencer par développer le système de mise à jour de cameras. Aujourd'hui est égalment le jour de l'évaluation intermédiaire, cependant je ne sais pas à quelle heure elle est planifiée.

### Mise à jour des cameras


#### Vue

Pour commencer, il faut que j'adapte ma vue en fonction de l'état de séléction du spinner des cameras.

Je crée une fonction - `change_view_input_state()` qui me sert à changer l'état des input de ma vue.
```py
def change_view_input_state(self, viewDisabled : bool):
    self.ids.update_cameras_list_button.disabled = viewDisabled
    self.ids.position_slider.disabled = viewDisabled
    self.ids.walls_spinner.disabled = viewDisabled
    self.ids.update_camera_button.disabled = viewDisabled
```


J'ajoute ensuite une nouvelle fonction - `camera_changed(input_text)` qui est appelé à chaque changement dans le spinner de la camera.

```py
def camera_changed(self, input_text):
    self.change_view_input_state(not (input_text != self.TEXT_NO_CAMERA_FOUND and input_text != self.TEXT_CAMERA_FOUND))
```

```
Button:
    id: update_camera_button
    text: "Mettre à jour la camera"
    disabled: True
    on_release: root.update_camera()
    disabled: True
    bold: True
```

##### Résultats

![](./ressources/images/camerainputmanagamentdisabled.png)
![](./ressources/images/canerainputmanagementactivaded.png)

#### 1 : Mise à jour des cameras

Pour le bouton *Mettre à jour la liste de cameras*, il faut que je crée un nouvel endpoint me permettant de forcer la nouvelle recherche de cameras sur le réseau. L'objectif de cette procesure c'est d'ajouter / supprimer les cameras en fonction de leur présence sur le réseau sans pour autant altérer les données des cameras qui n'ont pas changés.

1. Création du endpoint
2. Récupération des adresses actuelles des caméras présentes dans le réseau depuis la base.
3. Récupération des cameras dans le réseau actuel.
3. Comparaison des données
4. Adapatation de la base de données
5. Retour des nouvelles cameras dans la réponse
6. Faire l'appel vers l'API depuis le client
7. Désactiver tous les autres input
8. Interpréter les données

##### 1.1 : Création du endpoint

```py
self.app.add_url_rule('/update_camera_list', 'update_camera_list', self.update_camera_list, methods=['GET'])

@JwtLibrary.API_token_required
def update_camera_list(self):
     pass
```
##### 1.2 : Récupération des adresses actuelles des caméras présentes dans le réseau depuis la base

Je fais les mêmes vérification que avec le endpoint des `camera`. Si aucun réseau n'est présent, on le crée dans la fonction `initialise_network_with_cameras()`.

```py
@JwtLibrary.API_token_required
def update_camera_list(self):
    ip = request.args.get('ip')
    subnetMask = request.args.get('subnetMask')
    if not ip or not subnetMask:
        return jsonify({'erreur': 'Mauvais paramètres, utilisez (ip, subnetMask) pour l\ip du réseau et le masque de sous-réseau respectivement.'}), 400
    if not NetworkScanner.is_network_valid("{n}/{sub}".format(n = ip, sub = subnetMask)):
        return jsonify({'erreur': 'Le réseau donné est inavalide'}), 400
    
    self.cameraServerClient = CameraServerClient(ip, subnetMask)
    networkId = self.db_client.getNetworkIdByIpAndSubnetMask(ip, subnetMask)
    # Vérification si le réseau n'existe pas
    # Recherche automatique de caméras, vérification la présence des caméras et ajout dans la base.
    if(not self.db_client.checkIfNetworkExists(ip)):
        return self.intialise_network_with_cameras(ip, subnetMask)
    
    # Récupération des adresses actuelles des caméras présentes dans le réseau depuis la base
    cameras = self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)
```
##### 1.3 : Récupération des cameras dans le réseau actuel

```py
camera_server_client = CameraServerClient(ip, subnetMask)
cameras_in_network = camera_server_client.lookForCameras()
```

##### 1.4 : Comparaison des données
Pour récupérer la liste des caméras à ajouter j'ai crée un algorithme sur un tableau.  

Dans cet exemple, on commence par parcourir les cameras dans le réseau. Si on trouve une correspondance, on n'ajoute pas la camera.

![](./ressources/images/tableau_cameras_to_add1.jpg)  

Cependant, si une correspondance n'est pas trouvée, on ajoute la camera à la liste.

![](./ressources/images/tableau_cameras_to_add2.jpg)  

```py
def get_cameras_that_are_not_in_database(network_cameras : list, database_cameras : list):
    result_camera_list = []
    for network_camera in network_cameras:
        flag = False
        for database_camera in database_cameras:
            if network_camera == database_camera[1]:
                flag = True
                break
        if not flag:
            result_camera_list.append(network_camera)
```

Pour la liste des caméras à supprimer je fais l'inverse. Je commence par parcourir la liste des caméras dans la base puis celle du network. Si aucune correspondance n'est trouvée, la camera est ajoutée à la liste des caméras à supprimer.

![](./ressources/images/tableau_cameras_to_remove.jpg)  

```py
def get_cameras_that_are_not_in_network(network_cameras : list, database_cameras : list):
    result_camera_list = []
    for database_camera in database_cameras:
        flag = False
        for network_camera in network_cameras:
            if network_camera == database_camera[1]:
                flag = True
                break
        if not flag:
            result_camera_list.append(database_camera)
```

##### 1.5 : Adapatation de la base de données

Dans la classe `DatabaseClient` j'ai ajouté les fonctions `deleteCamerasFromNetwork()` ainsi que `addCamerasToNetwork()`

```py
def deleteCamerasFromNetwork(self, cameras : list, idNetwork : int):
    try:
        for camera in cameras:
            self.cursor.execute("DELETE FROM Cameras WHERE idCamera = %s AND idNetwork = %s", (camera, idNetwork,))
            self.dbConnexion.commit()
        return True, "Caméras supprimées du réseau avec succès."
    except Exception as e:
        print(f"Erreur lors de la suppression des caméras du réseau : {e}")
        return False, f"Erreur lors de la suppression des caméras du réseau : {e}"
def addCamerasToNetwork(self, cameras : list, idNetwork : int):
    try:
        for camera in cameras:
            self.cursor.execute("INSERT INTO Cameras (ip, idNetwork, JWT) VALUES(%s, %s, %s);", (camera['ip'], idNetwork, camera['token']))
            self.dbConnexion.commit()
        return True, "Caméras ajoutées au réseau avec succès."
    except Exception as e:
        print(f"Erreur lors de l'ajout des caméras au réseau : {e}")
        return False, f"Erreur lors de l'ajout des caméras au réseau : {e}"
```

Ces fonctions sont ensuite appelés par la roule :

```py
self.db_client.addCamerasToNetwork(cameras_to_add, networkId)
self.db_client.deleteCamerasFromNetwork(cameras_to_remove, networkId)
```

##### 1.6 : Retour des nouvelles cameras dans la réponse
Je retourne simplement la liste des cameras appartenant au network.

```py
return jsonify(self.db_client.getCamerasByNetworkIpAndSubnetMask(ip, subnetMask)), 201
```

##### 1.7 : Faire l'appel vers l'API depuis le client

Dans la classe `ServerClient`, je crée la fonction `update_camera_list` qui me permet de faire l'appel vers le endpoint et de créer dynamiquement les objets `Camera`.

```py
def update_camera_list(self):
    if not self.server_ip:
        return False
    
    print(ServerClient.get_netowk_from_ip(self.server_ip))
    
    params = {
        "token": self.API_token,
        "ip": ServerClient.get_netowk_from_ip(self.server_ip),
        "subnetMask": 24
    }
    
    endpoint_url = f"{self.server_url}/update_camera_list"
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 201:
        response_data = response.content.decode('utf-8')
        cameras_data = json.loads(response_data)
        cameras = []
        for camera in cameras_data:
            cameras.append(Camera(camera[0],camera[1],camera[2],camera[3],camera[4],camera[5],camera[6]))
        return True, cameras
    else:
        return False, response
```

Cette fonction est appelée de façon asyncrone depuis la vue quand le bouton `update_camera_list_button` est appuyé.

```py
def update_cameras_list(self):
    Clock.schedule_once(lambda dt: setattr(self.ids.cameras_spinner, 'text', self.TEXT_LOADING_CAMERA))
    self.ask_camera_update_thread = threading.Thread(target=self.ask_camera_update)
    self.ask_camera_update_thread.start()
    

def ask_camera_update(self):
    result, response = self.server_client.update_camera_list()
```

```
Button:
    id: update_cameras_list_button
    text: "Mettre à jour la liste des cameras"
    disabled: True
    on_release: root.update_cameras_list()
```

##### 1.8 : Désactiver les autres input

Je crée une fonction `change_all_view_input` qui me permet de définir l'état des input en fonction du booléen passé dans le paramètre.

```py
def change_all_view_input_state(self, viewDisabled : bool):
    self.ids.cameras_spinner.disabled = viewDisabled
    self.ids.update_cameras_list_button.disabled = viewDisabled
    self.ids.position_slider.disabled = viewDisabled
    self.ids.walls_spinner.disabled = viewDisabled
    self.ids.update_camera_button.disabled = viewDisabled
```

##### 1.9 : Interpréter les données

Dans la fonction `update_camera_list` dans la classe `ServeurClient`. Je fais en sorte que si je reçois une réponse **201** de récupérer les valeurs de la réponse en les stockant dans des objets `Camera` que je retourne.

```py
if response.status_code == 201
    response_data = response.content.decode('utf-8')
    cameras_data = json.loads(response_data
    cameras = []
    for camera in cameras_data
        cameras.append(Camera(camera[0],camera[1],camera[2],camera[3],camera[4],camera[5],camera[6])
    return True, cameras
else:
    return False, response
```

Du côté de la vue, je récupère unitquement les ip pour les afficher.

```py

def ask_camera_update(self):
    result, response = self.server_client.update_camera_list()
    print(response)
    
    cameras_ips = []
    if result:
        for camera in response:
            cameras_ips.append(str(camera.ip))
        if len(cameras_ips) < 1:
            Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'values', []))
                Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'text', self.TEXT_NO_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'disabled', True))
            else:
            Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'values', cameras_ips))
                Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'text', self.TEXT_CAMERA_FOUND))
                Clock.schedule_once(lambda dt: setattr(self.idscameras_spinner, 'disabled', False))
        
    self.ids.update_cameras_list_button.disabled = False
```

### Mise à jour des données des caméras

Quand les cameras sont trouvées sur le réseau, elles sont ajoutées dans la base sans leur positionX ni le mur où elle se trouvent. Par conséquent, je vais ajouter un endpoint permettant de les modifier.

#### 1.1 Rédaction de query sql (Serveur central : database_client.py)

J'ai crée cette query permettant de mettre à jour la positionX ainsi que l'id du mur en fonction de l'id de la camera et l'id du network.

```py
def updateCameraByIdCameraAndIdNetwork(self, idCamera, idNetwork, positionX, idWall):
    try:
        self.cursor.execute("UPDATE srs.Cameras SET positionX = %s, idWall = %s WHERE idCamera = %s AND idNetwork = %s", (positionX, idWall, idCamera, idNetwork,))
        self.dbConnexion.commit()
        return True, "Caméra mise à jour avec succès."
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la caméra : {e}")
        return False, f"Erreur lors de la mise à jour de la caméra : {e}"
```

#### 1.2 Création de la route (Serveur Central : app.py)

La route que je viens de créer va permettre de récupérer les paramètres et appeler la fonction dans ma classe `DatabaseClient`.

```py
self.app.add_url_rule('/update_camera', 'update_camera', self.update_camera, methods=['PUT'])

@JwtLibrary.API_token_required
def update_camera(self):
    idCamera = request.args.get('idCamera')
    idNetwork = request.args.get('idNetwork')
    positionX = request.args.get('positionX')
    idWall = request.args.get('idWall')

    if not idCamera or not idNetwork or not positionX or not idWall:
        return jsonify({'erreur': 'Paramètres manquants, veuillez fournir idCamera, idNetwork, positionX et idWall'}), 400

    result, message = self.db_client.updateCamera(idCamera, idNetwork, positionX, idWall)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'erreur': message}), 500
```

#### 1.3 Test avec Postman
Comme vous pouvez le voir, j'entre les données dans Postman et les modification sont prises en comptes dans la base.
![](./ressources/images/testpostmanupdatecamera.png)
![](./ressources/images/testpostmanupdatecameraresultdb.png)

### Conclusion
Lors de l'évaluation intermédiaire j'ai pu discuter sur différents points avec mes suiveurs. Dans l'absolut je suis sur la bonne route cependant, je dois absolument réaliser des tests fonctionnels et les mettre à jour régulièrement. De plus, je dois réaliser plus de commit. Pour conclure sur cette journée, j'ai l'impression d'avoir bien avancé. L'intégration de l'algorithmie a été interessante. Demain je vais continuer la mise à jour des caméras en espérant avoir terminé la matinée pour ensuite me concentrer sur les aspects manquants de ma documentation.

## 25.04.2024

#### Bilan de la veille
Hier était le jour de l'évalutation intermédiaire, j'ai bien pris note des conseils qui m'ont été apportés. Je dois réaliser un plan de test et être plus à jour sur mon git.

#### Planification du jour
Aujourd'hui je vais faire en sorte de travailler en parallèle sur le projet et sur mes cameras wifi. Je dois abosulment faire en sorte que les serveurs fonctionnent. Du côté du projet, je vais implémenter la modification des cameras. Si j'ai le temps ou si j'ai besoin de faire autre chose, je vais continuer ma maquette ou mettre à jour ma plannification effective.

### Installation des cameras

Je pensais avoir compris l'installation, cependant, vu l'environnement assez limitié au départ de mes cameras-wifi, il y a tout de même une liste assez importante de commandes à exécuter.

### Installation des dépendances necessaires

On commence par mettre à jour le système
```sh
sudo apt update
sudo apt upgrade
```

Créer l'environnement virtuel
```sh
python3 -m venv venv
```

Activer l'environnement virtuel
```sh
source venv/bin/activate
```

Ces librairies permettent de faire fonctionner la librairie [face-recognition](https://pypi.org/project/face-recognition/)

```sh
sudo apt install build-essential cmake
sudo apt install libopenblas-dev liblapack-dev libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libxine2-dev libtbb-dev libeigen3-dev libtesseract-dev
sudo apt install python3-dev python3-numpy python3-pip
```

Installation de la librairie [face-recognition](https://pypi.org/project/face-recognition/)

```sh
pip install face-recognition
```

### 1 : Affichage des données des caméras

Quand j'appelle le endpoint `cameras` ou `update_camera_list`, le serveur retourne une liste de camera. Cette liste est ensuite parsée en objets `Cameras`. Pour l'instant je n'affiche que les ip. Il faut que j'interprète le reste des données.

#### 1.1 : Mise à jour de l'objet Camera (application multiplateforme  : camera.py)

Afin de pour accèder aux données, je crée des getter setters sur toutes les varialbles d'instance.

```py
class Camera:
    def __init__(self, idCamera, ip, idNetwork, jwt, positionX, idWall, macAddress):
        self._idCamera = idCamera
        self._ip = ip
        self._idNetwork = idNetwork
        self._jwt = jwt
        self._positionX = positionX
        self._idWall = idWall
        self._macAddress = macAddress

    @property
    def idCamera(self):
        """Getter for the camera ID"""
        return self._idCamera

    @idCamera.setter
    def idCamera(self, value):
        """Setter for the camera ID"""
        self._idCamera = value

    @property
    def ip(self):
        """Getter for the IP address"""
        return self._ip

    @ip.setter
    def ip(self, new_ip):
        """Setter for the IP address"""
        # Add IP validation if necessary
        self._ip = new_ip

    @property
    def idNetwork(self):
        """Getter for the network ID"""
        return self._idNetwork

    @idNetwork.setter
    def idNetwork(self, value):
        """Setter for the network ID"""
        self._idNetwork = value

    @property
    def jwt(self):
        """Getter for the JWT token"""
        return self._jwt

    @jwt.setter
    def jwt(self, new_jwt):
        """Setter for the JWT token"""
        self._jwt = new_jwt

    @property
    def positionX(self):
        """Getter for the X position"""
        return self._positionX

    @positionX.setter
    def positionX(self, value):
        """Setter for the X position"""
        self._positionX = value

    @property
    def idWall(self):
        """Getter for the wall ID"""
        return self._idWall

    @idWall.setter
    def idWall(self, value):
        """Setter for the wall ID"""
        self._idWall = value

    @property
    def macAddress(self):
        """Getter for the MAC address"""
        return self._macAddress

    @macAddress.setter
    def macAddress(self, value):
        """Setter for the MAC address"""
        self._macAddress = value
```

#### 1.2 : Création de l'objet wall (application multiplateforme  : wall.py)

Afin de simplifier l'intégration de la table `ẁalls` je crée un objet wall.

```py
class Wall:
    def __init__(self, idWall, wallName):
        self._idWall = idWall
        self._wallName = wallName

    @property
    def idWall(self):
        """Getter for the wall ID"""
        return self._idWall

    @idWall.setter
    def idWall(self, value):
        """Setter for the wall ID"""
        self._idWall = value

    @property
    def wallName(self):
        """Getter for the wall name"""
        return self._wallName

    @wallName.setter
    def wallName(self, value):
        """Setter for the wall name"""
        self._wallName = value

```

#### 1.3 : Adaptation la récupération des mur (application multiplateforme  : server_client.py)

J'ai fais en sorte que lors de la récupération des murs, on crée dynamiquement l'objet.

```py
    def get_walls(self):
        """Récupérer la liste des murs depuis le serveur."""
        if not self.server_ip:
            return False, "IP du serveur manquante"
        
        params = {"token": self.API_token}
        endpoint_url = f"{self.server_url}/walls"
        response = requests.get(endpoint_url, params=params)
        
        if response.status_code == 200:
            walls_data = response.json()
            walls = [Wall(wall[0], wall[1]) for wall in walls_data]
            return True, walls
        else:
            return False, response.json()
```

#### 1.4 : Adaptation de la vue pour l'affichage des murs (application multiplateforme  : camera_management_window.py et app.kv)

Pour adapter le code à l'utilisation de l'objet wall, je stocke les noms de chaque mur dans la variable `wall_name` et attribue cette liste au spinner.

```py
def get_walls(self):
    result, response = self.server_client.get_walls()
    if result:
        self.walls = response
        wall_names = [wall.wallName for wall in self.walls]
        Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', wall_names))
    else:
        Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'values', []))
        Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'text', "Aucun mur trouvé"))
        Clock.schedule_once(lambda dt: setattr(self.ids.walls_spinner, 'disabled', True))
```

```
Spinner:
    id: walls_spinner
    text: "Select a Wall"
    values: root.get_wall_names()
    on_text: root.wall_changed(self.text)
```

Ensuite, je crée une fonction `wall_changed` qui est appelé lors d'un changement dans le spinner. Avec cela je crée une variable d'instance `selected_wall` permettant de savoir quel mur est séléctionnée.

```py
selected_wall = None

[...]

def wall_changed(self, wall_name):
    selected_wall = next((wall for wall in self.walls if wall.wallName == wall_name), None)
    if selected_wall:
        self.selected_wall = selected_wall
        print(f"Selected wall: {self.selected_wall.wallName}")
    else:
        self.selected_wall = None
        print("No wall matched the selection or no wall selected.")
```

#### 1.5 : Affichage de la position X (application multiplateforme : camera_management_window.py et app.kv)

Je crée une fonction qui permet de récupérer la propriété positionX de la camera actuelle séléctionnée.

```py
def get_selected_camera_positionX(self):
    if self.selected_camera:
        return self.selected_camera.positionX
    return 0
```

```
Slider:
    id: position_slider
    min: 0
    max: 100
    step: 1
    value: root.get_selected_camera_positionX()
    disabled: True
    orientation: 'horizontal'
```

### 2 : Mise à jour des données

#### 2.1 : Récupération des données (application multiplateforme : camera_management.py)

Je commence par récupérer les données depuis les différents inputs. Une fois cela fait, les données sont envoyé vers la fonction `update_camera` de la classe `server_client`.

```py
def update_camera(self):
    if self.selected_camera and self.selected_wall:
        idCamera = self.selected_camera.idCamera
        idNetwork = self.selected_camera.idNetwork
        positionX = self.ids.position_slider.value
        idWall = self.selected_wall.idWall
        result, response = self.server_client.update_camera(idCamera, idNetwork, positionX, idWall)
        if result:
            print("Camera updated successfully:", response)
        else:
            print("Failed to update camera:", response)
    else:
        print("No camera or wall selected. Please select both before updating.")
```

#### 2.2 Appel du endpoint (application multiplateforme : server_client)

Depuis le client du serveur, l'endpoint d'update est appelé. Les différentes données sont passés dans les paramètres puis l'endpoint est appelé.
```py

def update_camera(self, idCamera, idNetwork, positionX, idWall):
    if not self.server_ip:
        return False, "IP du serveur manquante"
    params = {
        "token": self.API_token,
        "idCamera": idCamera,
        "idNetwork": idNetwork,
        "positionX": positionX,
        "idWall": idWall
    }
    endpoint_url = f"{self.server_url}/update_camera"
    response = requests.put(endpoint_url, params=params)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()
```

#### 2.3 Résultat

##### Séléction d'une camera
En séléctionnant une des cameras dans le spinner, les données de cette dernière sont ajoutés dans le formulaire. On peut voir que les données correspondent à celles dans la base de données.

- Position relative au mur : 27
- Mur d'appartenance : West

![](./ressources/images/updateCamera1_app.png)  
![](./ressources/images/updateCamera1_bdd.png)

##### Pression du bouton de mise à jour

Une fois le bouton **Mettre à jour la camera** appuyé, les données sont envoyées dans la base.

- Position relative au mur : 70
- Mur d'appartenance : South

![](./ressources/images/updateCamera2_app.png)  
![](./ressources/images/updateCamera2_bdd.png)

### Conslusion

J'ai pu terminer mes objectifs fixés pour la journée. Le projet avance bien, il faut juste que je continue à mettre en place mes cameras pour enfin pourvoir effectuer mes tests. Demain, je vais continuer à mettre en place les serveur sur les cameras wifi, pendant l'installation, je vais faire le crud sur les utilisateurs.

## 26.04.2024

#### Bilan de la veille
Hier j'ai travaillé sur la mise à jour des camera en parallèle de la mise en place des cameras wifi restantes.

#### Planification du jour
Pour commencer sur la lancée de hier, je vais continuer à travailler sur la mise en place des serveurs des cameras wifi, cela sera ma priorité aujourd'hui. Pendant les téléchargements assez long je vais me concetrer sur des aspects moins urgents de mon application comme la suite du crud des utilisateurs.


### 1 : Installation des cameras

#### 1.1 : Installation par docker (machine puissante)

##### Mise à jour du système

```sh
sudo apt update
sudo apt upgrade -y
```

##### Creation du builder pour l'architecture du Raspberry Zero W 2

```sh
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```

##### Build l'image

```sh
docker buildx build --platform linux/arm64 -t face-recognition-app . --load
```

##### Envoi de l'exécutable vers la camera

```sh
docker save face-recognition-app | bzip2 | ssh pi@raspberrypi.local 'bunzip2 | docker load'
```

#### 1.2 : Installation sur le Raspberry

##### Installation de docker (Si besoin)

```py
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
echo "deb [arch=armhf] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install docker-ce
```

##### Démarrer l'image

```sh
docker run -p 4298:4298 face-recognition-app
```

### 2 : Modification / Suppression des données faciales

#### 2.1 : Création de la maquette

1. Un spinner permettant de choisir l'utilisateur à modifier.
2. Input affichant le nom de l'utilisateur.
3. Spinner de séléction de type de personnes.
4. Retour de la camera.
5. Bouton permettant de mettre en pause la video.
6. Bouton qui permet de mettre à jour l'utilisateur.
7. Bouton permettant de supprimer l'utilisateur.

![](./ressources/images/maquette_update_user.jpg)

#### 2.2 Création de la page

En suivant ma maquette j'ai crée une interface. J'ai fais en sorte de séparer la grid en 3 parties : 

1. Spinner utilisateur / text input nom / spinner types de personnes
2. Camera
3. Bouton pause / bouton modifier / bouton supprimer

L'objectif de cette approche et de laisser le plus de place à la camera.  Je n'ai pas pu intégrer la camera de suite car j'ai un petit problème lors du démarrage de l'application si je l'utilise deux fois. Je vais résoudre le problème plus tard lors de l'intégration.

##### Résultat

![](./ressources/images/updateUserInterface.png)

##### Code de l'interface (application multiplateforme : app.kv)

```
<UpdateUserWindow>:
    name: "updateUser"
    
    FloatLayout:
        GridLayout:
            cols: 3
            size_hint: 1, 0.1
            pos_hint: {'top': 1}

            Button:
                text: "<- Retour"
                on_release:
                    app.root.current = "navigationFaceManagement"
                    root.manager.transition.direction = "right"

            Label:
                text: "SRS : Modification d'utilisateurs"
                bold: True

            Image:
                source: 'Ressources/logo.png'
        
        GridLayout:
            cols: 1
            size_hint_y: 0.9

            GridLayout:
                cols: 1

                Spinner:
                    id: user_spinner
                    text: "Recherche d'utilisateurs en cours..."
                    disabled: True
                    on_text: root.user_changed(self.text)
                
                TextInput:
                    id: username_textInput
                    disabled: True
                    hint_text: "Nom de la personne"

                Spinner:
                    id: person_type_spinner
                    text: ""
                    disabled: True
            
            GridLayout:
                cols: 1

                Camera:
                    disabled: True
                    id: qrcam
                    resolution: (640, 480)
            
            GridLayout:
                cols: 1

                Button:
                    id: take_picture_button
                    text: "Prendre une photo"
                    disabled: True
                    on_release: root.take_picture()
                
                Button:
                    id: update_user_button
                    text: "Modifier l'utilisateur"
                    disabled: True
                    on_release: root.update_user()
                
                Button:
                    id: delete_user_button
                    text: "Supprimer l'utilisateur"
                    disabled: True
                    on_release: root.delete_user()
                    background_color: (1, 0, 0, 1)
                    background_normal: ''
```

#### 2.3 : Création de des routes (serveur central : app.py)

```py
self.app.add_url_rule('/update_user', 'update_user', self.update_user, methods=['PUT'])
self.app.add_url_rule('/delete_user', 'delete_user', self.delete_user, methods=['DELETE'])
```

Pour les données, elles sont passés dans le body à la place des paramètres pour des question de place.  

Une fois les données récupérée, elles sont passés dans une liste et envoyé vers le client de la base de données.

```py
@JwtLibrary.API_token_required
    def update_user(self):
        data = request.get_json()  # Automatically parses JSON data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        try:
            data = request.json
            user_id = data.get('idUser')
            new_username = data.get('username')
            new_idPersonType = data.get('idPersonType')
            new_encodings = data.get('encodings')

            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400

            update_data = {}
            if new_username:
                update_data['username'] = new_username
            if new_idPersonType:
                update_data['idPersonType'] = new_idPersonType
            if new_encodings:
                update_data['encodings'] = json.dumps(new_encodings)

            if not update_data:
                return jsonify({'error': 'No new data provided for update'}), 400

            result, message = self.db_client.updateUser(user_id, update_data)
            if result:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
```

```py
    @JwtLibrary.API_token_required
    def delete_user(self):
        try:
            user_id = request.args.get('idUser')
            if not user_id:
                return jsonify({'error': 'User ID is required'}), 400
    
            result, message = self.db_client.deleteUser(user_id)
            if result:
                return jsonify({'message': message}), 200
            else:
                return jsonify({'error': message}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
```

#### 2.4 : Query vers la bdd (serveur central : database_client.py)

Pour la suppression des données, je supprime l'utilisateur par l'id.

```py
def deleteUser(self, user_id):
    try:
        self.cursor.execute("DELETE FROM Users WHERE idUser = %s", (user_id,))
        self.dbConnexion.commit()
        return True, "User deleted successfully."
    except Exception as e:
        return False, str(e)

```

Pour la mise à jour, j'utilise les données passés en paramètres et je les attribue aux unitilisateurs par ID.

```py
def updateUser(self, user_id, update_data):
    update_parts = ", ".join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())
    values.append(user_id)
    try:
        self.cursor.execute(f"UPDATE Users SET {update_parts} WHERE idUser = %s", values)
        self.dbConnexion.commit()
        return True, "User updated successfully."
    except Exception as e:
        return False, str(e)
```

#### 2.6 : Résultats (Postman) 

##### Requête de mise à jour
![](./ressources/images/update_user_postman.png)

##### Requête de suppression
![](./ressources/images/delete_user_postman.png)

##### Résultat dans la bdd
Comme on peut voir sur le résulat final, l'utlisateur 4 a changé ses données alors que l'utilisateur 5 n'existe tout simplement plus.  
![](./ressources/images/delete_upadate_user_bdd.png)

### Conclusion

Je n'ai pas terminé la modification des utilisateurs, cependant j'ai bien avancé en utilisant les test postman. Ma journée a été rythmé par l'apprentissage de docker je n'ai donc pas pu avancé à ma vitesse souhaité. La semaine prochaine je vais essayer d'avoir une image docker prête déployée sur docker hub pour pouvoir mettre en place mes cameras.

## 29.04.2024

#### Bilan de la semaine dernière
La semaine dernière j'ai implémenté des concepts comme la recherche automatique de camera et leur mise à jour dans la base, le crud sur les camera ainsi que sur les utilisateurs. J'ai également appris comment utiliser docker mais j'ai pas réussi à build des images pour ARM depuis l'architecture de mon serveur.

#### Objectif de la journée
Aujourd'hui je vais commencer par développer un nouveau script pour les cameras wifi. Ensuite, je vais créer la page permettant d'afficher en temps réel la vue des cameras.

### 1.0 : Restructuration des cameras
Après longues réfléxion et tentatives, je n'ai pas réussi à faire fonctionner la librairie face-recognition sur mes raspberry une seconde fois, je n'arrive pas à trouver la sources des différentes erreur. Par conséquent j'ai décidé de passer la logique de la détéction faciale sur le serveur. Voici une liste des avantages et désavantages de cette méthode.

#### 1.1 : Avantages
1. Alègement de la logique sur les cameras.
2. Alègement des dépendances sur les cameras.
2. Possiblilité d'effectuer des algorithmes plus complexes
3. Tout cela sans compromettre la sécurité grâce à l'utilisation des JWT.

#### 1.2 : Désavantages
1. Logique et architecture plus complexe.
2. Suppression d'un partie du travail interessante incluant le multiprocessing.

#### 1.3 : Implémentation

Je débute par créer une route sur les cameras. Cette dernière envère une photo prise par la camera.

#### 1.4 : Problème lors de la récupération du flux

Après avoir fait un appel vers le endpoint `/video`, aucune image ne s'affiche et je me retrouve avec cette erreur.

```
[ WARN:1@17.308] global cap_v4l.cpp:997 open VIDEOIO(V4L2:/dev/video0): can't open camera by index
[ERROR:1@17.316] global obsensor_uvc_stream_channel.cpp:159 getStreamChannelGroup Camera index out of range
```

Cela veut simplement dire que la camera n'est pas indexée et donc pas accessible. Je commence à me dire que ça doit venir de la version de debian que j'utilise, peut-ête pas adapté. Les images que j'utilisait précédament et fonctionnaient était créés depuis le pi image version windows permettant de choisir le système où elles était déployés, assurant donc une compatibilité. Ce n'est pas le cas de la version Ubuntu. Je compare donc les version de debian en utilisant la commande `lsb_release -a`.

Version fonctionnelle :

```
Distributor ID:	Raspbian
Description:	Raspbian GNU/Linux 11 (bullseye)
Release:	11
Codename:	bullseye
```

Version (non) fonctionnelle :

```
Distributor ID:	Debian
Description:	Debian GNU/Linux 12 (bookworm)
Release:	12
Codename:	bookworm
```

#### 1.5 : Création du endpoint

L'endpoint `video` sert à récupérer le flux video en temps réel.

```py
@app.route('/video')
@token_required
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
```

La fonction `gen_frame()` prend une photo en utilisant la camera du serveur.
```py
def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
```

##### Résultat

Pour ce test, j'ai appelé l'endpoint depuis un navigateur. J'ai enlevé le décorateur au préalable. Le flux de la camera s'affiche en temps réel.

![](./ressources/images/endpointcamera.png)  

#### 1.6 : Problèmes lors de la récupération des flux
Pendant le poc j'ai eu l'occasion de récupérer le flux de mes camera depuis un client opencv. Le problème c'est que je n'ai pas réussi pour l'instant depuis mon application Kivy.  

```py
import cv2
import requests
import numpy as np

def main():
    # URL du serveur Flask
    server_url = 'http://192.168.1.131:4298/video?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNDQ3NjIyMH0.63zb0fjHPFmUtKttnOE3m2uqmQoQVDPm-2YFhZ7BFDY'

    # Réception du flux vidéo en continu
    response = requests.get(server_url, stream=True)

    if response.status_code == 200:
        bytes_stream = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            bytes_stream += chunk
            a = bytes_stream.find(b'\xff\xd8')
            b = bytes_stream.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_stream[a:b+2]
                bytes_stream = bytes_stream[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    else:
        print("Erreur lors de la récupération du flux vidéo")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
```

### Conclusion
Pour être honnête, aujourd'hui je ne suis pas réelement satisfait de mon travail. J'ai l'impression de bloquer sur un problème normalement simple. Demain je vais essayer d'autres façon de récupérer le flux. Peut-être modifier le serveur des camera me permettra de trouver une solution.

## 30.04.2024

#### Bilan de la veille
Hier, j'ai commencé à développer la page d'affichage des streams. J'ai renctré un problème lors de l'affichage avec Kivy. Cependant, j'ai tout de même réussi à faire fonctionner de façon fiable la récupération des caméras sur le réseau.

#### Objectifs de la jour
Aujourd'hui, j'ai décidé de créer un nouvel endpoint pour les camera appellé `/image` afin de récupérer une photo prise à l'instant, j'abandonne pas l'idée d'afficher le stream car c'est pratique pour la configuration etc.

### 1.0 : Récupération des images

Afin de récupérer les images, je vais en premier lieu, créer un endpoint adéquat, une fois cela fait, je vais effectuer un test avec postman et ensuite, je vais la récupérer dynamiquement dans la page que j'ai créé hier. 

#### 1.1 : Camera (app.py) : Endpoint de récupération d'image
L'endpoint `/image` prend une photo avec la camera, puis la retourne en réponse. J'ai pour l'instant enlevé le JWT pour le développement.

```py
@app.route('/image')
def image():
    """
    Route qui retourne une image capturée de la caméra.
    """
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()
    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    else:
        return jsonify({'message': 'Failed to capture image'}), 500
```

#### 1.2 : Test avec postman

Comme on peut le voir, l'image prise est envoyé dans le body.

![](./ressources/images/test_postman_image.png)

#### 1.3 : Récupération de l'image depuis le serveur central

Pour la récupération d'image j'ai décidé de procéder de la façon suivante :

1. Serveur central : Appel de l'endpoint `/image` grâce à l'id (transmit par l'application) de la camera et son JWT (récupéré dans la bdd).
2. Serveur central : Création de l'endpoint `/camera_picture`.
3. Application : Récupération des id des cameras grâce à l'objet camera.
4. Application : Appel de l'endpoint du serveur central.
5. Application : Affiche de l'image dans un élément `Image` en Kivy.

##### 1.3.1 : Serveur central (camera_server_client.py) : Appel de l'endpoint image des camera.

Avec la fonction `getCameraImage`, l'endpoint `image` des cameras est appelé avec le JWT ainsi que l'ip de la camera en paramètre. Si la réponse à la requête est 200, l'image est retournée. 

```py
@staticmethod
def getCameraImage(ip_camera, JWT):
    camera_url = f"http://{ip_camera}:{CameraServerClient.__CAMERAS_SERVER_PORT}/image?token={JWT}"
    try:
        response = requests.get(camera_url)
        if response.status_code == 200:
            return True, response.content
        else:
            return False, f"Échec de la récupération de l'image pour l'ip : {ip_camera}. Statut : {response.status_code}"
    except RequestException as e:
        return False, f"Erreur de connexion avec la caméra à l'ip : {ip_camera}. Détail de l'erreur : {str(e)}"
```

##### 1.3.2 : Serveur central (app.py) : Création du endpoint

Pour l'endpoint, je commence par la véfication du paramètre `idCamera`. Si ce dernier est présent, on recherche son JWT dans la base puis on appèle l'endpoint de la camera. Si une image est passé avec succès, l'image est encodée puis passé dans le body de la résponse.

```py
@JwtLibrary.API_token_required
def camera_picture(self):
    idCamera = request.args.get('idCamera')
    
    if not idCamera:
        return jsonify({'error': 'Camera ID is required'}), 400
    result, camera = self.db_client.getByIdCameras(idCamera)
    if camera:
        camera_ip = camera[1]
        camera_JWT = camera[3]
        result, response = CameraServerClient.getCameraImage(camera_ip, camera_JWT)
        if result:
            import base64
            image_base64 = base64.b64encode(response).decode('utf-8')
            return jsonify({'image': image_base64}), 200
        else:
            return jsonify({'error': response}), 401
    else:
        return jsonify({'error': 'Camera not found'}), 404
```

##### 1.3.3 : Postman : Test du endpoint

Si l'id de la camera est correcte, l'image est retournée, encodée en base64.

Par la suite, je vais effectuer les tests afin de vérifier les erreurs potentiels des utilisateurs, problèmes de serveur etc.
![](./ressources/images/test_postman_recupimage_srv.png)  

#### 1.4 : Récupération de l'image dans l'application

##### 1.4.1 : Application (server_client.py) : Appel de l'endpoint

```py
def get_image_by_camera(self, camera: Camera):
    endpoint_url = f"{self.server_url}/camera_picture?idCamera={camera.idCamera}"
    params = {
        'token': self.API_token
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        return True, response.json()['image']
    else:
        return False, response.json().get('error', 'Failed to retrieve the camera image')
```

##### 1.4.2 : Application (app.py) : Affichage de l'image

Pour l'instant je crée un objet en dur avec un id d'une camera qui est activée.

```py
def update_image(self, dt):
    camera = Camera(50, None, None, None, None, None, None)
    result, image_or_error = self.server_client.get_image_by_camera(camera)
    if result:
        self.display_image(image_or_error)
    else:
        print(f"Failed to retrieve image: {image_or_error}")
```

Dans la fonction `on_enter()`, cette fonction est appellée chaque 5 secondes.

```py
Clock.schedule_interval(self.update_image, 5)
```

##### 1.4.3 : Application (app.py) : Conversion de l'image

Afin d'afficher l'image dans un élément Image, il faut en premier lieu décoder l'image, puis la transformer en image pour ensuite en créer une texture qui elle est affichable.

```py
def display_image(self, image_base64):
    image_data = base64.b64decode(image_base64)
    image_stream = io.BytesIO(image_data)
    pil_image = Image.open(image_stream)
    pil_image = pil_image.convert('RGB')
    buf = pil_image.tobytes()
    img_texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
    img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
    self.image_one.texture = img_texture
```

##### 1.4.4 : Application (vue) : Résultat

![](./ressources/images/affichage_image.png)

##### 1.4.5 : Application (camera_streamer_window.py) : Gestion de l'affichage dynamique

J'ai voulu faire en sorte qu'on affiche les cameras en fonction de leur disponibilité.

je crée une fonction update_images qui aura comme rôle de mettre à jour les images des cameras. 
On commence par récupérer les caméras puis par vérifier le nombre de caméras présentes dans le réseau et adapter l'appel des methodes en fonction de cette donnée.

```py
def update_images(self, dt):
    result, cameras = self.server_client.get_cameras()
    if result:
        num_cameras = len(cameras)
        if num_cameras > 0:
            self.update_camera_image(cameras[0], self.ids.image_one)
        if num_cameras > 1:
            self.update_camera_image(cameras[1], self.ids.image_two)
        if num_cameras > 2:
            self.update_camera_image(cameras[2], self.ids.image_three)
        if num_cameras > 3:
            self.update_camera_image(cameras[3], self.ids.image_four)
```

Une fois cela fait, on crée je crée une seconde fonction `update_camera_image` qui met à jour l'élément de l'affichage en fonction de la camera qu'on lui attribue.

```py
def update_camera_image(self, camera, element):
    result, image_or_error = self.server_client.get_image_by_camera(camera)
    
    if result:
        element.texture = self.generate_texture(image_or_error)
    else:
        print("error retrieving image")
```

Et pour terminer, je crée j'adapte la fonction `display_image` à `generate_texture` qui génère la texture depuis une image en base 64.

```py
def generate_texture(self, image_base64):
    image_data = base64.b64decode(image_base64)
    image_stream = io.BytesIO(image_data)
    pil_image = Image.open(image_stream)
    pil_image = pil_image.convert('RGB')
    buf = pil_image.tobytes()
    img_texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
    img_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
    return img_texture
```

##### 1.4.6 : Application (vue) : Résultat

Dans cet exemple, le serveur trouve deux cameras sur le réseau. Leurs endpoint sont appelés et les photos sont affichées dans l'application.

![](./ressources/images/resultat_double_camera.png)


### Conclusion
J'ai l'impression d'avoir repris un bon rythme de travail. Après avoir effectué l'affciahge dynamique de la vue des cameras, j'ai commencé à développer la reconnaissance de silhouettes. Cependant, mon travail n'était pas suffisament avancé pour en faire mention dans le jdb. La prochaine fois, je vais développer une application de bureau me permettant de récupérer la position de personnes en temps réel. Une fois cela fait, j'implémenterai le code dans mon serveur.

## 02.05.2024

#### Bilan de la dernière fois
Mardi, j'ai terminé la récupération dynamique de la vue des cameras. J'ai également eu un problème avec un de [mes composants](https://www.pi-shop.ch/raspberry-pi-zero-kamera-kabel) qui a arrêté de fonctionné. J'ai demandé à Mr Garcia de passer une nouvelle commande.

#### Objectifs de la journée
Je vais commencer par la détection de personnes. Une fois cela fait, je vais l'intégrer au serveur. S'il me reste du temps ensuite, je vais commencer à développer la reconnaissance spaciale.

### 1.0 : Détection de personnes
Après avoir effectué quelques recherche je suis tombé sur [cet article](https://thedatafrog.com/en/articles/human-detection-video/) qui explique clairement comment fonctionne la détéction de personne et fournit également un code.

Après avoir testé le code, je suis assez scpetique. Logiquement le script fonctionne mieux quand la personne est loin vu que la camera peut prendre l'entièreté de la personne. 

![](./ressources/images/detection_de_personnes.png)

Afin que mon programme soit plus fiable, je recherche des façon pour pouvoir détecter le haut d'un corps.

#### 1.1 : MediaPipe Pose
Après avoir travaill sur `VisionPiano`, le projet en atelier décloisonné cet année. Je me suis dis que MediaPipe pouvait être une bonne solution. Et en effet, la personne présente sur l'image est traquée avec précision.  
Cependant, je me suis rendu compte un peu tard qu'il est impossible d'utiliser mediapipe pour détecter plusieurs personnes.

```py
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        positions = [landmark.x for landmark in results.pose_landmarks.landmark]
        avg_position = sum(positions) / len(positions)
        position_scale = int(avg_position * 100)
        
        cv2.putText(frame, f'Position: {position_scale}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('MediaPipe Pose', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

pose.close()
cap.release()
cv2.destroyAllWindows()

```

#### 1.2 : Pytorch - YOLOv5

La librairie YOLOv5 est utilisé pour la détéction d'objets. Le code ci-dessous permet de rechercher les personnes dans l'image puis de les afficher dans un cadre vert.

##### 1.2.1 : Code

```py
import cv2
import torch

# Charger le modèle pré-entraîné
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Fonction pour la détection dans un flux vidéo
def detect_people(frame):
    # Convertir l'image BGR de cv2 en RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Appliquer la détection
    results = model(frame_rgb)
    # Filtrer pour obtenir uniquement les détections de personnes
    results = results.pandas().xyxy[0]  # Résultats au format DataFrame
    people = results[results['name'] == 'person']
    return people

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)  # '0' est généralement l'indice de la première caméra

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détecter les personnes dans le cadre actuel
        detections = detect_people(frame)

        # Dessiner les boîtes englobantes sur l'image
        for index, row in detections.iterrows():
            cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 255, 0), 2)

        # Afficher l'image
        cv2.imshow('Detected People', frame)

        # Arrêter le flux en appuyant sur 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
```

##### 1.2.1 : Exemple

Comme vous pouvez le voir le système est très efficace, il affiche même mon collègue alors que ce dernier est assis sur une chaise et n'est presque pas visible.

![](./ressources/images/yolo5_test.png)

#### 1.3 : Implémentation dans l'API

##### 1.3.1 : Création de la classe SpaceRecognition (Serveur : space_recognition.py)

En premier lieu, je dois faire en sorte que ce soit l'image récupérée par les cameras soit passé dans l'algorithme. Pour cela je crée une nouvelle classe `SpaceRecognition`.

```py
import cv2
import torch
import numpy as np

class SpaceRecognition:

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    
    def _detect_people(self, image):
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(frame_rgb)
        results = results.pandas().xyxy[0]
        people = results[results['name'] == 'person']
        return people


    def get_people_positions_x(self, imageBase64):
        nparr = np.frombuffer(imageBase64, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detections = self._detect_people(image)
```

Une fois cette partie fonctionnelle, il faut que je récupère la position x des personnes dans l'image. Je complète la fonction `get_people_positions_x` en conséquence.

1. Récupération des détections 
2. Pour chaque personne trouvée
    - Récupération du milieu de la personne.
    - Récupération de la largeur de l'image
    - Normalisation de la position pour correspondre au reste du projet (0 à 100)
    - Ajout de la personne dans la liste


```py
def get_people_positions_x(self, imageBase64):
    nparr = np.frombuffer(imageBase64, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    detections = self._detect_people(image)
    people_positions = []
    for index, row in detections.iterrows():
        x_center = (row['xmin'] + row['xmax']) / 2
        width = image.shape[1]
        normalized_x_position = (x_center / width) * 100
        people_positions.append(normalized_x_position)
    return people_positions
```

##### 1.3.2 : Adaptation de la route (Serveur : app.py)

Et pour terminer, j'adapte ma route afin de pouvoir retourner les données dans le endpoint.

```py
@JwtLibrary.API_token_required
def space_recognition(self):
    idNetwork = request.args.get('idNetwork')
    if not idNetwork:
        return jsonify({'error': 'Network ID is required'}), 400
    response = []
    result, response = self.db_client.getCamerasByIdNetwork(idNetwork)
    if not result:
        return jsonify({'error': 'Camera not found'}), 404
    cameras = []
    for data in response:
        camera = Camera(data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, None)
        resultImg, responseImg = CameraServerClient.getCameraImage(camera.ip, camera.jwt)
        if resultImg:
            space_recongition = SpaceRecognition()
            positions_x = space_recongition.get_people_positions_x(responseImg) # Ajouté
            camera.persons_position = positions_x # Ajouté
            cameras.append(camera)
        else:
            return jsonify({'error': responseImg}), 401
    cameras_info = [{'id': cam.idCamera, 'persons_position': cam.persons_position} for cam in cameras]
    return jsonify(cameras_info), 200
```

##### 1.3.2 : Test (Postman)

Quand je fais l'appel vers le endpoint je reçois les position des personnes captés par les camera. Pour l'instant, j'ai que 2 caméras, j'attends la commande que j'ai passé avec mr Garcia pour la suite.

![](./ressources/images/postman_yolo.png)

### Conclusion

Je suis en capacité de commencer le développment de la reconnaissance spaciale. Cependant, je dois impérativement avoir mes caméras disponibles. La prochaine fois je vais mettre en place les autres caméras.

## 03.05.2024

#### Bilan de la veille
Hier j'ai terminé la détection de personnes. J'ai effectué des recherches afin de trouver la meilleure technologie possible dans mon cas de figure.

#### Objectifs de la journée
Je pense avoir bien avancé dans mon travail technique, à présent, je dois me concentrer sur le rendu de la semaine prochaine. Pour ce faire, je dois avancer la documentation, faire des diagrammes, l'analyse organique, les tests etc.

### Diagramme

En utilisant Draw.io, j'ai crée le diagramme complet du projet.

![](./ressources/images/srs_diagramme_complet.jpg)

### Poster

J'ai voulu créer quelque chose dans la charte graphique sérieuse de mon travail, quelque chose qui écoque la sécurité. J'ai envoyé cette première version à mes suiveurs.

![](./ressources/poster/poster_srs_v1.1.png)

### Conclusion

J'ai pu avancer sur la documentation. J'ai rédigé les tests fonctionnels en adéquation avec les avancées que j'ai fais fais chaque semaine. J'ai égalment fait le diagramme général du projet et la première verion du poster.

## 06.05.2024

Absent

## 07.05.2024

#### Bilan de la dernière fois
J'ai terminé la semaine dernière par la documentation, j'ai fais le poster et j'ai commencé l'analyse fonctionelle.

#### Objectif de la journée
Aujourd'hui je vais commencer par modifier le poster afin de suivre les conseils de Monsieur Zanardi et Monsieur Jayr.

### 1.0 : Modification du poster
Pour résumer, je dois mettre en application les conseils suivants :
- Utiliser des mots clés
- Remplacer la description par une séquence qui décrit mon application.
- Bouger le texte "Travail de diplôme" en bas de la page.
- Mettre la phrase d'accroche en dessous du titre.

#### 1.1 : Version 1.3 du poster
![](./ressources/poster/poster_srs_1.3.png
)

### 2.0 : Suite du travail sur la doc
En vue de l'évaluation intermédiaire, je dois continuer mon travail sur la documentation de mon projet.

#### 2.1 : Diagramme de l'application
Afin d'aider à la compréhension de l'architecture de l'application. J'ai crée un diagramme.

![](./ressources/diagrams/application.jpg)

#### 2.2 : Diagrammes de séquences
Pour faire les diagrammes de séquence j'utilise [PlantUML](https://plantuml.com/fr/). La plus value par rapport à draw.io c'est la vitesse et vu le nombre de diagrammes que je vais devoir effectué c'est bienvenu.

### Conclusion
Aujourd'hui j'ai bien avancé la documentaiton, j'ai appris une nouvelle technologie avec PlantUML et j'ai pu discuter avec Monsieur Zanardi par rapport à la structure. Maintenant que j'ai toutes les clés en main je dois donner mon maximum demain pour essayer de terminer.

## 08.05.2024

#### Résumé de la veille
Hier j'ai travaillé sur les diagrammes de séquences et terminé le poster. Grâce à l'utilisation de plantUML j'ai réussi à être plus efficace.

#### Objectif de la journée
Je vais commencer par créer mon abstract, en effet, il faut que je le rende ce soir à 17h. Ensuite, je vais continuer la documentation. Avec les conseils apportés hier par monsieur Zanardi, je connais la structure que je dois faire.

### 1.0 : Abstract
Je dois commencer par me renseigner qu'est-ce qu'un abstract en informatique.
Je n'ai pas trouvé d'informations sur internet alors en recherchant dans les rapports des années précédentes, l'abstract s'avère être une sorte de résumé du projet.

- [Abstract](./abstract.md)

J'ai pu demander à monsieur Jayr des détails supplémentaires, pour m'aider, il va nous envoyer des exemples.

En faisant la rédaction de l'abstract, je me suis rendu compte qu'il serait meilleur de placer les caméras dans les coins des pièces. Je garde cette information pour le développement la semaine prochaine.

### Conclusion
Pas grand chose à dire pour cette conclusion, j'ai terminé l'abstract et j'ai bien avancé les diagrammes de séquence. Je pense être dans les temps pour rendre la documentation lundi.

## 13.05.2024

#### Bilan de la semaine dernière
La semaine dernière je me suis exclusivement conscentré sur la documentation en vue du rendu qui est plannifié aujourd'hui.

#### Objectif de la journée
Aujourd'hui, je vais commencer par trouver une façon de générer un pdf à partir de ma documentaiton. Une fois cela terminé, je vais commencer à développer le support en 3D pour mes caméras.

### 1.0 : Documentation en PDF

Je recherche la meilleure façon de générer automatiquement ma documentation pour le rendu.

#### 1.1 : Pandoc et Xelatex

Pour commencer j'ai recherche les solutions en ligne et je suis tombé sur Pandoc. Après avoir généré un fichier je peux affirmer que ça focntionne bien cependant, ça ne correspond pas à ce que je recherche. En effet j'ai pas trouvé de façon pour que ça fonctionne avec tous les fichier dans un dossier pour avoir des liens relatifs avec une eventuelle table des matières etc.

#### 1.2 : MkDocs material

J'ai décidé de passer ma documentation dans un serveur [mkdocs](https://pypi.org/project/mkdocs/) avec le thème [material](https://squidfunk.github.io/mkdocs-material/). J'ai ensuite ajouté le plugin [mkdocs-with-pdf](https://pypi.org/project/mkdocs-with-pdf/). Avec cette configuration, j'ai réussi à avoir un résultat satisfaisant.

### 2.0 : Impression 3D des supports pour les caméras

Mon objectif est d'avoir au moins un support pour la soirée poster de demain. Pour ce faire je vais demander à un camarade, ayant de l'expériance en 3D pour m'aider à modélier mon support. Pour les mesures des différents composants, je me suis renseigné sur les sites suivants :

1. [Raspberry Zero 2 W (65mm x 30mm)](https://core-electronics.com.au/raspberry-pi-zero-2-w-wireless.html)
2. [Raspberry Pi Camera 2.1 (25mm x 23mm x 9mm)](https://uk.pi-supply.com/products/raspberry-pi-camera-board-v2-1-8mp-1080p)
3. [MediaRange MR745 (21mm x 21mm x 90mm)](https://www.digitec.ch/en/s1/product/mediarange-mr745-2600-mah-962-wh-powerbanks-15660520)

Pour l'impression en elle même, j'utilise le logiciel [Ultimaker Cura](https://ultimaker.com/fr/software/ultimaker-cura/) qui me permet de générer un fichier au format [G-code](https://fr.wikipedia.org/wiki/Programmation_de_commande_num%C3%A9rique) que je passe à l'imprimante 3D via une carte microSD.

- Modèle de l'imprimante 3D : [Creality CR 20 Pro](https://www.digitec.ch/en/s1/product/creality-cr-20-pro-3d-printers-11547283)


#### 2.1 : Version 0.1

Avec les données que j'ai récolté, j'ai été en mesure d'imprimer une première version.

Pour la taille des composants, j'ai décidé de viser un peu large volontairement. L'impression s'est bien passée cependant il y a plusieurs axes d'amélioration.

1. La camera ne rentre pas dans son réceptacle, il faut reculer le support.
2. L'avant de la batterie est exposé, il serait meilleur fermé.
3. Ajouter les lettres **SRS** sur le côté.

![](./ressources/images/support-v0.1a.jpg)

![](./ressources/images/support-v0.1b.jpg)

#### 2.2 : Version 0.2

On a effectué les ajustements et avec les modifications nous avons effectué une seconde version.

Les améliorations sont visible et le support fonctionne bien pour une version en développement. Cependant, certaines améliorations sont toujours possibles.

1. Viser la camera ainsi que le Raspberry sur le support directement.
2. Trouver une façon de fixer la batterie de façon plus professionnelle.
3. Fermer le support sur le haut pour protéger le Raspberry.

![](./ressources/images/support-v0.2a.jpg)
![](./ressources/images/support-v0.2b.jpg)
![](./ressources/images/support-v0.2c.jpg)
![](./ressources/images/support-v0.1d.jpg)

### Conslusion
Aujourd'hui j'ai réussi à avoir un support assez satisfaisant pour la suite de mon développement. J'ai effectué également mon rendu intermédiaire, demain je vais effectuer mon auto-évaluation.

## 14.05.2024

#### Bilan de la veille
Hier je me suis conctré sur l'achèvement de mon rendu intermédiaire, une fois cela terminé, j'ai développé deux version de mon support pour les caméras.

#### Objectifs de la journée
Aujourd'hui, je vais commencer par effectuer mon auto-évaluation. Ensuite je vais me concentrer sur la préparation de la soirée poster en effectuant un prototype de mon projet.


### 1.0 : Auto-évaluation

#### Prestation professionnelle
**Qualité du travail : travail très soigné** Selon moi, mon travail est suffisament clair grâce aux diagrammes de séquences et aux user story que je mets en place avant le développement.  

**Organisation du travail : normale et sensée** La documentation est pour l'instant mon point faible, j'ai appris comment rédiger des diagrammes de séquence de façon plus efficace mais il fallait que j'y sois contraint. Je pense que si je redouble d'ôrganisation que ferais du meilleur travail à ce niveau là.

**Rythme de travail : rapide** Je pense toujours que j'avance à une bonne cadence malgrès quelques difficultés lié à Kivy et OpenCV.

**Squelette documentation : bien avancé** Je pense avoir enfin trouvé une structure qui fonctionne bien. Avec les séquences dans l'analyse organique qui expliquent de façon efficace le fonctionnement des différentes technologies. Cependant, il faut que je trouve une façon efficace de faire des diagramme en python.

**Ordre des dossiers fichiers: examplaire** Pas grand chose à dire, je pense que mon projet est clair.

#### Comportement au travail
**Engagement et persévérence : appliqué, persévérant** Je pense avoir prouvé à plusieurs reprise que les problème de compatibilité pouvait être contournés avec suffisament de motivation, par exemple, la compatibilité de openCV en Kivy.

**Intérêt : très interessé** Toujours le même niveau de motivation depuis la dernière fois.

**Autonomie : totalement indépendant** Je suis toujours d'avis que je n'ai pas spécialement besoin d'aide à l'organisation de mon projet. Quand j'ai un problème je le signale etc.

**Capacité à comprendre : comprend vite et bien** Selon moi, je pense assimilier assez vite les principe fondamontaux de mon projet, je comprends de mieux en mieux les différentes technologies de mon projet.

**Mise à jour des outils de partage : très régulier** J'ai fais un effort à ce niveau là depuis la dernière fois, j'essaye de push à chaque fonctionnalité que j'implémente.

#### Attitude personnelle

**Collaboration : Très bonne, caractère sociable** Pas de changement à ce niveau là.

**Façon d'être : préveant et serviable** Je pense avoir toujours la même attitude.

**Conscience professionnelle : respecte les consignes** Quand on me demande quelque chose je pense toujours répondre de façon professionnelle.

**Réponse aux communications : rapide** Quand un mail est envoyé, je vais mon possible pour répondre dans mes meilleurs délais

#### Conclusion
Je pense m'être amélioré sur plusieurs points qui me faisait défault lors de la première évaluation, je dois cependant toujours fais un effort pour mon organisation de travail.

### 2.0 : Création du prototype
Pour avoir un prototype fonctionnel à montrer aux différents invités, je intéger les éléments suivants :

1. Récupération du flux de la camera.
2. Affichage des carrés autour des personnes.
3. Affichage de la position des personnes sur l'axe x.

Pour rendre cela plus compréhensible, je vais faire un graphique que je vais imprimer pour m'aider lors de mes explications.

#### 2.1 : Graphique

Dans ce graphique, on voir la position de l'utilisateur sur la vue des différentes caméras.

![](./ressources/images/demo.jpg)

#### 2.2 : Implémentation

Pour des question de simplicité, j'ai décidé de mettre le token et l'ip de la caméra en dûr.

```py
# URL du serveur Flask
server_url = 'http://192.168.1.131:4298'
video_url = f'{server_url}/video'

# Token JWT
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNTc1NTQ0Mn0.W-WjTXrWXsigBKmPhrsXx7GV2JIgUmW1At1chwbyIyk'

# Headers pour l'authentification
params = {'token': token}
```


En utilisant la librairie YoloV5, je récupère la position des personnes dans la frame.

```py
# Chargement du modèle pré entrainé
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_people(frame):
    '''
    Détecte les personnes dans une image

    Params:
        frame : Image où les personnes sont recherchées
    '''
    # Convertir l'image BGR de cv2 en RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Appliquer la détection
    results = model(frame_rgb)
    # Filtrer pour obtenir uniquement les détections de personnes
    results = results.pandas().xyxy[0]  # Résultats au format DataFrame
    people = results[results['name'] == 'person']
    return people
```

Pour la récupération des données des caméras, j'utilise la fonciton que j'ai crée lors du POC. J'inversé égalment l'image pour correspondre au support.

```py
# Fonction pour récupérer le flux vidéo du serveur Flask
def get_video_stream(url, params):
    video_response = requests.get(url, params=params, stream=True)
    if video_response.status_code == 200:
        bytes_data = b''
        for chunk in video_response.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    img = cv2.flip(img, 0)
                    yield img
    else:
        raise Exception(f"Failed to get video feed. Status code: {video_response.status_code}")
```

Affichage des résultats et détermination de position x.

```py
for frame in get_video_stream(video_url, params):
# Détecter les personnes dans le cadre actuel
detections = detect_people(frame)
# Créer une nouvelle image pour afficher les positions x
position_map = np.zeros((100, 500, 3), dtype=np.uint8)

for index, row in detections.iterrows():
    cv2.rectangle(frame, (int(row['xmin']), int(row['ymin'])), (int(row['xmax']), int(row['ymax'])), (0, 255, 0), 2)
    # Calculer la position x approximative de la personne
    center_x = int((row['xmin'] + row['xmax']) / 2)
    # Convertir les coordonnées de l'image en coordonnées de la carte
    map_x = int(center_x / frame.shape[1] * position_map.shape[1])
    # Dessine la position sur la carte
    cv2.circle(position_map, (map_x, position_map.shape[0] // 2), 5, (0, 255, 0), -1)
# Afficher l'image avec les détections
cv2.imshow('Detected People', frame)
# Afficher la carte des positions x
cv2.imshow('People Position Map', position_map)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

#### 2.3 : Résultat

On peut voir que les personnes dans l'image sont détectés et des rectangles verts les englobent. Sur l'application de droite on voit leurs position x.

![](./ressources/images/demo-application.png)