Pour lancer le programme, il suffit d'entrer la commande suivante :
flask run

Il faut également un fichier .env à ajouter que je vous donnerai par mail.


### User Story 1: Générateur de QCM
**En tant que** élève,
**Je veux** pouvoir générer un QCM basé sur le sujet que je souhaite étudier,
**Afin de** tester mes connaissances de manière interactive.

#### Critères d'acceptation:
1. L'utilisateur peut sélectionner un sujet spécifique pour le QCM.
2. Le système génère automatiquement un ensemble de questions à choix multiples basé sur le sujet sélectionné.
3. Chaque QCM produit doit être unique pour éviter la répétition des questions.

### User Story 2: Adaptation de la Difficulté
**En tant que** élève,
**Je veux** que la difficulté des questions s'adapte à mon niveau,
**Afin de** me concentrer sur l'amélioration de mes points faibles.

#### Critères d'acceptation:
1. Le système enregistre les scores des utilisateurs sur chaque QCM.
2. Le système analyse les points faibles de l'utilisateur en fonction de ses performances précédentes.
3. Les questions suivantes sont adaptées pour se concentrer davantage sur les domaines où l'utilisateur a montré des lacunes.

### User Story 3: Feedback Utilisateur sur le Contenu
**En tant que** élève,
**Je veux** pouvoir liker ou disliker les QCM et flashcards, et noter la difficulté des questions.
**Afin de** contribuer à l'amélioration de la qualité du contenu, et à la classification de ce dernier.

#### Critères d'acceptation:
1. Les utilisateurs peuvent donner un feedback positif ou négatif sur chaque QCM ou flashcard.
2. Le système utilise les feedbacks pour améliorer ou retirer le contenu de la plateforme.
3. Les contenus les mieux notés sont plus fréquemment proposés aux futurs utilisateurs.
4. Les questions sont de difficultés progressives pour les utilisateurs, en fonction des notes de difficulté données par les utilisateurs précédents.

### User Story 4: Générateur de Flashcards
**En tant que** élève,
**Je veux** avoir accès à des flashcards générées automatiquement,
**Afin de** m'aider à mémoriser les informations importantes.

#### Critères d'acceptation:
1. Le système génère des flashcards basées sur les sujets étudiés.
2. Les flashcards doivent présenter des informations clés de manière concise.
3. Les utilisateurs peuvent parcourir les flashcards à leur propre rythme.
