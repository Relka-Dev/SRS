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