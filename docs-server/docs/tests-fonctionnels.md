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
