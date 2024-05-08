# Abstract 

Résumé du projet en français ainsi qu'en anglais.

## Version française

### Présentation
Le système de reconnaissance spatiale est un projet qui vise à sécuriser une pièce en déterminant la position et l'identité des personnes qui s'y trouve. Pour y arriver, le système utilise des technologies d'intelligence artificielle de reconnaissance et d'identification de personnes.

### Initialisation
L'administrateur commence par initialiser le système. Il démarre l'application, si un serveur SRS est trouvé, il lui demande de se connecter avec les identifiants par défaut présents dans le manuel d'installation. Une fois les identifiants vérifiés, il peut ajouter un premier administrateur. Après avoir rentré son nom ainsi qu'un mot de passe sécurisé, il est redirigé vers la page de connexion ou il lui est demandé de rentrer à nouveau les identifiants de l'administrateur afin d'accéder au reste du système. Si les identifiants sont corrects, l'utilisateur est redirigé vers la page d'accueil.

### Configuration
Pour configurer le serveur, l'administrateur par ajouter une personne dans le système, il doit rentrer son nom, une photo de son visage et le type de personne (associé, dangereux ou autre).  
Ensuite, il doit placer les caméras dans les coins de la pièce. Une fois cela fait, il doit assigner la localisation de la caméra par rapport à la pièce, par exemple, nord/ouest pour une caméra se situant en haut à gauche de la pièce.

### Reconnaissance spatiale
Une fois le serveur et les caméras configurées, chaque caméra envoie les données capturées au serveur central. Le système calcule la position des personnes en utilisant la triangulation entre les différentes caméras et si possible, essaie d'identifier les personnes en fonction des données présentes dans le système. Une fois le traitement terminé, l'application affiche la position des personnes ainsi que leur identité si ces dernières ont réussi à être déterminées.

### Sécurité
D'un point de vue plus technique, la sécurité des communications se fait par les JWT. Pour l'initialisation, une fois que l'administrateur a rentré les données par défaut, un JWT de 15 min lui permet d'ajouter le premier administrateur. Lors d'une connexion classique, le serveur renvoie un JWT d'une durée de vie de 24 heures permettant à l'administrateur d'accéder aux autres fonctionnalités du projet. Les caméras possèdent également un JWT demandant au serveur des identifiants de connexion, une fois ces derniers vérifiés, les caméras renvoie un JWT d'une durée de vie de 24 heures. Les token sont stockés dans la base et utilisés pour les appels à l'API. À chaque appel, le serveur vérifie la durée de vie des JWT des caméras, si ce dernier est expiré, il le remplace par un nouveau en effectuant une nouvelle connexion.

## English version

### Présentation
The Space Recognition System (SRS) is a project that aims to secure a room by finding person position and their identity. In order to do that, the system uses artificial intelligence technologies that can identify and find people in an image or a video. 

### Initialisation
The administrator starts by initialisng the system. He stasrts the application, if a SRS is found, he ask th connect the administrator by using generic credentials given to him in the user manual. Ones the credentials are verified, he can add the first administrator in the system. After inputing their name and a secure password, he's redirected to the login page where it's asked to him to enter the login credentials of the admin. If they are correct, the administrator is redirected to the main page of the application.

### Configuration
The user stats by adding people in the system, he must enter their name, a picture and the type (dangerous, associate, etc.).
After that, he places the camera at each corner of the room, then, he must assign them a position, such as north/west for a camera that is at the top left of the room.  

### Space recognition

Ones the server and the camera are configured, the server gets the images captured by the cameras. The system finds the person's positions by using triangulation between the cameras, and if possible, tries to identify the peoples faces using the data in the system. Ones the processing is done, the application displays the person's position and their identity if it has been found.

### Sécurity

From a more technical point of view, the security of the communication uses the json web tokens. For the initialisation, ones the administrator has put the correct default credentials, a JWT with a 15 minute lifespan is generated. With this token, he can add the first admin in the database. Ones the administrator logins, another JWT is generated, this time with a 24 hour lifespan that gives him the rights to access the application functionality. The wifi camera got their JWT as well, when the server wants to get a picture or a video from the camera he has to login using secured credentials. Ones they are verified, a JWT is generated and given to the server. The server proceeds, then by adding this JWT to the camera in the database. For the lifespan of the token, the server will use it to get the pictures or the videos. Ones it is expired, it makes another login and update token in the database.