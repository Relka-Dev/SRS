# Composant : Application

L'application sert d'interface au projet SRS. C'est ce composant qui est contact direct avec les utilisateurs finaux. Elle est en communication avec le serveur principale qui sert lui de backend.


![](../ressources/diagrams/application.png)

## Informations sur l'ordinateur de développement
`lsb_release -a `
```
Distributor ID: Ubuntu
Description:    Ubuntu 23.10
Release:        23.10
Codename:       mantic
```

## Dépendances externes

⚠️ à ajouter ⚠️

## Architecture de l'application

##### Légende
| Couleur | Type de page            | Description                                            |
|---------|-------------------------|--------------------------------------------------------|
| Violet  | Page de connexion       | Sert à s'authentifier pour le système                   |
| Gris    | Initialisation          | Pages uniquement accessible lors de l'initialisation du système |
| Orange  | Page de navigation      | Sert à naviger entre les pages                          |
| Bleu    | Page de gestion         | Sert à configurer le système                            |
| Vert    | Page de fonctionnalité  | Affiche les résultats des configurations, des calculs etc.                |

##### Diagramme

![Architercture de l'application](../ressources/diagrams/application.jpg)

## Initialisation

![](../ressources/videos/initialize.gif)


