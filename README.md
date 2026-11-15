# MISSION ORION-7

**Étudiant(e) :** [Robert Mélodie]
**Date de remise :** dimanche 8 novembre 2026

## Objectif

Développer en autonomie un escape game spatial console en Python orienté objet.
Lire les PDF dans `../DOCUMENTATION_ETUDIANTS` avant de coder.

## Lancer le programme

```bash
python main.py
```


## Mon avis
Projet complet et intéressant mais un peu complexe. Le readMe a été générer par IA par manque de temps mais j'ai vérifier si tout était correcte

# Mission ORION-7 : escape game spatial en Python

Projet final de programmation orientée objet (Bachelor 1). Le joueur se réveille dans le sas de la station ORION-7. Il doit explorer, récupérer du matériel, redémarrer le réacteur puis évacuer depuis le poste de commande avant que l'oxygène tombe à zéro.

## Lancer le jeu

Depuis le dossier du projet :

```
python main.py
```

Aucun module externe n'est nécessaire.

## Fichiers

- `main.py` : menu, saisies (`input()`) et affichages (`print()`). C'est le seul endroit qui dialogue avec le joueur.
- `__init__.py` : toutes les classes du jeu.
- `REPONSES_POO_15_QUESTIONS.txt` : les 15 réponses de conception.

## Les classes

