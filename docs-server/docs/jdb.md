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

![](./ressources/images/support-v0.2a.jpg){: style="max-height:200px;"}


![](./ressources/images/support-v0.2b.jpg){: style="max-height:200px;"}

![](./ressources/images/support-v0.2c.jpg){: style="max-height:200px;"}

![](./ressources/images/support-v0.1d.jpg){: style="max-height:200px;"}


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

### Conclusion
Bien que aujourd'hui j'ai pas avancé mon projet en lui même, la démo que j'ai conçu m'a permis de me questionner sur l'implémentation de la reconnaissance spatiale. Je me demande si mon modèle sera suffisament précis.

## 15.05.2024

#### Bilan de la veille
Hier a eu lieu la soirée poster, expliquer à des personnes le principe de mon projet a été une tâche interessante. Cela m'a fait réfléchir sur l'architecture de ma reconnaissance spaciale.

#### Objectif de la journée 
Je vais explorer une autre façon d'aborder le projet. Je vais essayer de faire de la détection de profondeur.

### 1.0 : Détection de profondeur

Pour comprendre comment implémenter la détection de profondeur en Python, j'ai suivi un tutoriel sur Youtube.

- [**Depth Estimation with OpenCV Python for 3D Object Detection - Nicolai Nielsen**](https://www.youtube.com/watch?v=uKDAVcSaNZA&list=PLCpB2LmtGbuel31gdKHSV_HBaZa2guc6Y&index=4)

#### 1.1 : Calibration

La calibration me sert à elever la distortion dans l'image.

##### 1.1.1 : Prise de photo (get_images.py)

Je commence par prendre une dizaine de photo par camera afin d'avoir des échantillons pour la calibration. J'ai du adapter le code du script du cours afin d'appeler mes caméras.

1. Pause de 3 seconde afin de pouvoir se mettre en place avec l'échiquier.
2. Récupération des images, appel des deux caméras en simultanné.
3. Attente de une seconde entre chaque prise.
4. Stockage des résultat dans leur dossier correspondant.

```py
import cv2
import requests
import numpy as np
import time
import os

time.sleep(3)
# Créer des répertoires pour sauvegarder les images récupérées
os.makedirs('./stereoLeft', exist_ok=True)
os.makedirs('./stereoRight', exist_ok=True)

# URLs des serveurs Flask pour récupérer les images de calibration
image_urls = ['http://192.168.1.131:4298/image', 'http://192.168.1.26:4298/image']

# Token JWT
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiU1JTLVNlcnZlciIsImV4cCI6MTcxNTg1MDEwMn0.pJPpg97CWWcaY0HKNb6jgv7lGuZIwbmn6__yBQOLf84'


# Headers pour l'authentification
params = {'token': token}

def get_calibration_images(urls, params, num_images=10):
    for j in range(num_images):
        images = []
        for i, url in enumerate(urls):
            response = requests.get(url, params=params)
            if response.status_code == 200:
                img_array = np.frombuffer(response.content, np.uint8)
                img = cv2.flip(cv2.imdecode(img_array, cv2.IMREAD_COLOR), 0)
                if img is not None:
                    images.append((i, img))
            else:
                print(f"Failed to get image from {url}. Status code: {response.status_code}")
                continue

        if len(images) == len(urls):
            for i, img in images:
                # Sauvegarder l'image dans le dossier correspondant
                if i == 0:
                    image_path = f'./stereoLeft/imageL{j+1}.jpg'
                else:
                    image_path = f'./stereoRight/imageR{j+1}.jpg'
                cv2.imwrite(image_path, img)
                print(f"Saved image to {image_path}")

        # Attendre une seconde avant la prochaine capture
        time.sleep(1)

# Appel de la fonction pour récupérer et enregistrer les images
get_calibration_images(image_urls, params)
```

##### 1.1.2 : Calibration des caméras (calibration_images.py)

Ce script permet de détecter les coins de l'échiquier, calibrer les cameras afin d'effectuer une calibration stereo pour corriger les distorsions et aligner les images pour la vision stereo.

1. **Importations nécessaires** :
    ```python
    import numpy as np
    import cv2 as cv
    import glob
    ```

2. **Définition de la taille du damier et de la taille du cadre de l'image** :
    ```python
    chessboardSize = (10, 6)
    frameSize = (640, 480)
    ```

3. **Critères de terminaison pour l'algorithme de `cornerSubPix`** :
    ```python
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ```

4. **Préparation des points d'objets dans le monde réel pour le damier (3D)** :
    ```python
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)
    size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm
    ```

5. **Initialisations des listes pour stocker les points d'objets et les points d'images** :
    ```python
    objpoints = []  # Points 3D dans l'espace réel
    imgpointsL = []  # Points 2D dans le plan de l'image de la caméra gauche
    imgpointsR = []  # Points 2D dans le plan de l'image de la caméra droite
    ```

6. **Chargement des images de répertoires** :
    ```python
    imagesLeft = glob.glob('stereoLeft/*.jpg')
    imagesRight = glob.glob('stereoRight/*.jpg')
    print(f"Found {len(imagesLeft)} images on the left and {len(imagesRight)} images on the right.")
    ```

7. **Boucle sur chaque paire d'images** :
    ```python
    for imgLeft, imgRight in zip(imagesLeft, imagesRight):
        imgL = cv.imread(imgLeft)
        imgR = cv.imread(imgRight)
        if imgL is None or imgR is None:
            print(f"Failed to load images {imgLeft} or {imgRight}")
            continue
    ```

8. **Convertion des images en niveaux de gris et égaliser l'histogramme pour améliorer le contraste** :
    ```python
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayL = cv.equalizeHist(grayL)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    grayR = cv.equalizeHist(grayR)
    ```

9. **Détection des coins de l'echiquier** :
    ```python
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK)
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK)
    ```

10. **Affichage des résultats de la détection des coins** :
    ```python
    print(f"Chessboard detected in image {imgLeft}: {retL}")
    print(f"Chessboard detected in image {imgRight}: {retR}")
    ```

11. **Affinage les coins et les dessiner sur les images** :
    ```python
    if retL:
        cornersL = cv.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
    else:
        print(f"Chessboard corners not found in {imgLeft}")

    if retR:
        cornersR = cv.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
    else:
        print(f"Chessboard corners not found in {imgRight}")
    ```

12. **Affichage des images avec les coins détectés** :
    ```python
    cv.imshow('img left', imgL)
    cv.imshow('img right', imgR)
    cv.waitKey(1000)
    ```

13. **Ajout des points d'objet et des points d'image aux listes si les coins sont trouvés** :
    ```python
    if retL and retR:
        print(f"Adding object points and image points for {imgLeft} and {imgRight}")
        objpoints.append(objp)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)
    ```

14. **Fermer les fenêtres d'affichage** :
    ```python
    cv.destroyAllWindows()
    ```

15. **Calibration des caméras gauche et droite si des points d'objet et d'image sont trouvés** :
    ```python
    if objpoints and imgpointsL:
        retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
        heightL, widthL, channelsL = imgL.shape
        newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

        retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
        heightR, widthR, channelsR = imgR.shape
        newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))
    ```

16. **Calibration stéréo en fixant les paramètres intrinsèques des caméras** :
    ```python
    flags = 0
    flags |= cv.CALIB_FIX_INTRINSIC
    criteria_stereo = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)
    ```

17. **Rectification stéréo pour obtenir les matrices de projection et les cartes de rectification** :
    ```python
    rectifyScale = 1
    rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale, (0, 0))
    stereoMapL_x, stereoMapL_y = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_32FC1)
    stereoMapR_x, stereoMapR_y = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_32FC1)
    ```

18. **Sauvegarde des paramètres de rectification stéréo** :
    ```python
    print("Saving parameters!")
    cv_file = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)
    cv_file.write('stereoMapL_x', stereoMapL_x)
    cv_file.write('stereoMapL_y', stereoMapL_y)
    cv_file.write('stereoMapR_x', stereoMapR_x)
    cv_file.write('stereoMapR_y', stereoMapR_y)
    cv_file.release()
    ```

19. **Message d'erreur si aucun point n'est trouvé** :
    ```python
    else:
        print("No object points or image points found. Calibration not performed.")
    ```

###### Résultat :

Sur la video ci-dessous, on peut voir la vue de la camera de droite, quand l'echiquier est détecter, on voir les différentes lignes pour la calibration apparaître.

![camera calibration gif](./ressources/videos/camera_calibration.gif)

### 2.0 : Evaluation intermédaire

Mes suiveurs on pu faire leurs retours sur le travail que j'ai effectué jusqu'à présent. J'ai relevé des points positifs et des points à améliorer

#### Positif

1. User stories.
2. Diagrammes de séquence.
3. Quantité de travail.
4. Documentaiton en séquences.
5. Tests unitaires avec Postman.

#### À amélorer

1. Abstract trop technique.
2. Meilleur résumé du projet.
3. Analyse de l'existant à ajouter.
4. Diagrammes de classe.
    - Utiliser [PlantUML](https://plantuml.com/fr/) sur les fichier individuellement pour éviter les problèmes de compatibilité avec Kivy.
5. Tests unitaires en Python.
    - Monsieur Zanardi a insisté sur le fait qu'il n'était pas obligatoire d'en avoir une grande quantité, mais montrer qu'on sait le faire constiturait une plus-value au-près des experts.
    - Librairie conseillée : [PyTest](https://docs.pytest.org/en/8.2.x/)
    - Je pense m'en servir pour le serveur central. Selon moi c'est l'endroit le plus interessant au niveau des tests.

### Conslusion

Selon mes suiveurs, mon travail se déroule bien et je dois continuer sur cette voie. Personnellement, je sens qu'il faut que j'accelère mon rythme, il faut absolument avoir un livrable interessant pour les experts.

## 16.05.2024

#### Bilan de la veille
Hier j'ai commencé la vision stereo avec mes deux caméras, j'ai également fait l'évaluation intermédiaire avec mes suiveurs qui s'est bien passé dans l'ensemble.

#### Objectif de la journée
Pour commencer, je vais déterminer la meilleure façon d'effectuer la reconnaissance spatiale. Ensuite, je vais explorer la piste et effectuer un prototype.

### 1.0 : Recherche de la meilleure façon de faire la reconnaissance spatiale

Après la discussion de hier avec Monsieur Zanardi, on en a conclut que la meilleure serait de mettre les caméras le coins des murs.

### 2.0 : Calcul de la position

J'ai décidé d'effectuer la triangulation *from scratch*. Pour commencer, j'ai crée une permettant de récupérer l'angle des utilisateurs.

```py
def draw_angles(frame, positions, fov):
    height, width, _ = frame.shape
    for (cx, cy) in positions:
        # Calculer l'angle par rapport au centre de la caméra
        angle = ((cx - width / 2) / (width / 2)) * (fov / 2)
        cv2.putText(frame, f"Angle: {angle:.2f}", (int(cx), int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return frame
```

#### 2.1 : Trigonometrie

Afin de connaîte la position de la personne dans l'espace, j'utilise plusieurs principes trigonométriques.

Voici les calculs dans leurs totalité, veuillez continuer pour voir les détails des étapes.

![](./ressources/images/calcul_position.jpg.jpg)

##### Variables

- C (distance entre les deux caméras) : 3m
- ɑ (angle de la camera de droite vers l'objet) : 10°
- β (angle de la camera de gauche vers l'objet) : -12°

##### Recherche des données du triangle (Camera - Personne - Camera)

Je commence par trouver les angles en appliquant le principe suivant :

l'angle ɑ représente l'angle de la personne par rapport au milieur de l'angle de vue de la camera qui est pointé vers le milieu de la pièce. 

L'angle ɑ₁ représente l'angle entre le mur et la personne.

$ɑ₁ = \frac{90}{2} + \alpha$

![angle de camera](./ressources/images/angle_camera.jpg)

Pour trouver le dernier angle de la personne vis à vis des caméras, il suffit de complèter les angles du triangle.

ϑ₁ = 180 - $ɑ₁ - β₁

![](./ressources/images/triangle_camera_personne.jpg)


##### Recherche de la distance camera - personne

En utilisant le théorème du sinus, on recherche la distance camera -> personne.

$ \frac{a}{\sin(\alpha)} = \frac{b}{\sin(\beta)} = \frac{c}{\sin(\gamma)} $

$a = \frac{c}{\sin(\gamma)} * \sin(\alpha)$

![](./ressources/images/distance_camera_personne.jpg)

##### Recherche de la position Y

À présent, nous avons un triangle rectangle, par conséquent on peut utiliser la trigonométrie.

$$
\sin(\alpha) = \frac{\text{opp}}{\text{hyp}}
$$


$\sin(\alpha ₁) = \frac{y}{a₁}$  

$\sin(\alpha ₁) *  a₁ = y$  

![](./ressources/images/recherche_position_y.jpg)

##### Recherche de la position X

Avec les données que nous avons récoltés, il suffit à présent d'effectuer un théorème de pythagore pour trouver la position x.

$c^2 = a^2 + b^2$

$a^2 = c^2 - b^2$

$a = \sqrt{c^2 - b^2}$

![](./ressources/images/calcul_position_x.jpg)

##### 2.2 Implémentation

Après le modèle effectué, j'ai implémenté dans la classe `Triangulation` mes calculs

```py
import math

class Triangulation:

    @staticmethod
    def get_object_position(wall_length, object_angle_from_left, object_angle_from_right):
        # Conversion des angles en radians
        alpha = math.radians(90 / 2 + object_angle_from_left)
        beta = math.radians(90 / 2 + object_angle_from_right)
        
        # Calcul de gamma
        gamma = math.pi - alpha - beta  # 180 degrés en radians
        
        # Calcul de la distance entre la caméra et l'objet
        distance_camera_object = wall_length * math.sin(alpha) / math.sin(gamma)
        
        # Calcul de la position Y
        position_y = distance_camera_object * math.sin(alpha)
        
        # Calcul de la position X
        position_x = math.sqrt(distance_camera_object**2 - position_y**2)
        
        return [position_x, position_y]
```

**Test :**  
Sur papier, le résultat pour les variables suivantes :
- Taille du mur : 3m
- Angle camera gauche : 10
- Angle camera droite : -12

Devrait être (environ) :
- y : 1.34 m
- x : 2.06 m

Dans le code :
```py
print(Triangulation.get_object_position(3, 10, -12))
```

Nous donne :

```py
[1.41039810759833, 2.014257246079405]
```

Les valeurs sont proches, selon moi, c'est satisfaisant.

### Conclusion
J'ai réussi à implémenter la détection de la distance en python en effectuant les calculs au tableau au préalable. Demain, je vais essayer de trouver une façon de détecter plusieurs personnes en même temps.

## 17.05.2024

#### Bilan de la veille
Hier je me suis concentré sur le développement de la triangulation, j'ai fais des calculs au tableau que j'ai intégré dans mon journal de bord.

#### Objectif de la journée
Aujourd'hui je vais essayer de développer la gestion d'objets multiples dans l'espace, mais avant cela, je vais vérifier si ma triangulation fonctionne correctement.

### 1.0 : Vérification de la triangulation

Pour prouver que ma triangulation fonctionne, j'utilise le site [Math Warefhouse](https://www.mathwarehouse.com/triangle-calculator/online.php) qui me permet d'effectuer des triangle en ligne, je compare ensuite les résultats à ceux de mon application.

#### 1.1 : Ajout des prints pour le débug

```py
@staticmethod
def get_object_position(wall_length, object_angle_from_left, object_angle_from_right):
    # Conversion des angles en radians
    alpha = 90 / 2 + object_angle_from_left
    beta = 90 / 2 + object_angle_from_right
    print(object_angle_from_left)
    print("alpha : " + str(90 / 2 + object_angle_from_left))
    print("beta : " + str(90 / 2 + object_angle_from_right))
    print("gamma : " + str(180 - (90 / 2 + object_angle_from_right) - (90 / 2 + object_angle_from_left)))
    # Calcul de gamma
    gamma = 180 - alpha - beta
    # Calcul de la distance entre la caméra et l'objet
    distance_camera_object = wall_length * math.sin(math.radians(alpha)) / math.sin(math.radians(gamma))
    print("cam -> object : " + str(distance_camera_object))
    
    # Calcul de la position X
    position_y = distance_camera_object * math.sin(math.radians(alpha))
    print("position y : " + str(position_y))
    # Calcul de la position Y
    position_x = math.sqrt(distance_camera_object**2 - position_y**2)
    print("position x : " + str(position_x))
    
    return [position_x, position_y]
```

#### 1.2 : Correction du calcul de la distance

J'ai constaté une erreur lors de mes tests, le calcul distance camera objet pointe la mauvaise camera, cela est du au fait que j'utilise $\alpha$ à la place de $\beta$.

```py
distance_camera_object = wall_length * math.sin(math.radians(alpha)) / math.sin(math.radians(gamma))

# Est adapté pour :
distance_camera_object = wall_length * math.sin(math.radians(beta)) / math.sin(math.radians(gamma))
```

#### 1.3 : Comparaison avec [Math Warefhouse](https://www.mathwarehouse.com/triangle-calculator/online.php)

Avec ce code, modifié, on peut voir avec la comparaison que les données correspondent.

##### Résultat dans le debug
![](./ressources/images/test_triangle_code.png)

#### Insertion des données dans le générateur de triangle
![](./ressources/images/test_triangle_web.png)

#### 1.4 : Test avec PyTest

Afin de tester ma fonction j'utilise PyTests et j'effectue les vérifications suivantes :

1. Valeurs classiques
2. Triangle rectangle
3. Triangle equilatéral
4. Angle suppérieur à 90°
5. Angle inférieur à 0° 

Dans le cadre de mon projet je n'ai pas besoin que ces deux derniers tests réusissent car la FOV de mes caméras est uniquement de 62.2°. Donc je retourne simplement False.

##### PyTest

```py
import pytest
from math import isclose
from triangulation import Triangulation

def test_get_object_position_valid_angles():
    result, position = Triangulation.get_object_position(3, 30, -20)
    assert result == True
    assert isclose(position[0], 0.333, abs_tol=0.001)
    assert isclose(position[1], 1.243, abs_tol=0.001)

def test_get_object_position_equilateral_rectangle():
    result, position = Triangulation.get_object_position(3, 15, 15)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 2.598, abs_tol=0.001)

def test_get_object_position_isosceles_rectangle():
    result, position = Triangulation.get_object_position(3, 30, 30, True)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 5.598, abs_tol=0.001)

def test_get_object_position_angle_greater_than_90():
    result, message = Triangulation.get_object_position(3, 45, 50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle supérieur à 90°"

def test_get_object_position_angle_less_than_0():
    result, message = Triangulation.get_object_position(3, -50, -50)
    assert result == False
    assert message == "Impossible de calculer la triangulation pour un angle inférieur à 90°"

def test_get_object_position_boundary_angles():
    result, position = Triangulation.get_object_position(3, 0, 0)
    assert result == True
    assert isclose(position[0], 1.5, abs_tol=0.001)
    assert isclose(position[1], 1.5, abs_tol=0.001)

if __name__ == "__main__":
    pytest.main()
```

##### Résultat

```sh
(venv) svoboda@ubuntu-karelsvbd:~/srs-proto$ python3 test_triangulation.py 
position y : 1.2435459380619063
alpha : 75.0
beta : 25.0
gamma : 80.0
cam_left -> object : 1.287413488921204
position x : 0.33320712985469103
position y : 1.2435459380619063
(True, [0.33320712985469103, 1.2435459380619063])
====================================================================== test session starts =======================================================================
platform linux -- Python 3.11.6, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/svoboda/srs-proto
collected 6 items                                                                                                                                                

test_triangulation.py ......                                                                                                                               [100%]

======================================================================= 6 passed in 0.04s ========================================================================
(venv) svoboda@ubuntu-karelsvbd:~/srs-proto$ 
```

### 2.0 : Gestion de plusieurs objets

Il faut que je trouve une façon de faire correspondre plusieurs objets depuis  deux point de vue différents.

#### 2.1 : Calculs au tableau

Je commence par exploxer la piste avec uniquement deux caméras. En parcourant la liste deux fois, il y a une possibilité que les position soit identiques de liste en liste.

![](./ressources/images/multiple_srs.jpg)
![](./ressources//images/pseudo-code-multiple.jpg)

Après avoir effectuer des tests dans le code, je me suis rendu compte que je faisait uniquement d'afficher les deux lsite deux fois mais dans un ordre différent. Au lieu de m'obstiner, je décide de me laisser le weekend pour réfléchir à une autre approche.

### Conclusion

Aujourd'hui j'ai appris à utiliser PyTest, mis à jour la triangulation et exploré une piste pour le S.R.S multiple. Je vais réfléchir à une autre façon de procéder et recommancer la semaine prochaine.

## 21.05.2024

#### Bilan de la dernière fois
J'ai travaillé sur la première tentative pour identifier les objets dans l'espace, malheureusement sans succès.

#### Objectifs de la journée
Pour débuter, je vais répondre au mail envoyé par Monsieur Zanardi la semaine dernière, une fois cela fait, je vais trouver une nouvelle façon de pour déterminer les personnes dans l'espace.

### 1.0 : Identification de la position des personnes
Comme expliqué la semine dernière, Il m'est impossible determiner la position de chaque personne si y'en a plusieurs dans une pièce. Pour pallier à ça, j'ai pensé ajouter une autre caméras à l'autre bout de la pièce.

Si on continue à suivre la logique du projet, un angle correspond à une personne, en effectuant la suite de calculs suivants, il est possible de trouver l'angle de la personne du point de vue de la camera en haut à droite. On a ensuite plus qu'à comparer avec ce que voit la camera.

#### 1.1 : Calcul pour identifier l'angle gauche

Pour identifier l'angle de la camera de gauche on fait le calcul suivant :

##### Variables

$A = longueur\ du\ mur - y$

$B = position\ X\ de\ l'utilisateur\ $

$C = \sqrt{A^2 - B^2} $

$\gamma = 90°$

##### Théorème du sinus

On utilise ensuite le théorème du sinus pour déterminer l'angle de la camera vers l'utilisateur.

$\frac{a}{\sin(\alpha)} = \frac{b}{\sin(\beta)} = \frac{c}{\sin(\gamma)}$

Pour trouver beta on va se servir de l'angle droit ($\gamma$),la distance camera utilisateur ($C$) et la position X de l'utilisateur ($B$).

$\beta = \arcsin(\frac{\sin(\gamma)}{C}*B)$

##### Représentation graphique

![](./ressources/images/calcul-angle-gauche.jpg)

##### Implmentation (triangulation.py)

```py
def find_angle_from_top_left(position, wall_length):
    A = wall_length - position[1] # Distance Y entre la camera et l'objet
    B = position[0] # Distance X entre l'objet et la camera
    C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet
    gamma = math.radians(90) # Angle droit entre A et B
    beta = math.asin(math.sin(gamma) / C * B) # Angle entre la camera et l'objet
    return math.degrees(beta)
```

#### 1.2 : Calcul pour identifier l'angle droit

Les étapes sont quasiment identiques que pour l'angle gauche. Il faut simplement changer les variables. 

##### Variables

$A = longueur\ du\ mur - y$

$B = longueur\ du\ mur - x $

$C = \sqrt{A^2 - B^2} $

$\gamma = 90°$

##### Théorème du sinus

Comme précédament, on utilise le théorème du sinus pour trouver l'angle.

$\frac{a}{\sin(\alpha)} = \frac{b}{\sin(\beta)} = \frac{c}{\sin(\gamma)}$

Pour trouver beta on va se servir de l'angle droit ($\gamma$),la distance camera utilisateur ($C$) et la position X de l'utilisateur ($B$).

$\beta = \arcsin(\frac{\sin(\gamma)}{C}*B)$

##### Représentation graphique

![](./ressources/images/recherche_angle_droit.jpg)

##### Implémentation

```py
def find_angle_from_top_right(position, wall_length):
    A = wall_length - position[1] # Distance Y entre la camera et l'objet
    B = wall_length - position[0] # Distance X entre l'objet et la camera
    C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet    gamma = math.radians(90) # Angle droit entre A et B
    beta = math.asin(math.sin(gamma) / C * B) # Angle entre la camera et l'objet
    return math.degrees(beta)
```

### Conclusion

Malgrès ma maladie, j'ai bien avancé dans mon travail, je suis capable à présent de détecter un angle d'une personne par rapports aux caméras. Demain je vais tester mes théorie sur papier et après, implémenter la vérification avec les angles captés par les caméras.

## 22.05.2024

#### Bilan de la veille
Hier j'étais malade et j'ai trouvé une façon de déterniner l'angle depuis une cameras de l'autre bout de la zone à surveiller afin de déterminer les personnes dans la pièce.

#### Objectif du jour
Aujourd'hui je vais commencer par tester les calculs que j'ai effectué hier sur un papier et sur mon programme pour ensuite comparer les résultats. Une fois cela fait, je vais implémenter la vérification de sangles afin d'avoir une liste des utilisateurs à la fin. Il faut également compter avec la demo aujourd'hui dans l'après midi.

### 1.0 : Tests des angles

Afin d'effectuer les tests des fonctionnalités que j'ai implémenté hier. 

#### 1.1 : Code (triangulation.py)

Je commence par définir l'angle auquel un utilisateur est apperçu sur les deux caméras du dessous puis ensuite je le passe dans mes fonctions qui déterminent son angle vis à vis des caméras du dessus .

```py
result, response = Triangulation.get_object_position(10, -20, -25, True)
print(response)
print(Triangulation.find_angle_from_top_left(response, 10))
print(Triangulation.find_angle_from_top_right(response, 10))
```

**Console :**

```
alpha : 25.0
beta : 20.0
gamma : 135.0
cam_left -> object : 4.836895252959504
position x : 4.383715832837805
position y : 2.044160264027586
[4.383715832837805, 2.044160264027586]
28.855030188101914
35.219502597708626
```

#### 1.2 : Tests sur papier

À l'aide de mon rapporteur et ma règle, je dessine une pièce de 10cm par 10cm, j'ajoute les angles que j'ai entré dans mon programme.

![](./ressources/images/tests-papier.jpg) 

#### 1.2 : Conclusion

Les résultats sont très proches et doivent surement être du à mon manque de précision sur papier. J'en conclus que c'est fonctionnel.

|           | Programme          | Papier |
|-----------|---------------------|--------|
| Position X | 4.383715832837805  | 4.35   |
| Position Y | 2.044160264027586  | 2.00   |
| $\alpha$   | 28.855030188101914 | 28.5   |
| $\beta$   | 35.219502597708626 | 35.8   |

### 2.0 : Identification de plusieurs personnes

#### 2.1 : Problème initial

Avec deux caméras, je n'ai pas trouvé de façon pour identifier que points des intersections est la position de la personne.

![](./ressources/images/positions_possibles.jpg)

Comme l'image ci-dessus le montre (une donnée manque car elle sort du cadre), le nombre total d'intersection est le suivant :

$x^2$

$x=nb\ personnes$

Dans ce cas, il y a 3 personnes dans la pièce donc :

$3^2=9$

#### 2.2 : Solution apportée

Pour déterminer quelle interséction est correcte, j'ajoute une troisième camera, l'angle capté par cette dernière permet de savoir déterminer lesquelles sont valides.

![](./ressources/images/solution_multidetection.jpg)

#### 2.3 : Implémentation (triangulation.py)

##### Création de liste de toutes les intersections

Je crée une fonction `get_objects_positions`, je crée une liste avec tous les points possibles.

```py
all_possible_points = []
for left_object in objects_angles_from_bot_left:
    for right_object in objects_angles_from_bot_right:
        result, pointXY = Triangulation.get_object_position(wall_length, left_object, right_object)
        if result:
            all_possible_points.append(pointXY)
```

##### Comparaison des données

Avec tous les objets récupérés, je recherchere l'angle vis à vis de leurs position et la camera en haut à gauche. Si la différence est inférieur à une certaine données, elle est ajoutée à la liste des vrais points.

```py
for possible_point in all_possible_points:
    for top_left_angle in object_angles_from_top_left:
        top_left_angle = 90/2 + top_left_angle
        angle_object_camera = Triangulation.find_angle_from_top_left(possible_point, wall_length)
        if abs(angle_object_camera - top_left_angle) < tolerence:
            list_true_points_left.append(possible_point)
```

##### Tests

Pour ce tests les données suivantes correspondent, j'enlève 45° pour correspondre aux donnes envoyées par les caméras :

| Personne  | Camera gauche bas | Camera droite bas | Camera gauche haut                  | Position x            | Position y            |
|-----------|-------------------|-------------------|-------------------------------------|-----------------------|-----------------------|
| Personne 1| -20               | -25               | 28.855030188101914 - 45            | 4.383715832837805     | 2.044160264027586     |
| Personne 2| 15                | 12                | 68.55727721216165 - 45             | 4.7063099156843045    | 8.15156789013041      |

### Conclusion
Aujourd'hui j'ai pu effectuer les tests sur papier de mon projet, j'ai également fait un prototype qui affiche les personnes et leurs angles par rapport à la camera. Cependant, ce modèle avait beaucoups de lag, je préfère le documenter demain chez moi quand je ferai les tests en condition réels.

## 23.05.2024 et 24.05.2024 

#### Bilan de la veille
Hier j'ai effectué les tests sur papier et j'ai fais ma première démonstration qui s'est relativement bien passé, cependant, il y avait quelques bugs mais compte les corriger.

#### Objectif du jour
Pour cette première journée de travail à la maison, je vais commencer par configurer mes deux raspberry pour mon réseau local, ensuite je vais lancer une impression pour mon troisième support. Une fois cela fait, je vais faire les tests en condition réelle.

### 1.0 : Configuration des Raspberry

Je reviens sur ce points pour avoir une version à jour pour la documentation.

1. Créer l'environnement virtuel
```sh
sudo apt-get install python3-venv
python3 -m venv venv
```

2. Activez la legacy camera
```sh
sudo raspi-config
```
Naviguez :  
    - Interface options -> Enable legacy camera support -> yes

Reboot le raspberry
    - Appuyez sur oui à la sortie du menu.  

ou

```sh
sudo reboot
```

3. Activez l'environnement virtuel
```sh
source venv/bin/activate
```

4. Installer les dépendances necessaires
```sh
pip install flask opencv-python PyJWT
```

5. Installes les librairies de vidéo.

```sh
sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y
```

### 2.0 : Optimisation du serveur

Lors du dernier rendez-vous avec mes suiveurs, je me suis rendu compte que mon prototype est lent, ayant un délait d'une dizaine de seconde avec le flux capté par mes caméras. Ce problème se produit uniquement quand j'utilise la librairie Yolo. Pour contrer cela, je me suis dis que j'allais profiter de la puissance de calcul qu'offre mon GPU. Pour ce faire, j'ai suivi les commandes suivantes sur Fedora :

#### 2.1 : Installation des pilotes Nvidia et installation de cuda

```
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install akmod-nvidia
sudo dnf install xorg-x11-drv-nvidia-cuda
lsmod | grep -i nvidia
nvidia-smi
```

#### 2.2 : Déplacement des modèles pré-entrainés sur le GPU si possible
Afin de faire cela, j'ajoute cette ligne dans mon script. Si cuda, est disponible, alors il est utilisé. Sinon c'est le processeur. :

```py
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

#### 2.3 : Tests

Sur la vidéo suivante sont affichées les deux caméras fonctionnelles avec un délais fortement réduit.

![](./ressources/videos/optimised_cameras.gif)

### 3.0 : Tests réels

Ayant accès à une grand epièce chez moi, je peux effectuer les tests en condition réele.

#### 3.1 : Test avec une camera

l'objectif de ce test est de savoir l'angle d'où se trouve l'utilisateur par rapport à la camera. Pour résumer, avec une camera de fov de 62.2, tout à gauche serait -31.1 et tout à droite 31.1.

Le résultat est fonctionnel, voici le lien vers la vidéo Youtube :

[SRS - Single Camera Demo](https://www.youtube.com/watch?v=yyQEoyNrqvA)


#### 3.2 : Test avec plusieurs cameras

À présent il est temps d'essayer ce que donne le système avec plusieurs cameras et vérifier que la position x et y est correcte.

Dans l'exemple suivant, les caméras sont séparée de 10m.

[SRS - Double Camera Demo](https://www.youtube.com/watch?v=f4BZxshQ2D0)

Le test est concluant, ma position est affichée en temps réelle dans la pièce.

### Conclusion
Aujourd'hui j'ai réussi à faire les démo ainsi qu'optimiser mon code. Je suis content que le projet fonctionne.

## 27.05.2024

#### Bilan de la dernière fois
La semaine dernière j'ai travaillé sur la reconnaissance spatiale et j'ai terminée en faisant des tests que j'ai hébergé sur youtube.

#### Objectif du jour
Pour commencer, je vais commencer par lancer une impression afin de tester mon système de tri-caméras demain. Ensuite je vais retourner à l'école chercher le restant de mes composants. Une fois cela fait, je vais essayer d'implémenter la reconnaissance faciale.

### 1.0 : Reconnaissance facaile en temps réel

Ayant déjà effectué un projet en utilisant la librairie [face-recognition](https://pypi.org/project/face-recognition/), j'ai voulu l'implémenter dans le projet SRS. Cependant, lors de l'exécution de mon ancien programme, je me suis rendu compte que le code était très le lent. Le temps réel était donc complexe. Je vais donc chercher d'autres altetrnatives.

#### 1.1 : Recherche de la bonne technologie

Avec l'aide de ChatGPT, j'ai pu trouver une alternative pour face_recongition. En premier lieu je recherche une façon qui marche c'est pour cela que j'utilise une ia.

##### Code généré 

```py
import cv2
import dlib
import os
import numpy as np

class FaceRecognitionSRS:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
        self.known_face_descriptors, self.known_labels = self.load_faces('faces')

    # Fonction pour extraire les descripteurs de visage
    def get_face_descriptor(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        if len(faces) == 0:
            return None

        shape = self.predictor(gray, faces[0])
        face_descriptor = self.face_rec_model.compute_face_descriptor(img, shape)
        return np.array(face_descriptor)

    # Chargement des images et extraction des descripteurs
    def load_faces(self, directory):
        face_descriptors = []
        labels = []
        for filename in os.listdir(directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                path = os.path.join(directory, filename)
                descriptor = self.get_face_descriptor(cv2.imread(path))
                if descriptor is not None:
                    face_descriptors.append(descriptor)
                    labels.append(filename)
        return face_descriptors, labels

    # Comparaison des descripteurs
    def compare_faces(self, descriptor, known_descriptors, threshold=0.6):
        distances = np.linalg.norm(known_descriptors - descriptor, axis=1)
        min_distance = np.min(distances)
        if min_distance < threshold:
            return True, np.argmin(distances)
        else:
            return False, None

def main():
    # Initialisation de l'instance de reconnaissance faciale
    recognizer = FaceRecognitionSRS()

    # Capture vidéo en temps réel
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionnement pour accélérer le traitement
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Obtenir le descripteur de visage pour la frame actuelle
        descriptor = recognizer.get_face_descriptor(small_frame)

        if descriptor is not None:
            match, index = recognizer.compare_faces(descriptor, recognizer.known_face_descriptors)
            if match:
                label = recognizer.known_labels[index]
            else:
                label = 'Inconnu'

            # Affichage de l'étiquette sur la frame
            faces = recognizer.detector(cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY))
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x*2, y*2), ((x+w)*2, (y+h)*2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x*2, y*2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
```

##### Résultat

Sur la vidéo suivante on voit que mon visage est détecté et que c'est assez fiable. Si j'ai pas d'autres choix, je vais utiliser ce code.

![](./ressources/videos/reconnaissance-faciale.gif)

### 2.0 : Système tri camera

Avec mon troisième modèle imprimé, je peux faire les tests du système tri-caméras.

#### 2.1 : Code à tester

J'adapte légérement le code des bi caméras afin de récupérer les 3 flux.

##### triple-camera.py

```py
import cv2
import torch
import numpy as np
from triangulation import Triangulation

# Configuration
CAMERA_URLS = [
    "http://192.168.1.118:4298/video",
    "http://192.168.1.115:4298/video",
    "http://192.168.1.114:4298/video"
]

CAMERA_FOV = 62.2  # Angle de vue de la caméra en degrés
ROOM_WIDTH = 4  # Largeur de la pièce en mètres
ROOM_HEIGHT = 4  # Hauteur de la pièce en mètres

# Charger le modèle YOLOv5 pré-entrainé et déplacer le modèle sur le GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Initialisation des captures vidéo
cap1 = cv2.VideoCapture(CAMERA_URLS[0])
cap2 = cv2.VideoCapture(CAMERA_URLS[1])
cap3 = cv2.VideoCapture(CAMERA_URLS[2])

# Vérifiez si les captures vidéo sont ouvertes correctement
if not cap1.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 1")
    exit()
if not cap2.isOpened():
    print("Erreur : Impossible de lire le flux vidéo de la caméra 2")
    exit()

def process_frame(frame, model, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    angles = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:  # Détecter les personnes uniquement
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles

map_width, map_height = 600, 600

while True:
    # Lire les frames des deux caméras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    # Si une des captures échoue, on sort de la boucle
    if not ret1 or not ret2:
        print("Erreur : Impossible de lire une frame des flux vidéo")
        break

    frame1 = cv2.flip(cv2.flip(frame1, 0), 1)
    frame2 = cv2.flip(cv2.flip(frame2, 0), 1)
    frame3 = cv2.flip(cv2.flip(frame3, 0), 1)

    # Traiter les frames pour détecter les personnes et calculer les angles
    frame1_processed, angles_cam1 = process_frame(frame1, model, CAMERA_FOV)
    frame2_processed, angles_cam2 = process_frame(frame2, model, CAMERA_FOV)
    frame3_processed, angles_cam3 = process_frame(frame3, model, CAMERA_FOV)

    # Afficher les frames dans des fenêtres séparées
    cv2.imshow('Camera 1', frame1_processed)
    cv2.imshow('Camera 2', frame2_processed)
    cv2.imshow('Camera 3', frame3_processed)

    if len(angles_cam2) >= 1 and len(angles_cam1) >= 1 and len(angles_cam3) >= 1:
        result = Triangulation.get_objects_positions(4, angles_cam1, angles_cam2, angles_cam3, None)
        if result:
            print(result)

        #if result:
        #    map_frame = np.zeros((map_height, map_width, 3), dtype=np.uint8)
        #    # Redimensionner les positions pour correspondre à la carte
        #    map_x = int((response[1] / ROOM_WIDTH) * map_width)
        #    map_y = int((response[0] / ROOM_HEIGHT) * map_height)
        #    # Limiter les coordonnées à l'intérieur de la carte
        #    map_x = np.clip(map_x, 0, map_width - 1)
        #    map_y = np.clip(map_y, 0, map_height - 1)
        #    # Dessiner un point à la position calculée
        #    cv2.circle(map_frame, (map_x, map_y), 5, (0, 0, 255), -1)
        #    cv2.putText(map_frame, f"X: {response[0]:.2f}, Y: {response[1]:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        #    cv2.imshow('Map', map_frame)

    # Appuyer sur 'q' pour quitter les fenêtres
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les captures vidéo et fermer les fenêtres
cap1.release()
cap2.release()
cv2.destroyAllWindows()
```

##### triangulation.py

Pour résumer, ce code vérifie si l'angle trouvé mathématiquement par les deux caméras est plus ou moins égal à l'angle capté par la caméra.

```py
def get_objects_positions(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, object_angles_from_top_left, object_angles_from_top_right, tolerence=10**-15):
    all_possible_points = []
    for left_object in objects_angles_from_bot_left:
        for right_object in objects_angles_from_bot_right:
            result, pointXY = Triangulation.get_object_position(wall_length, left_object, right_object)
            if result:
                all_possible_points.append(pointXY)
    list_true_points_left = []
    list_true_points_right = []
    for possible_point in all_possible_points:
        for top_left_angle in object_angles_from_top_left:
            top_left_angle = 90/2 + top_left_angle
            angle_object_camera = Triangulation.find_angle_from_top_left(possible_point, wall_length)
            print(str(angle_object_camera) + " : "  + str(top_left_angle))
            if abs(angle_object_camera - top_left_angle) < tolerence:
                list_true_points_left.append(possible_point)
    
    list_true_points = []

    list_true_points.append(list_true_points_left)

    return list_true_points_left

def find_angle_from_top_left(position, wall_length):
    A = wall_length - position[1] # Distance Y entre la camera et l'objet
    B = position[0] # Distance X entre l'objet et la camera
    C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet
    gamma = math.radians(90) # Angle droit entre A et B
    beta = math.asin(math.sin(gamma) / C * B) # Angle entre la camera et l'objet
    return math.degrees(beta)
```

##### Résultat

J'ai mis la vidéo sur Youtube. L'objectif est d'avoir les données les plus proches entre l'angle de la camera et la personne. Sur la gauche, c'est l'angle trouvé mathématiquement et à droite, celui capté par la caméra.

- [SRS Tri Camera - Test 1](https://youtu.be/AQjxHJF_0o0)

En conclusion, on peut constater que certaines imprécisions sont à constater. Premièrement, on dirait que les angles sont parfois très identitiques à très disparates.

Cela peut être dut à deux choses :
1. Mauvais placement des caméras
2. Lag entre les caméras

Pour résoudres je vais utiliser des craies, pour tracer au sol un périmètre et tracer des angles à 45°.

![](./ressources/images/piece-traces.jpg)  
![](./ressources/images/trace-sol.jpg)

### Conclusion
J'ai avancé sur la reconnaissance faciale et sur la reconnaissance spatiale avec 3 caméras. Demain je vais essayer de trouver la source des imprécisions. Je vais également imprimmer le quatrième et le dernier support.

## 28.05.2024

#### Bilan de la veille

Hier, j'ai effectué un prototype de la reconnaissance faciale et j'ai débuté mes tests avec mes trois caméras.

#### Objectif de la journée

Je vais commencer la journée en mettant en route la quatrième impression. Ensuite, je vais effectuer les tests afin de trouver le problème.

### 1.0 : Tests du système tri-caméra

Je vais effectuer la série de tests suivants pour déterminer où est le problème.

Je me place en haut, au millieu puis en bas de la pièce en faisant un tour sur moi à chaque fois et faisant une pose à chaque quart de tour. Je repette cette opération à gauche, au millieu puis à droite. Cela me permettra surement de déterminer le problème.

#### Résultats

| Position      | Calcul      | Pov Cam 3   |
|---------------|-------------|-------------|
| Gauche Bas    | Non détecté | Non détecté |
| Gauche Milieu | 37°         | 27°         |
| Gauche Haut   | 45°         | 45°         |
| Milieu Bas    | 17.5°       | 38.5°       |
| Milieu Milieu | 42°         | 47°         |
| Milieu Haut   | 50°         | 67°         |
| Droite Bas    | 41°         | 49°         |
| Droite Milieu | 76°         | 59°         |
| Droite Haut   | 72°         | 73°         |

##### Conclusion
Les résultats ne sont pas assez précis pour pouvoir en tirer de réeles conclusion, je dois tracer une zone plus précise au sol.

#### 1.1 : Second test plus précis

J'ai fais des marques au sol séparée de 60 cm. Avec cela, les résultats devrait être mieux interprétables.

![](./ressources/images/9-marks-floor.jpg)

J'ai également décidé de modifier ma fonction de calcul de l'angle pour calculer alpha.

```py
def find_angle_from_top_left(position, wall_length):
    A = wall_length - position[1] # Distance Y entre la camera et l'objet
    B = position[0] # Distance X entre l'objet et la camera
    C = math.sqrt(A ** 2 + B ** 2) # Distance camera objet
    gamma = math.radians(90) # Angle droit entre A et B
    alpha = math.asin(math.sin(gamma) / C * A) # Angle entre la camera et l'objet
    return math.degrees(alpha)
```

[SRS Tri Camera - Test 2 (Vidéo Youtube)](https://youtu.be/oRsWYY_EFWs)

##### Conclusion

En effectuant le test, je me suis rendu compte que les calculs était simplement correctes. Le problème vient de ma façon à trouver l'angle des utilisateurs, en effet on peut voir dans la vidéo une différence dans l'angle entre ce qui est capté et la caméra quand je trourne sur moi même, si je cumule les erreurs entre les trois caméras, cela explique les imprécisions.

Pour palier à cela, je vais simplement mettre la reconnaissance multi-utilisateur en alpha. Car en théorie ça fonctionne mais en pratique c'est complexe à implémenter. Du moins avec les technologies que j'ai choisis.

### 2.0 : Correction du bug du serveur

Lors du sernier rendez-vous avec mes suiveurs j'ai eu un bug lors de la recherche de caméras sur le réseau. Je vais essayer de le régler.

Sur le serveur j'ai trouvé que j'ai mis le mot *self* à une variable qui n'est pas d'instance. Ce qui causait un bug. Cela étant corrigé, le code fonctionne.

```py
tokens_for_ip = cameraServerClient.getCamerasTokens(cameras_in_network)
```

Je me suis ensuite rendu compte que l'application considérait son réseau local comme 127.0.0.1. Ce qui est étrange car au CFPT c'était 192.168.1.0. J'hardcode le réseau pour l'instant.

Avec cette modification et quelques autres optimisations, la recherche automatique de caméra fonctionne à nouveau.

### Conclusion
J'ai bien avancé sur la gestion des JWT. Il faut cependant que je trouve une solution pour la reconnaissance spatiale, c'est un point central de mon projet et demain avec les quatres caméras disponnibles, je vais trouver une solution.

## 29.05.2024

### Bilan de la veille
Hier j'ai travaillé sur les tests de mon modèle de reconnaisssance spatiale qui ne sont pas bien terminés et sur la corrections de bug de mon serveur.

### Objectif du jour
Je vais commencer par tourner une video pour montrer à mes suiveurs que la recherche automatique de caméra fonctionne. Ensuite, je dois aller à l'école pour faire l'évaluation intermédiaire ainsi qu'une présentation en anglais de mon projet.

### 1.0 : Correction du bug du management des caméras

J'ai remarqué une erreur lors de mes tests. Quand j'arrive sur la page, les caméras se remettent à zéro, cela veut dire que j'ai un problème avec les fonctions `get_cameras_that_are_not_in_database` et `get_cameras_that_are_not_in_network`. Le problème vient du format dont je récupère dans ma classe socet io qui n'est pas compatible avec ce que j'ai dans la base :

```
Format Socket.io :
[IPv4Address('192.168.1.121')]
Format Bdd :
192.168.1.121
```

Pour régler le problème, j'utilise regex afin de récupérer uniquement ce qui ce situe entre les guimets.

```py
result_camera_list = []
pattern = r"'(.*?)'"
network_cameras = re.findall(pattern, str(network_cameras))
```

En ajoutant cette modification à mes deux fonctions, le management des caméras fonctionne.

![](./ressources/videos/camera-management.gif)

### 2.0 : Second système pour la multi-reconnaissance et calibration

Après réfléxion, je me suis dis que ça pouvait être interessant d'avoir une page de calibration qui indique la position de l'utilisateur au milieu de la pièce. Pour ce faire, il suffirait de voir l'angle où l'utlisateur est capté et essayer de le placer aussi proche du 0 (ou 45) que possible. Je note cette idée

Après cela, je me suis dis qu'il serait interessant d'explorer une nouvelle piste pour la reconnaissance spatiale avec 4 caméras. En utilisant les caméras du haut ainsi que les caméras du bas pour trouver la position des personnes. On pourrais déterminer leurs véritable position. Voici un croquis comment cela fonctionnerait :

La raison pourquoi cette méthode est plus efficace est que l'angle où est capté l'utilisateur depuis le haut de la pièce est similaire à celui vers le bas. Si un utilisateur est tourné depuis le point de vue des caméeras du dessous, il le sera également depuis celles du haut.

![](./ressources/images/multi-person-detection-v2.jpg)

#### 2.1 : Implémentation (Triangulation.py)

Je commence par créer une fonction `get_objects_positions_v2` et je crée deux liste qui me permettent de récupérer tous les points possibles.

```py
for left_object_bot in objects_angles_from_bot_left:
    for right_object_bot in objects_angles_from_bot_right:
        result, pointXY = Triangulation.get_object_position(wall_length, left_object_bot, right_object_bot)
        if result:
            all_possible_points_bot.append(pointXY)
for left_object_top in objects_angles_from_top_left:
    for right_object_top in objects_angles_from_top_left:
        result, pointXY = Triangulation.get_object_position(wall_length, left_object_top, right_object_top)
        if result:
            all_possible_points_top.append(pointXY)
```

Je crée ensuite une fonction me permettant de convertir les points capturés depuis les caméras du haut comme s'ils étaient capturés depuis le bas afin de pouvoir les comparer.

```py
all_possible_points_top = Triangulation.convert_to_top_position(wall_length, all_possible_points_top)


def convert_to_top_position(wall_length, objects_positions):
    position_from_top = []
    for position in objects_positions:
        position_from_top.append([wall_length - position[0], wall_length - position[0]])
    return position_from_top
```

Je termine en comparant les points avec une tolérence. Si les points correspondent, je l'ajoute à la liste en faisant une moyenne de la position.

```py
true_points = []
for top_point in all_possible_points_top:
    for bot_point in all_possible_points_bot:
        if(abs(top_point[0] - bot_point[0]) < tolerence and abs(top_point[1] - bot_point[1]) < tolerence):
            true_points.append([(top_point[0] + bot_point[0]) / 2, (top_point[1] + bot_point[1]) / 2])
return true_points
```

### 3.0 : Calibration

Pour la calibration, l'objectif est d'afficher les angles captés par les 4 caméras.

#### 3.1 : Route (Serveur : app.py)

1. Récupère l'id du network passé en paramètre
2. Récupération de la liste des caméras depuis la bdd avec l'id du network
3. Récupération des images captés par les caméras
4. Récupération des angles des utilisateurs présents dans l'image

```py
@JwtLibrary.API_token_required
def calibration(self):
    idNetwork = request.args.get('idNetwork')
    if not idNetwork:
        return jsonify({'error': 'Network ID is required'}), 400
    response = []
    result, response = self.db_client.getCamerasByIdNetwork(idNetwork)
    if not result:
        return jsonify({'error': 'Camera not found'}), 404
    cameras_angles = []
    for data in response:
        camera = Camera(data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, None)
        resultImg, responseImg = CameraServerClient.getCameraImage(camera.ip, camera.jwt)
        if resultImg:
            cameras_angles.append({camera.ip: self.spaceRecognition.get_persons_angles(responseImg, 62.2)})
        return jsonify(cameras_angles), 200
```

#### 3.2 : Récupération des angles (Serveur : space_recognition.py)

La fonction `get_persons_angles` permet de récupérer les angles où les personnes sont captées.

```py
def get_persons_angles(self, frame, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = self.model(frame_rgb)
    angles = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
    return angles
```

#### 3.3 : Récupération des données (Application : server_client.py)

La fonction `get_calibration` sert de client au serveur et récupère les données.

```py
def get_calibration(self, idNetwork):
    endpoint_url = f"{self.server_url}/calibration?idNetwork={idNetwork}"
    params = {
        'token': self.API_token
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()
```

#### 3.4 : Vue et interprétation des données (Application : calibration_window.py)

```py
def on_enter(self):
    super().on_enter()
    self.app = App.get_running_app()
    self.server_client = self.app.get_server_client()
    self.api_call_loop = Clock.schedule_interval(self.update, 1)
```

La fonction `update` qui s'exécute chaque seconde, elle fait un appel à l'api et interprète les résultats en fonction des longeurs de liste.

```py
def update(self, dt):
    result, cameras_angles = self.server_client.get_calibration(44)
    
    if result:
        if len(cameras_angles) > 0:
            self.update_label(self.ids.camera1_label, list(cameras_angles[0].values())[0])
        if len(cameras_angles) > 1:
            self.update_label(self.ids.camera2_label, list(cameras_angles[1].values())[0])
        if len(cameras_angles) > 2:
            self.update_label(self.ids.camera3_label, list(cameras_angles[2].values())[0])
        if len(cameras_angles) > 3:
            self.update_label(self.ids.camera4_label, list(cameras_angles[3].values())[0])
```

La fonction `update_label` met à jour un label en fonction du text qui est passé, si la valeur se trouve entre -1 et 1 le texte apparait en vert sinon il apparait en rouge.

```py
def update_label(self, label, values):
    if (len(values) > 0):
        value = values[0]
        label.text = str(value)
        if -1 <= value <= 1:
            label.color = (0, 1, 0, 1)
        else:
            label.color = (1, 0, 0, 1)
```

La fonction `on_leave` permet de arrêter les appels à l'api quand l'utilisateur quitte la fenêtre.

```py
def on_leave(self):
    self.api_call_loop.cancel()
```

#### 3.5 : Résultat

![](./ressources/videos/calibration.gif)

### Conclusion

Avec la calibration j'ai implémenté une nouvelle fonctionnalité qui fonctionne bien, je pense ajouter un affichage pour montrer la caméra et son angle plus tard. J'ai également développé une nouvelle façon de faire la reconnaissance spatiale.

## 30.05.2024

#### Bilan de la veille
Hier j'ai développé la calibration et j'ai trouvé une nouvelle façon de faire la reconnaissance spatiale avec 4 caméras.

#### Objectif du jour
En premier lieu, je vais faire des tests pour mon nouveau systeme a quatres caméras. Ensuite, si j'ai le temps, je vais implémenter la reconnaissance faciale à mon système.

### 1.0 : Correction de la triangulation
J'ai refais les calculs de la triangulation sur papier et j'ai constaté quelques erreurs.

1. L'angle $\alpha$ est mal calculé, je prends en considération l'angle extérieur à la place de l'angle intérieur.
2. Une paranthèse en trop dans le calcul du théorème du sinus. 

```py
@staticmethod
def get_object_position(wall_length, object_angle_from_left, object_angle_from_right, debug=False):
    # Conversion des angles en radians

    alpha = 90 / 2 - object_angle_from_left
    # Anciennement : alpha = 90 / 2 + object_angle_from_left

    beta = 90 / 2 + object_angle_from_right
    if beta > 90 or alpha > 90:
        return False, "Impossible de calculer la triangulation pour un angle supérieur à 90°"
    
    if beta < 0 or alpha < 0:
        return False, "Impossible de calculer la triangulation pour un angle inférieur à 90°"
    
    # Calcul de gamma
    gamma = 180 - alpha - beta

    # Calcul de la distance entre la caméra et l'objet
    distance_camera_object = wall_length / math.sin(math.radians(gamma)) * (math.sin(math.radians(beta)))
    # Anciennement : distance_camera_object = wall_length / (math.sin(math.radians(gamma)) * (math.sin(math.radians(beta))))

    # Calcul de la position Y
    position_y = distance_camera_object * math.sin(math.radians(alpha))
```

### 2.0 : Double Triangulation

L'objectif de cette fonctionnalité est de trouver les véritables points où les personnes se situent.

Le problème de mon programme est que vu que je me base sur les intersections entre les détections des personnes, le problème c'est que quand il y a plusieurs personnes, il y'a plusieurs positions possible. De plus, il n'est pas possible de différencier une personne d'une autre et je ne veux pas utiliser la reconnaissance faciale pour y pallier car elle est pas suffisament fiable. Pour plus de détails, allez vers le point 2.0 du 29.05.

#### 2.1 : Implémentation (srs-proto : triangulation.py)

J'ai ajouté un paramètre reverse qui permet de définir que l'on recherche les position depuis les caméras qui se situent à l'autre bout de la pièce.

Quand le flag reverse est à `True`, la position est convertie pour faire comme si elle avait été captée par les caméras oposée. Pour ce faire, je prends les valeurs et je les soustrais à la longeur du mur.

```py
@staticmethod
def get_object_position(wall_length, object_angle_from_left, object_angle_from_right, debug=False, reverse=False):
    # Conversion des angles en radians
    alpha = 90 / 2 - object_angle_from_left
    beta = 90 / 2 + object_angle_from_right
    if beta > 90 or alpha > 90:
        return False, "Impossible de calculer la triangulation pour un angle supérieur à 90°"
    
    if beta < 0 or alpha < 0:
        return False, "Impossible de calculer la triangulation pour un angle inférieur à 90°"
    
    # Calcul de gamma
    gamma = 180 - alpha - beta
    # Calcul de la distance entre la caméra et l'objet
    distance_camera_object = wall_length / math.sin(math.radians(gamma)) * (math.sin(math.radians(beta)))
    # Calcul de la position Y
    position_y = distance_camera_object * math.sin(math.radians(alpha))
    # Calcul de la position X
    position_x = math.sqrt(distance_camera_object**2 - position_y**2)
    if reverse:
        position_x = wall_length - position_x
        position_y = wall_length - position_y
    if debug:
        print("alpha : " + str(alpha))
        print("beta : " + str(beta))
        print("gamma : " + str(gamma))
        print("cam_left -> object : " + str(distance_camera_object))
        print("position x : " + str(position_x))
        print("position y : " + str(position_y))
    return True, [position_x, position_y]
```
 

#### 2.2 : Vidéo du test

Le point rouge correspond à la triangulation calculée depuis les caméras du sud et le point bleu, la triangulation inversée depuis les caméras nord.

[SRS - Double Triangulation](https://youtu.be/JMINCs2bN4M)

Selon moi, cette partie est fonctionnelle.

### Conclusion
Le travail que j'ai produit aujourd'hui peut paraître peut conséquent. Cependant, J'ai effectué un grand nombre de test ce qui prend du temps. Au final, le résultat est fonctionnel, il faut à présent voir ce que cela donne dans une utilisation réelle.

## 31.05.2024

#### Bilan de veille
Hier j'ai corrigé le calcul de la triangulation et j'ai développé le calcul de position depuis deux set de caméras.

#### Objectif du jour
Aujourd'hui je vais commencer par effectuer les tests réels sur la double triangulation. Si elle est fonctionnelle, je vais essayer de commencer la reconnaissance faciale.

### 1.0 : Exécution automatique du script sur les caméras
En attendant que les batteries se charge, je recherche une façon s'exécuter automatiquement le script du serveur caméra.

J'ai demandé à ChatGPT et il m'à donné deux façons de le faire, la première par `rc.local` je n'ai pas réussi à la faire fonctionner. la seconde par `systemctl` par deamon fonctionne parfaitement.

- [Prompt ChatGPT](https://chatgpt.com/share/980b9281-335c-4caf-afb8-54e407267588)

#### 1.1 : Marche à suivre

Créez le fichier de service :

```bash
sudo nano /etc/systemd/system/srs.service
```
Copiez et collez le contenu suivant dans l'éditeur nano :

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

Sauvegardez et quittez l'éditeur (Ctrl+X, puis Y, puis Entrée).

Recharger les services systemd :

```bash
sudo systemctl daemon-reload
```

Activer et démarrer le service :

```bash
sudo systemctl enable srs.service
sudo systemctl start srs.service
```

Vérifiez l'état du service :

```bash
sudo systemctl status srs.service
```

### 2.0 : Gestion des multi-utilisateur

J'ai trouvé une façon de gérer plusieurs personnes. Pour ce faire, quand une personne est détectée, tous les angles lié à cette personne sont supprimés.

J'ai crée trois objets :
1. TwoCameraPoint (Stocke les points détectés par deux caméras)
2. FourCameraPoint (Contient les références des points calculé par le set des caméras du hout et bas ainsi que la valeur moyenne de la position)
3. UniquePointList (Liste de point FourCameraPoint uniques)

```py
class TwoCameraPoint:
    def __init__(self, angle_gauche, angle_droit, value):
        self._angle_gauche = angle_gauche
        self._angle_droit = angle_droit
        self._value = value

    @property
    def angle_gauche(self):
        return self._angle_gauche

    @property
    def angle_droit(self):
        return self._angle_droit

    @property
    def value(self):
        return self._value

from two_camera_point import TwoCameraPoint

class FourCameraPoint:
    def __init__(self, point_bot: TwoCameraPoint, point_top: TwoCameraPoint, value):
        self._point_bot = point_bot
        self._point_top = point_top
        self._value = value

    @property
    def point_bot(self):
        return self._point_bot

    @property
    def point_top(self):
        return self._point_top
    
    @property
    def value(self):
        return self._value
    
    def compare_points(self, fourCameraPoint):
        #true : same point

        if self.point_bot.angle_gauche == fourCameraPoint.point_bot.angle_gauche or self.point_bot.angle_droit == fourCameraPoint.point_bot.angle_droit:
            return True
        
        if self.point_top.angle_gauche == fourCameraPoint.point_top.angle_gauche or self.point_top.angle_droit == fourCameraPoint.point_top.angle_droit:
            return True
        
        return False

from four_camera_point import FourCameraPoint

class UniquePointList:
    def __init__(self):
        self._points = []

    def add_point(self, fourCameraPoint : FourCameraPoint):
        for point in self._points:
            if fourCameraPoint.compare_points(point):
                return False
        
        self._points.append(fourCameraPoint)
        return True
    
    @property
    def points(self):
        return self._points

    def __repr__(self):
        return f"UniquePointList(points={self.points})"
```

J'implémente ces trois objets dans la classe Triangulation :

```py
def get_objects_positions(wall_length, objects_angles_from_bot_left, objects_angles_from_bot_right, object_angles_from_top_left, object_angles_from_top_right, tolerence=0.5):
    all_possible_points_bot = []
    for left_object_bot in objects_angles_from_bot_left:
        for right_object_bot in objects_angles_from_bot_right:
            result, pointXY = Triangulation.get_object_position(wall_length, left_object_bot, right_object_bot)
            if result:
                all_possible_points_bot.append(TwoCameraPoint(left_object_bot, right_object_bot, pointXY))
    all_possible_points_top = []
    for left_object_top in object_angles_from_top_left:
        for right_object_top in object_angles_from_top_right:
            result, pointXY = Triangulation.get_object_position(wall_length, left_object_top, right_object_top, reverse=True)
            if result:
               all_possible_points_top.append(TwoCameraPoint(left_object_top, right_object_top, pointXY))
    
    unique_point_list = UniquePointList()
    for possible_point_bot in all_possible_points_bot:
        for possible_point_top in all_possible_points_top:
            if(abs(possible_point_bot.value[0] - possible_point_top.value[0] < tolerence) and abs(possible_point_bot.value[1] - possible_point_top.value[1] < tolerence)):
                unique_point_list.add_point(FourCameraPoint(possible_point_bot, possible_point_top, [(possible_point_bot.value[0] + possible_point_top.value[0]) / 2, (possible_point_bot.value[1] + possible_point_top.value[1]) / 2]))
    return True, unique_point_list
```

### 3.0 : Tests réels

Dans ce tests, deux personnes sont dans dans la zone, il faut prendre en compte les résultats quand les deux personnes sont immobiles pour des question de lag qui est légérement présent.

[SRS Multiple Recognition - Version 0.1](https://www.youtube.com/watch?v=DaS3AGwTjWM)

### Conclusion
J'approche de la fin du projet, c'est cependant rassurant de savoir que le système de reconnaissance spatiale est fonctionnel. La semaine prochaine je vais implémenter la reconnaissance facial et cloturer le projet.

## 03.06.2024

#### Blian de la dernière fois
J'avais travaillé sur la reconnaissance spatiale qui est fonctionnelle.

#### Objectif du jour
Aujourd'hui je vais implémenter la reconnaissance faciale, j'ai un prototype me permettant de récupérer les encodages de la base et de faire la reconnaissance avec la caméras de mon pc. Voici les vidéo youtube en faisant la démonstration :

1. [SRS - Face Recognition](https://youtu.be/IvVYjrRSz2s)
2. [SRS - Multiple Face Recognition](https://youtu.be/TRsDz8WGZxw)

### 1.0 : Reconnaissance faciale dans les box

Ma première idée est que lorsqu'une personne est détectée, la zone de frame des cameras où se situe la personne est analysée par la reconnaissance faciale.

Cela me permettra de l'intégrer par la suite dans la reconnaissance spatiale.

### 1.1 : Implémentation "reconnaissance_faciale.py"

Je commence par récupérer les encodages des visages présents dans la base de données.

```py
class DatabaseClient:
    
    def __init__(self):
        self.dbConnexion = mysql.connector.connect(
            host="127.0.0.1",
            user="srs-admin",
            password="fzg5jc29cHbKcSuK",
            database="srs"
        )
        self.cursor = self.dbConnexion.cursor()

    def get_encodings(self):
        try:
            self.cursor.execute("SELECT username, encodings FROM Users")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
```

J'ai ensuite demandé à ChatGPT de trouver une façon de contrôler la véracité des données présentes dans la base :

```py
for user_data in users_data:
    known_face_names.append(user_data[0])
    encoding_base64 = user_data[1]
    encoding_json = base64.b64decode(encoding_base64).decode('utf-8')
    encoding = json.loads(encoding_json)
    if len(encoding) == 128:  # Vérifier la taille de chaque encodage
        known_face_encodings.append(encoding)
    else:
        print(f"Encodage incorrect pour {user_data[0]}: {encoding}")
```

Dans une boucle infinie, on détecte les personnes dans la pièce. L'algorithme fonctionne de la façon suivante :

1. Récupèration des données en utilisant le modèle de YoloV5
2. Filtrage afin de garder les personnes
3. Pour chaque personne détectée
    - Tentative de reconnaissance faciale
    - Ajout du résultat dans la frame
4. Affichage de la frame

```py
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        break
    
    results = model(frame)
    
    bboxes = results.xyxy[0].cpu().numpy()
    
    # Filtrage afin de garder uniquement les personnes
    person_bboxes = [bbox for bbox in bboxes if int(bbox[5]) == 0]
    
    # Liste des résultats
    results_list = []

    # Pour chaque personne détectée, essayer de reconnaître le visage
    for bbox in person_bboxes:
        name = recognize_faces(frame, bbox, tolerance=0.4)
        results_list.append({'Position': bbox[:4], 'Personne détectée': name})
        
        # Affichage final des résultats
        left, top, right, bottom = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({left}, {top}, {right}, {bottom})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Afficher le résultat
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

La reconnaissance faciale fonctionne de la façon suivante :

1. Récupération de la position de la personne
2. Isolation de la partie de l'image à détecter
3. Tentative de détection de visages
4. Vérification de la bonne capture des encodage des visages
5. Pour chaque visage détectée dans l'image isolée
    - Recherche de correspondance entre les encodages de la base et ceux dans l'image
    - Si correspondance trouvée, retour des utilisateurs trouvés.


```py
def recognize_faces(image, bbox, tolerance=0.6):
    top, left, bottom, right = int(bbox[1]), int(bbox[0]), int(bbox[3]), int(bbox[2])
    face_image = image[top:bottom, left:right]
    
    # Conversion au format RGB
    face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    
    # Recherche de visage dans l'image
    face_locations = face_recognition.face_locations(face_image_rgb)
    if not face_locations:
        return "Personne"
    
    face_encodings = face_recognition.face_encodings(face_image_rgb, face_locations)
    if not face_encodings:
        return "Personne"
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
        name = "Visage inconnu"
        
        if np.any(matches):  # Permet de déterminer s'il y a une corresponsance dans la liste
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches and best_match_index < len(matches) and matches[best_match_index]:
                name = known_face_names[best_match_index]
        
        return name
    return "Personne"
```

### 1.2 : Résultat

J'ai fais une vidéo youtube montrant le tests, et comme vous pouvez le voir le script fonctionne cependant, il est moins fiable de faire la reconnaissance faciale par rapport à la détection de personnes. Ce qui veut dire que l'architecture de mon projet était bien trouvée (détection de personnes -> reconnaissance faciale).

Dans la vidéo, la personne s'ajoute dans la base puis se fait détecter par la suite.

- [SRS - Face Recognition](https://www.youtube.com/watch?v=IvVYjrRSz2s)

Ici, on fait le test avec deux personnes.

- [SRS - Multiple Face Recognition](https://youtu.be/TRsDz8WGZxw)

### 2.0 : Reconnaissance Faciale dans la reconnaissance spatiale (srs-face_recognition.py)

Je vais uniquement expliquer comment j'ai intégré la reconnaissace faciale dans la reconnaissance spatiale, pour plus de détails sur cette dernière, allez consulter l'entrée du jdb du 31.05.2024.

L'objectif est de reconnaitre les personnes uniquement si elles sont détectés par le système.

J'ajoute la reconnaissance faciale dans le projet et j'appèle la fonction `recognize_faces` dans le process frame, comme ça quand une personne est détectée par le système via Yolov5, il y a également une tentative au niveau de space recognition.

```py
def process_frame(frame, model, fov):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    angles = []
    names = []
    for det in results.xyxy[0].cpu().numpy():
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:
            center_x = (x1 + x2) / 2
            angle = (center_x - frame.shape[1] / 2) / frame.shape[1] * fov
            angles.append(angle)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Ici
            name = recognize_faces(frame, (x1, y1, x2, y2))
            names.append(name)
            cv2.putText(frame, f"Angle: {angle:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, name, (int(x1), int(y2) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, angles, names
```

#### 2.1 : Vérification de l'identité des personnes

J'ai du trouver une façon de déterminer l'identidé de la personnes avec la reconnaissance faciale depuis les différentes cameras. Pour ce faire j'ai crée une fonction `get_name_per_index`.

```py
def get_name_per_index(name_list):
    """
    Met à jour les noms dans la liste avec un compteur d'index et retourne le nom avec la plus grande occurrence.

    Args:
        name_list: Liste des noms de personnes détectées.

    Returns:
        Le nom avec le plus grand nombre de correspondances. Si aucun nom n'est reconnu, retourne "Personne non reconnue".
    """
    name_counter = {}
    updated_name_list = []  
    
    for name in name_list:
        if name != "None" and name != "Unknown":
            if name in name_counter:
                name_counter[name] += 1
            else:
                name_counter[name] = 1

            updated_name_list.append(f"{name}_{name_counter[name]}")
    # Trouver le nom avec la plus grande correspondance
    if(len(name_counter) > 0):
        return max(name_counter, key=name_counter.get)
    return "Personne non reconnue"
```

#### 2.2 Tests

[SRS - Version 0.1](https://www.youtube.com/watch?v=RFYBNXF6DCQ)

Pour conclure, ça fonctionne cependant il y a pas mal de lag, si j'ai le temps je vais optimiser cela mais je vais me concentrer à documenter mes fonctionnalités.

### Conclusion

J'ai réussi à développer la reconnaissance spatiale avec la reconnaissance faciale de façon dynamique.

## 04.06.2024

#### Bilan de la veille

Hier j'ai implémenté la reconnaissance faciale dans la reconnaissance spatiale.

#### Objectif du jour

Je vais implémenter mes fonctionnalités dans l'application Kivy.

### 1.0 : Implémentation des subprocess

Je pense que j'ai plus le temps pour implémenter les focntionnalités directement dans Kivy, je recherche donc une façon de lancer un script depuis mon application. J'utilise les [subprocess](https://stackoverflow.com/questions/6945466/using-python-to-run-another-program/6945501#6945501) pour faire fonctionner cela.

#### 1.1 : Ajout des arguments (srs-proto : srs-face_recognition.py)

Ensuite, il me faut trouver une façon de passer les liens vers les cameras et d'autres variables afin de rendre le script dynamique. Pour ce faire, j'utilise la librairie [argparse](https://docs.python.org/3/library/argparse.html).

```py
# Récupération des arguments
parser = argparse.ArgumentParser(description="Object Detection and Triangulation with multiple cameras")
parser.add_argument('--camera_url1', type=str, required=True, help='URL of the first camera')
parser.add_argument('--camera_url2', type=str, required=True, help='URL of the second camera')
parser.add_argument('--camera_url3', type=str, required=True, help='URL of the third camera')
parser.add_argument('--camera_url4', type=str, required=True, help='URL of the fourth camera')
parser.add_argument('--wall_size', type=str, required=True, help='Size of the walls')
parser.add_argument('--api_link', type=str, required=True, help='Link to the users API')
parser.add_argument('--headless', action='store_true', help='Run in headless mode without GUI')
args = parser.parse_args()


# Configuration
CAMERA_URLS = [
    args.camera_url1,
    args.camera_url2,
    args.camera_url3,
    args.camera_url4
]

wall_size = float(args.wall_size)
api_link = args.api_link
```

### 1.2 : Intégration (room_window.py)

**Création des paramètres**

1. Recherche des cameras
2. Création du lien des caméras
    - Ajout de l'adresse ip ainsi que du JWT
3. Ajout de la taille du mur en paramètre
4. Ajout du lien vers l'api des données faciale
    - On ne peut pas les transmettre direcement dans les paramètre pour des questions de taille et de format.

Les autres fonctionnalités ont un schema de fonctionnement similaire mais avec moins de paramètres.

**Appel du subprocess (_run_subprocess_script)**

1. S'il y a des paramètres supplémentaires dans la fonction (cameras, wall_size, api_link), on les ajoute dans les paramètres du subprocess.
2. On lance le subprocess avec le script_path et les paramètres.

```py
def run_spatial_recognition_system(self):
    wall_size = self.ids.size_textInput.text
    room = Room()
    api_link = self.server_client.get_users_link()
    for camera in self.cameras:
        match camera.idWall:
            case 1:
                room.set_top_left(camera)
            case 2:
                room.set_top_right(camera)
            case 3:
                room.set_bottom_left(camera)
            case 4:
                room.set_bottom_right(camera)
    camera_urls = [
        f"http://{room.get_bottom_left().ip}:4298/video?token={room.get_bottom_left().jwt}",
        f"http://{room.get_bottom_right().ip}:4298/video?token={room.get_bottom_right().jwt}",
        f"http://{room.get_top_left().ip}:4298/video?token={room.get_top_left().jwt}",
        f"http://{room.get_top_right().ip}:4298/video?token={room.get_top_right().jwt}"
    ]
        
    self._run_subprocess_script('../srs-proto/srs-face_recognition.py', camera_urls, wall_size, api_link)
def _run_subprocess_script(self, script_path, cameras=None, wall_size=None, api_link=None):
    # Construire le chemin absolu pour le script
    abs_script_path = os.path.abspath(script_path)
    
    print(f"Tentative d'exécution du script : {abs_script_path} avec les paramètres : {cameras}")
    file_exists = os.path.exists(abs_script_path)
    
    if file_exists:
        try:
            command = ["python", abs_script_path]
            
            if cameras != None:
                for i, param in enumerate(cameras):
                    command.extend([f'--camera_url{i+1}', param])
            
            if wall_size != None:
                command.extend([f'--wall_size', wall_size])
            
            if api_link != None:
                command.extend([f'--api_link', api_link])
            result = subprocess.run(command, capture_output=True, text=True)
            print(f"Sortie du script : {result.stdout}")
            print(f"Erreurs du script : {result.stderr}")
            
        except Exception as e:
            print(f"Erreur lors de l'exécution du script : {e}")
    else:
        print("Le fichier spécifié n'existe pas.")
```

#### Implémentation graphique

![room](./ressources/images/room_window.png)

```
<RoomWindow>:
    name: "room"

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
                text: "Système de reconnaissance spatiale"
                bold: True

            Image:
                source: 'Ressources/logo.png'
        
        GridLayout:
            cols: 1
            size_hint_y: 0.9
            pos_hint: {'top': 0.9}

            GridLayout:
                cols: 2

                Label:
                    text: "Taille du mur"
                
                TextInput:
                    id: size_textInput

            Button:
                text: "Système de reconnaissance Spatiale"
                on_release:
                    bold: True
                    # Ajouter ici le code pour gérer l'action du bouton
                    root.run_spatial_recognition_system()

            Label:
                text: "Prototypes"

            GridLayout:
                cols: 2

                Button:
                    text: "Angle Camera"
                    on_release:
                        # Ajouter ici le code pour gérer l'action du bouton
                        root.run_angle_camera()

                Button:
                    text: "Deux cameras"
                    on_release:
                        # Ajouter ici le code pour gérer l'action du bouton
                        root.run_two_cameras()

            GridLayout:
                cols: 2

                Button:
                    text: "Quatres cameras"
                    on_release:
                        # Ajouter ici le code pour gérer l'action du bouton
                        root.run_four_cameras()
                
                Button:
                    text: "Reconnaissance faciale"
                    disabled: True
                    on_release:
                        # Ajouter ici le code pour gérer l'action du bouton
                        root.run_face_recognition()
```

J'ai appliqué les subprocess à d'autres script me permettant de montrer quelques prototypes en plus. Cela me permettra de mieux expliquer le fonctionnement du système en montrant plus d'étapes.

#### Conclusion

J'ai implémenté les subprocess, cela m'a permis de régler le problème de temps et les éventuels défis liés à l'intégration opencv dans kivy.

## 05.06.2024

## 06.06.2024

## 07.06.2024

## Conclusion

Dans sa globalité, le travail a été effectué. Les deux aspects du projet que sont la reconnaissance spatiale ainsi que la gestion des différents composant de façon automatique sont fonctionnels. Cependant, des aspects d'amélioration peuvent être trouvés. Par exemple, la modification des données faciales. La fonctionnalité est implémentée du côté du serveur mais j'ai pas réussi à la faire fonctionner depuis l'application à cause d'un bug présent dans Kivy. Également, je pense qu'il y a des améliorations possibles au niveau des performances de la reconnaissance spatiale. La librairie face_recognition prend énormément de ressources et trouver une alternative permetterais de rendre le projet plus fluide et par conséquent, plus fiable.

### Bilan personnel

Je suis staisfait du travail que j'ai effectuer. Travailler sur ce projet m'a permis d'apprendre à combiner les technologies avec lesquelle j'ai eu l'occasion de travailler au cours de cette seconde année en tant que technicien ES et je trouve que c'est une bonne conclusion aux travaux que j'ai eu l'occasion de faire. 