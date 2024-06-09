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