# Tests fonctionnels

Les tests fonctionnels sont effectués toutes les semaines afin de garantir une bonne avancée du projet. Ils permettent également de suivre l'évolution du travail.

| Test ID | Composant        | Description du Test                                                              | Résultat Attendu                                              | Méthode de Test                             |
|---------|------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------|
| T1      | Caméras Wifi     | Vérifier la capture d'image en temps réel                                        | Images et vidéos sont capturées sans retard significatif      | Observation visuelle et chronomètre          |
| T2      | Caméras Wifi     | Tester la sécurité des endpoints Flask avec JWT                                  | Accès non autorisé est refusé                                 | Tentatives d'accès avec/ sans JWT            |
| T3      | Serveur Central  | Tester le traitement et le stockage des images                                   | Images correctement traitées et stockées                      | Vérifier la sortie de traitement             |
| T4      | Serveur Central  | Tester la détection de corps et de visages                                       | Corps et visages correctement identifiés dans les images      | Comparaison avec des images test             |
| T5      | Serveur Central  | Tester la reconnaissance faciale                                                 | Visages connus sont correctement reconnus                     | Reconnaissance avec base de données          |
| T6      | Serveur Central  | Tester la recherche automatique de caméras                                       | Caméras sur le réseau correctement identifiées et connectées  | Simulation de détection de caméras en réseau |
| T7      | Serveur Central  | Tester la gestion des JWT pour les caméras                                       | Authentification sécurisée et correcte des caméras via JWT    | Test d'accès avec JWT valide et invalide     |
| T8      | Serveur Central  | Tester la gestion des utilisateurs (ajout, modification)                         | Gestion correcte des utilisateurs dans la base de données     | Ajout et modification d'utilisateur          |
| T9      | Serveur Central  | Tester l'initialisation du système (création de l'administrateur, première connexion) | Administrateur initialisé et première connexion réussie      | Processus d'initialisation                    |
| T10     | Application      | Tester la capacité de l'application à se connecter automatiquement au serveur    | Connexion automatique et réussie au démarrage de l'application | Redémarrage de l'application                  |
| T11     | Application      | Tester la gestion des utilisateurs (interface pour ajout, modification)          | Interface permet l'ajout et la modification efficace          | Tests d'interface utilisateur                 |
| T12     | Application      | Tester l'affichage des positions sur l'interface utilisateur                     | Positions correctement affichées sur l'interface              | Vérification manuelle de l'UI                |
| T13     | Infrastructure   | Tester la redondance et la résilience du réseau                                  | Système reste opérationnel malgré une panne simulée           | Simulation de panne réseau                   |
| T14     | Intégration      | Tester l'intégration de toutes les fonctionnalités du système une par une        | Toutes les fonctionnalités fonctionnent ensemble sans erreur  | Test de bout en bout                         |

## 28.03.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ❌   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   | Tests postman fonctionnels, sécurité des routes |
| T3      | Tester le traitement et le stockage des images                                   | ❌   |              |
| T4      | Tester la détection de corps et de visages                                       | ❌   |              |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ❌   |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ❌   |              |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |              |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ❌   |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ❌   |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |              |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

### Conclusion

Grâce à l'utilisation de la fonction décoratrice dans les routes de mes API Flask, je suis en capacité de les sécuriser grâce à l'utilisation des tokens JWT.

## 19.04.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ❌   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ❌   |              |
| T4      | Tester la détection de corps et de visages                                       | ❌   |              |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅   |  Fonctionnel grâce à l'utilisation de la librairie Socket.io |
| T7      | Tester la gestion des JWT pour les caméras                                       | ❌   |              |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |              |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅   |  Fonctionnel            |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅   | Connexion automatique fonctionnelle, si echec, activation d'un bouton pour une nouvelle tentative.  |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   | Uniquement l'ajout |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |              |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

### Conclusion
Socket.io me permet de rechercher le serveur ainsi que les caméras sur le réseau. J'ai également commencé l'intégration des fonctionnalités dans l'application Kivy, ce qui marque le début du travail.

## 26.04.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ❌   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ❌   |              |
| T4      | Tester la détection de corps et de visages                                       | ❌   |              |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅   | Optimisation avec l'utilisation des JWT             |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |              |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |              |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅   |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅  |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |              |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

