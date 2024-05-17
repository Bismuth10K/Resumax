# Resumax
Resumax est un parseur de PDF vers un format texte.
Ce projet est demandé par le laboratoire de l'IRISA dans le cadre d'un cours, il a pour but de simplifier la lecture d'articles scientifiques pour les chercheurs.

Ce projet doit être appliqué selon la méthode Scrum, et est créé par les deux membres de l'équipe : [@Bismuth](https://github.com/Bismuth10K) (Scrum Master) et [@SwiniusRex](https://github.com/SwiniusRex) (Dev senior). [@RemyK](https://github.com/RemyK) est le représentant du client.

Voici un récapitulatif de nos sprints jusqu'à là :
- **Sprint 1 - Veille technologique** : (29/01/24 - 04/02/24)

    Chercher et comparer les outils ou librairies déjà existantes, ensuite se décider du langage et de la librairie afin de commencer le sprint suivant.
    Un rapport de deux pages est attendu afin de justifier le choix.

- **Sprint 2 - Début parsing** : (05/02/24 - 18/02/24)

    Le but de ce sprint va être de tester si notre librairie (pyMuPDF à ce jour) marche correctement.
    Nous devons réussir à extraire le nom du fichier d'origine, le titre du papier, le(s) auteur(s) et le résumé (abstract).
    
- **Sprint 3 - Gérer le XML** : (19/02/2024 - 25/02/2024)

	Permettre au logiciel de générer des fichiers xml en plus des txt. Le choix doit etre laissé à l'utilisateur par le biais d'arguments de commandes : -x pour un xml, -t pour un txt, -a pour les deux.
	Améliorer la détection des auteurs.

- **Sprint 4 - Dette technique et amélioration des résultats** : (26/02/2024 - 24/03/2024, point intermédiaire le 12/03)

    Dans un premier temps, rattraper la dette technique.
    C'est-à-dire retravailler le code pour le rendre plus performant et maintenable.
    Ainsi, il sera plus facile de rajouter des nouvelles fonctionnalités.
    
    Dans un second temps, améliorer la détection des auteurs où il faut extraire les noms des laboratoires et les mails.
    Puis ajouter l'introduction, le corps, la conclusion et la discussion.

    Et enfin, ajouter le menu textuel.

- **Sprint 5 - Évaluation de la qualité** : (25/03/2024 - 31/03/2024)

    Le but de ce sprint est d'évaluer la qualité et la précision des rendus du parser à l'aide du site développé par le client.

- **Sprint 6 - Dernier sprint** : (02/04/24 - 14/05/24, point intermédiaire le 29/04)

    Dernier sprint, nous avons un nouveau jeu de 10 pdf.
    Nous devons *fine-tune* notre parseur afin d'avoir le meilleur score possible.
    Ensuite, nous devons rédiger un rapport dans le style d'un article scientifique où nous expliquons la façon dont nous avons procédé.

À chaque nouveau sprint, une nouvelle branche sera créée selon le numéro de sprint. À chaque fin de sprint, on merge la branche de main et on créé un release. Ce release contiendra l'exécutable de fin de sprint et le code source à l'heure de la fin.

## Lancement
Pour exécuter Resumax, il est recommandé de créer une venv python.
Ouvrez votre terminal, allez `CODE/Resumax/` à partir de la racine du projet, puis tapez les commandes suivantes :

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install python-dateutil
$ pip install PyMuPDF
```

Vous aurez donc un dossier `.venv/` dans le dossier `Resumax/` contenant les librairies necéssaires à l'exécution du script.

Pour l'exécuter, allez dans le dossier `CODE/Resumax/`, vérifier si la venv est bien activée (normalement, vous verrez son nom en début de ligne dans votre terminal, mais cela dépend probablement des terminaux).
Puis lancez la commande suivante :

```bash
python main.py -t # Output en txt seulement
python main.py -x # Output en xml seulement
python main.py -a # Output en txt et en xml
```

Vous trouverez les résultats dans le dossier `../output/` en partant du dossier contenant le code.

Le code traite automatiquement tous les .pdf appartenant au dossier `CODE/ressources/` à partir de la racine du projet. 
Libre à vous d'y mettre vos .pdf.

## Résultats
Pour l'instant, le parser ne récupère que le titre, les auteurs (avec une distinction auteur et mail), l'abstract et les références (résultat attendu du sprint 3).