- **Oxygene** : garde le niveau d'oxygène (départ 48, maximum 80, jamais négatif). Méthodes : `retirer()`, `recharger()`, property `niveau`.
- **Objet** (classe mère) avec **Badge**, **Cable**, **Fusible**, **Bombonne** : chaque enfant redéfinit `utiliser(joueur, salle)` avec son propre effet.
- **Enigme** (classe mère) avec **EnigmeObjet** (le joueur possède-t-il l'objet ?) et **EnigmeCode** (le code est-il bon ?) : chaque enfant redéfinit `verifier()`.
- **Salle** : liste d'objets et de passages. Méthodes : `ajouter_objet()`, `retirer_objet()`, `trouver_objet()`, `decrire()`, `ajouter_passage()`, `passage_vers()`.
  - **Laboratoire** (hérite de Salle) : `lire_journal()`, qui donne le code du réacteur.
  - **Machines** (hérite de Salle) : `installer()`, `tenter_code()`, properties `cable_installe`, `fusible_installe`, `reacteur_actif`.
- **Passage** : relie deux salles, garde l'état verrouillé ou non. Méthodes : `est_ouvert()`, `deverouiller()`, `autre_salle()`, `essayer_deverouiller()`.
- **Joueur** : position, oxygène et inventaire. Méthodes : `ajouter_objet()`, `retirer_objet()`, `trouver_objet()`, `possede()`, `voir_inventaire()`, `changer_salle()`, `est_vivant()`, `retirer_oxygene()`, `recharger_oxygene()`.
- **GameManager** : prépare la partie (`preparer_partie()`), applique les règles et les coûts d'oxygène (`_payer()`), gère l'état de la partie (en cours, victoire, défaite).

Les 5 salles (Sas, Réserve, Laboratoire, Machines, Commande) sont créées dans `preparer_partie()`. Seules Laboratoire et Machines ont leur propre classe, les trois autres sont des instances de `Salle`.

## Actions disponibles

| N° | Action | Coût en oxygène |
|----|--------|-----------------|
| 1 | Se déplacer | 6 |
| 2 | Observer la salle | 1 |
| 3 | Lire le journal (laboratoire seulement) | 1 |
| 4 | Ramasser un objet | 2 |
| 5 | Utiliser un objet | 2 |
| 6 | Tenter un code (machines seulement) | 3 |
| 7 | Évacuer (commande seulement) | 3 |
| 8 | Attendre | 5 |
| 9 | Aide | 0 |
| 10 | État | 0 |
| 11 | Inventaire | 0 |

Une action impossible ne doit pas déplacer le joueur ni modifier le monde.

## Procédure pour gagner

Le code du réacteur est `8259`. Il se trouve dans le journal du laboratoire.

1. Aller à la réserve, ramasser le **Badge** et le **Cable**.
2. Revenir au sas, puis aller au laboratoire.
3. Ramasser le **Fusible** et la **Bombonne**, puis lire le journal (on découvre le code).
4. Utiliser la **Bombonne** (+30 d'oxygène).
5. Utiliser le **Badge** : la porte vers les machines se déverrouille.
6. Aller aux machines, utiliser le **Cable** puis le **Fusible**.
7. Tenter le code `8259` : le réacteur démarre et la porte vers la commande se déverrouille.
8. Aller à la commande et évacuer : **victoire**.

Parcours de référence : il reste environ 22 unités d'oxygène à la fin.

## Procédure pour perdre

Depuis le début, choisir **Attendre** 10 fois de suite (5 d'oxygène chaque fois). L'oxygène tombe à 0, la partie s'arrête et c'est une **défaite**.

## Vérifications effectuées

Chaque scénario du cahier des charges est testé en jouant. Ce tableau donne le test fait et le résultat attendu.

| N° | Scénario | Ce que j'ai fait | Résultat attendu |
|----|----------|------------------|------------------|
| 1 | Du sas, accès au laboratoire et à la réserve | Se déplacer vers la réserve, revenir, aller au laboratoire | Déplacements acceptés |
| 2 | Machines fermées sans badge | Depuis le laboratoire, aller aux machines sans avoir utilisé le badge | Refus, le joueur reste au laboratoire, 0 oxygène dépensé |
| 3 | Objet collecté : plus dans la salle | Ramasser le badge, puis essayer de le ramasser encore | Deuxième tentative refusée, la salle ne contient plus le badge |
| 4 | Objet absent : inutilisable | Utiliser le fusible sans l'avoir ramassé | Refus, rien ne se passe |
| 5 | Badge durable | Utiliser le badge, regarder l'inventaire, puis le réutiliser | Le badge reste dans l'inventaire, la porte reste ouverte |
| 6 | Un seul composant ne suffit pas | Installer le câble seulement, tenter le bon code | Réacteur toujours éteint |
| 7 | Code erroné | Tenter un faux code avec les deux composants installés | Réacteur éteint, 3 d'oxygène dépensés |
| 8 | Bon code : réacteur actif | Tenter `8259` avec câble et fusible installés | Réacteur démarré |
| 9 | Commande fermée avant le réacteur | Aller à la commande avant le code | Refus |
| 10 | Bombonne à usage unique | L'utiliser deux fois | Une seule recharge de 30, niveau jamais au-dessus de 80 |
| 11 | Oxygène jamais négatif | Attendre jusqu'à 0 | Défaite, la partie s'arrête, aucune action possible |
| 12 | Évacuation depuis la commande | Évacuer avec le réacteur actif et de l'oxygène | Victoire |
| 13 | Commande invalide ou action impossible | Choix inconnu dans le menu, aller dans une salle sans passage, ramasser un objet absent, tenter un code hors des machines, évacuer hors de la commande | Aucun changement, 0 oxygène dépensé |
| 13 (partiel) | Utilisation impossible d'un objet | Utiliser le badge hors du laboratoire | Refus, mais 2 d'oxygène sont dépensés : non conforme (voir Limites connues) |
| 14 | Consultations gratuites | Aide, état, inventaire, puis lire le journal | 0 oxygène pour les consultations, 1 pour le journal |
| 15 | Victoire et défaite reproductibles | Les deux procédures ci-dessus | Victoire et défaite obtenues |

## Choix de conception

- Une classe `Passage` partagée par deux salles : l'état verrouillé est à un seul endroit et le déverrouillage vaut dans les deux sens.
- Les règles sont dans les classes concernées (`Badge.utiliser()`, `EnigmeCode.verifier()`), le `GameManager` appelle seulement les méthodes.
- L'oxygène est protégé dans la classe `Oxygene`. Il n'est modifié que par `retirer()` et `recharger()`.
- `main.py` est le seul fichier qui utilise `input()` et `print()` : les autres classes renvoient des textes ou des booléens.

## Limites connues

- Utiliser un objet quand l'usage est impossible (par exemple le badge hors du laboratoire) peut encore dépenser 2 d'oxygène, alors que le cahier des charges demande 0.
- Le code du réacteur est fixe (`8259`).