## 03.05.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |  Utilisation de la librairie YOLOv5 |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |  Fonctionnelle + optimisation de la recherche grâce à l'asyncrone            |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   | Fonctionnelle avec gestion de l'expiration des JWT   |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   | Toujours le problème avec les multicamera en Kivy            |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |              |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

## 08.05.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |   |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |    |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |             |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |              |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

### Conclusion

Cette semaine a été consacrée au rendu intermédiaire et n'a pas connu des avancement conséquent au niveau du projet.

## 17.05.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |   |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |    |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |             |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ❌   |  Théorique mais pas testé,            | 
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |              |

### Conclusion

Cette semaine je me suis consacré à la trigonométrie bi-camera de mon projet ainsi que la rédaction d'un prototype sous opencv. J'ai également essayer de développer la version multi-utilisateurs mais cela n'était pas fonctionnel.

## 24.05.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |   |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |    |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |             |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ⚠️  |    Tests fonctionnels du modèle à une seule personne.          |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |        

### Conclusion
Je me suis consentré sur la recherche à faire de la recherche de plusieurs personnes dans l'espace. J'ai pu cependant tester la recherche de personnes avec deux caméras. J'ai également vérifié si les caméras captaient le bon angle.

1. [Recherche de l'angle avec une caméra](https://www.youtube.com/watch?v=yyQEoyNrqvA)
2. [Recherche de la position avec deux caméras](https://www.youtube.com/watch?v=f4BZxshQ2D0)


## 31.06.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |   |
| T5      | Tester la reconnaissance faciale                                                 | ❌   |              |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |  Correction du bug de la recherche automatique des caméras  |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         | ❌   |             |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ❌   |              |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ⚠️  |    Réussite de la reconnaissance spatiale (reconnaissance faciale manquante)          |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ❌   |       

### Conclusion

Grâce à la création du modèle de double triangulation, il m'est à présent possible de faire la reconnaissance avec plusieurs personnes. Cependant, ce modèles etant plus complexe, il utilise plus de ressources ce qui fait lagger un peu le programme.

1. [Test double triangulation](https://youtu.be/JMINCs2bN4M)
2. [Test multi reconnaissance](https://youtu.be/JMINCs2bN4M)

## 07.06.2024

| Test ID | Description du Test                                                              | État | Commentaires |
|---------|----------------------------------------------------------------------------------|------|--------------|
| T1      | Vérifier la capture d'image en temps réel                                        | ✅   |              |
| T2      | Tester la sécurité des endpoints Flask avec JWT                                  | ✅   |              |
| T3      | Tester le traitement et le stockage des images                                   | ✅   |              |
| T4      | Tester la détection de corps et de visages                                       | ✅   |   |
| T5      | Tester la reconnaissance faciale                                                 | ✅   |    Fontionnelle avec la librairie Face Recognition          |
| T6      | Tester la recherche automatique de caméras                                       | ✅  |              |
| T7      | Tester la gestion des JWT pour les caméras                                       | ✅   |  Correction du bug de la recherche automatique des caméras  |
| T8      | Tester la gestion des utilisateurs (ajout, modification)                         |  ⚠️   |    Modification non fonctionnelle         |
| T9      | Tester l'initialisation du système (création de l'administrateur, première connexion) | ✅    |              |
| T10     | Tester la capacité de l'application à se connecter automatiquement au serveur    | ✅    |              |
| T11     | Tester la gestion des utilisateurs (interface pour ajout, modification)          | ⚠️   |      modification non fonctionnelle        |
| T12     | Tester l'affichage des positions sur l'interface utilisateur                     | ✅   |    Reconnaissance spatiale implémentée         |
| T13     | Tester la redondance et la résilience du réseau                                  | ❌   |              |
| T14     | Tester l'intégration de toutes les fonctionnalités du système une par une        | ✅   |  

### Conclusion
L'implémentation de la reconnaissance faciale dynamique avec les données dans la base est fonctionnelle et intégrée au système. Le passage de Kivy à opencv pour les fonctionnalités est fonctionnelle.

La reconnaissance faciale est moins efficace que la détection de la position de personnes.


1. [Test de la reconnaissance faciale](https://youtu.be/IvVYjrRSz2s?si=TsdDVFazKivi8Gjx)
1. [Tests de la reconnaissance faciale à deux](https://www.youtube.com/watch?v=TRsDz8WGZxw)
3. [Tests complet de l'application](https://www.youtube.com/watch?v=RFYBNXF6DCQ)