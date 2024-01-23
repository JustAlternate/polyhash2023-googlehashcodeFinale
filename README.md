# Projet Polyhash2023 team S
============

Projet polyhash de la team S.

Utilisation du "issues_board" de gitlab pour la gestion des tickets, et politique de merge request pour avoir un suivi de projet explicite, efficace et fonctionnel grace au review.

## L'équipe
========

- Théo Masselot - theo.masselot@etu.univ-nantes.fr
- Loïc Weber - loic.weber@etu.univ-nantes.fr
- Amedeo Calcagni - amedeo.calcagni@etu.univ-nantes.fr

## Prérequis
- Python
```sh
sudo apt install python
```
- pip 
```sh
python -m ensurepip --upgrade
```

## Fonctionnement du projet
========================

Afin d'utiliser notre projet, nous conseillons vivement d'**utiliser notre Makefile** avec la commande `make`.
Celle-ci devrait permettre de faire tout ce que vous avez besoin.

- Pour installer les dépendances du projet et créer l'environnement python :
```shell
make install
```
- Pour générer toutes les solutions du dossier `challenges` avec un algorithme (polyhash.py) :
```sh
make generate theo|loic|amedeo
```
Les solutions seront écrites dans le dossier `solutions`

- Pour générer une solution en particulière avec un algorithme (polywriter.py) :
```sh
make run theo|loic|amedeo challenges/a_example.in
```
- Pour lancer notre module de tests (polytests.py) :
```sh
make tests
```
- Pour lancer nos tests de formatage (pep8 et flake8) :
```sh
make lint
```
- Pour lancer tous nos tests (linter et polytests) :
```sh
make all
```
- Pour supprimer les fichiers non essentiels :
```sh
make clean
```


