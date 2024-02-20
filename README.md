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
    
- **Sprint 3 - Gérer le XML** : (19/02/2024 - 23/02/2024)

	Permettre au logiciel de générer des fichiers xml en plus des txt. Le choix doit etre laissé à l'utilisateur par le biais d'arguments de commandes : -x pour un xml, -t pour un txt, -a pour les deux.
	Améliorer la détection des auteurs.
	 
À chaque nouveau sprint, une nouvelle branche sera créée selon le numéro de sprint. À chaque fin de sprint, on merge la branche de main et on créé un release. Ce release contiendra l'exécutable de fin de sprint et le code source à l'heure de la fin.
