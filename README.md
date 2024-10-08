# Système de reconnaissance spatiale (SRS)

![Logo](./docs-server/docs/ressources/images/logo.png)

## Introduction
Le SRS (Système de Reconnaissance Spatiale) est un projet destiné à localiser précisément les individus dans un environnement 3D et à présenter visuellement leur position en 2D en utilisant des caméras WiFi et des technologies de reconnaissance faciale.

## Navigation

Utilisez ces liens pour naviguer entre les répertoires du projet.

### Documentation
- [**Accueil documentation**](./docs-server/docs/index.md)  
- [Tests fonctionnels](./docs-server/docs/tests-fonctionnels.md)  
- [Journal de bord](./docs-server/docs/jdb.md)  

### Sources
Lien vers les sources des différents composants ainsi que leurs tests.

| Composant        | Sources                                    | Tests                                |
|------------------|--------------------------------------------|--------------------------------------|
| Cameras Wifi     | [Sources](./src/cameras_wifi/src/)        | [Tests](./src/cameras_wifi/tests/)  |
| Serveur Central | [Sources](./src/serveur_central/src/)     | [Tests](./src/serveur_central/tests/) |
| Application      | [Sources](./src/application_multiplateforme/) | N/A                                  |

### Poster

- [Poster](./docs-server/docs/ressources/poster/)

## Normalisation des push

La normalisation des push permet d'augementer la lisibilité dans l'historique des intéractions avec le repertoire du projet.  

| **Syntaxe** | **Domaine de modification**                                    |
|-------------|----------------------------------------------------------------|
| Code        | Code / Fonctionnalités                                         |
| Docs        | Documentation / Lisibilité du projet (ReadMe, etc.)            |
| Struct      | Structure                                                      |
| Mixed       | Plusieurs domaines changés (Description détaillée recommandée) |
| Hotfix      | Modification rapide visant à réparer une erreur ou un bug      |