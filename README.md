# OCR_P9 - Projet P9 - Développez une application Web en utilisant Django

### Créer un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande

---

## Présentation

[![Generic badge](https://img.shields.io/badge/Statut-Stable-<COLOR>.svg)](https://shields.io/)

Cette application permet de demander ou publier des critiques de livres ou d’articles littéraire sous forme de site internet collaboratif.<br/>
Un espace d'inscription, de connexion est obtenu en page d'accueil, l'accès aux demande de critique (Ticket) et la réalisation d'un critique littéraire (Review) n'est accessible qu'une fois connecté avec son compte.

---

## Prérequis :

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python badge](https://img.shields.io/badge/Python->=3.7-blue.svg)](https://www.python.org/)

---

## Clonage du Repository :

```shell
git clone https://github.com/Litibe/OCR_P9.git
```

---

## Environnement Virtuel :

création de l'environnement virtuel

```shell
python3 -m venv [nom_de_votre_environnement_virtuel]
```

activation de l'environnement virtuel

### Mac/Linux

```shell
source [nom_de_votre_environnement_virtuel]/bin/activate
```

### Windows

```shell
source .\[nom_de_votre_environnement_virtuel]\Scripts\activate
```

Aller dans le dossier OCR_P9 contenant les fichiers

```shell
cd OCR_P9
```

---

## Installation des packages nécessaires

```shell
pip install -r requirements.txt
```

---

## Lancement du programme :

Exécution du serveur local Django via la commande :

```shell
python manage.py runserver
```

Cette commande produit le resultat suivant :
en effet, le programme dispose d'une interface dans le terminal.

```shell
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
DATE
Django version 3.2.7, using settings 'litreview_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Vous pouvez lancer votre navigateur web avec le lien [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Connexion au Site web généré par le serveur Django :

Différents utilisateurs ont été construit pour la "démonstration" de LITReview.
Voici la liste des Idenfiants, ayant tous le mot de passe : litreview :

<ul>
<li>lionel</li>
<li>jean8597</li>
<li>jean_5679</li>
<li>sarahj</li>
<li>severine123</li>
</ul>
Possibilité de voir le serveur Django de test pour soutenance à l'adresse [http://193.26.22.227](http://193.26.22.227)

---

## Utilisation du programme :

Le site web d'application permet :

<ul>
<li>D'accéder à la page FLUX : créer une nouvelle demande ainsi qu'une nouvelle critique, suivi de ses propres demandes, ses critiques, regarder les publications des utilisateurs auxquels l'utilisateur est abonné avec possibilité de publication de nouvelle critique sur le ticket en cours de lecture.</li>
<li> D'accéder à la page POSTS : gérer de ses demandes et de ses critiques, possibilités de créer/modifier/supprimer ses tickets, et/ou critiques. Gestion de son mot de passe de connexion</li>
<li> D'accéder à la page ABONNEMENTS : suivre de nouveaux utilisateurs, modifier sa liste d'abonnements et voir qui nous suit.</li>
</ul>
