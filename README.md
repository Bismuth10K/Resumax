# Resumax
Resumax est un parseur de PDF vers un format texte.
Ce projet est demandé par le laboratoire de l'IRISA dans le cadre d'un cours, il a pour but de simplifier la lecture d'articles scientifiques pour les chercheurs.

Ce projet doit être appliqué selon la méthode Scrum, et est créé par les deux membres de l'équipe : @Bismuth (Scrum Master) et @SwiniusRex (Dev senior). @RemyK est le représentant du client.

Voici un récapitulatif de nos sprints jusqu'à là :
- <u>Sprint 1 - Veille technologique :</u> (29/01/24 - 04/02/24)

    Chercher et comparer les outils ou librairies déjà existantes, ensuite se décider du langage et de la librairie afin de commencer le sprint suivant.
    Un rapport de deux pages est attendu afin de justifier le choix.

- <u>Sprint 2 - Début parsing :</u> (05/02/24 - 18/02/24)

    Le but de ce sprint va être de tester si notre librairie (pyMuPDF à ce jour) marche correctement.
    Nous devons réussir à extraire le nom du fichier d'origine, le titre du papier, le(s) auteur(s) et le résumé (abstract).

À chaque nouveau sprint, une nouvelle branche sera créée selon le numéro de sprint. À chaque fin de sprint, on merge la branche de main et on créé un release. Ce release contiendra l'exécutable de fin de sprint et le code source à l'heure de la fin.