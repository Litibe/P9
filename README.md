# OCR_P9 - Projet P9 - Développez une application Web en utilisant Django

### Créer un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande

---

## Présentation

[![Generic badge](https://img.shields.io/badge/Statut-Stable-<COLOR>.svg)](https://shields.io/)

Cette application permet de demander ou publier des critiques de livres ou d’articles.
L’application présente deux cas d’utilisation principaux :
Les personnes qui demandent des critiques sur un livre ou sur un article particulier ;
Les personnes qui recherchent des articles et des livres intéressants à lire, en se basant sur les critiques des autres.

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
