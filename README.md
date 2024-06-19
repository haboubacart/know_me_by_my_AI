## Description du Projet
Boubé AI est un assistant virtuel conçu pour répondre aux questions des recruteurs sur le profil d'une personne. L'objectif est qu'il fournisse des réponses détaillées, convaincantes et personnalisées en mettant en valeur les éléments clés de son parcours professionnel, ses compétences et ses réalisations. 
Le projet Flask pour le backend, GPT-4o pour le traitement du langage naturel avancé, et FAISS pour la recherche et l'indexation efficace des informations.


## Technologies Utilisées
- **Flask :** Framework web utilisé pour développer l'application backend de Boubé AI.
- **GPT-4o :** Modèle de génération de texte avancé utilisé pour comprendre et générer des réponses basées sur le contexte des questions posées.
- **Sentence-camembert-large :** Modèle pour l'embedding 
- **FAISS :** Bibliothèque utilisée pour l'indexation rapide et la recherche de données, assurant des réponses efficaces et rapides.

## Structure du Code

Le projet est structuré de la manière suivante :

- **app.py :** Fichier principal contenant la logique de l'application Flask.
- **chatbot/templates/** : Répertoire contenant les templates HTML utilisés pour la présentation des réponses.
- **chatbot/static/** : Répertoire contenant les fichiers statiques tels que les images ou les fichiers CSS.
- **chatbot/src/chatbot.py :** Fichier contenant la logique de l'assistant virtuel utilisant GPT-4o.
- **chatbot/src/token_manager.py :** Fichier contenant la logique de génération de connexion à l'interface de chat.
- **train_vectorestore.ipynb :** Notebook pour entrainer le vectorestore du retriever FAISS

## Comment Utiliser le Projet
Pour lancer l'app (avec docker):
1. Installez les dépendances listées dans ` chatbot/requirements.txt` en lançant : pip install -r  chatbot/requirements.txt depuis le dossier
2. Entrainer le vectorestore : assurer vous d'avoir un fichier base de compétence (base_cometence.txt ou base_competence.md), votre fichier CV detaillé ou portfolio en format texte ou markdown
3. lancer la commande : docker-composer up afin de générer puis exécuter l'image de l'application qui démarre sur la page de connexion
4. Accéder à l'adresse (127.0.0.1:8080/generate_token) afin de générer le token de connexion 
5. Renseinger le token génér& sur la page d'authentification (27.0.0.1:8080/). La session (token) expire au bout de 10 mins après authentification