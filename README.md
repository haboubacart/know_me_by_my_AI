## Description du Projet
Ce projet est un assistant virtuel intelligent conçu pour répondre aux questions des recruteurs sur le profil d'une personne. Il est développé à l'aide d'un **RAG implémenté sur un le portfolio ou CV détaillé, servant de base contextuelle**. L'objectif est qu'il fournisse des réponses détaillées, convaincantes et personnalisées en mettant en valeur les éléments clés de son parcours professionnel, ses compétences et ses réalisations. Le projet utilise Flask pour le backend, GPT-4o pour le traitement du langage naturel avancé, et FAISS pour la recherche et l'indexation efficace des informations.

## Technologies Utilisées
- **Flask :** Framework web utilisé pour développer l'application backend de Boubé AI.
- **GPT-4o :** Modèle de génération de texte avancé utilisé pour comprendre et générer des réponses basées sur le contexte des questions posées.
- **Sentence-camembert-large :** Modèle pour l'embedding.
- **FAISS :** Bibliothèque utilisée pour l'indexation rapide et la recherche de données, assurant des réponses efficaces et rapides.

## Structure du Code

Le projet est structuré de la manière suivante :

- **app.py :** Fichier principal contenant la logique de l'application Flask.
- **chatbot/templates/** : Répertoire contenant les templates HTML utilisés pour la présentation des réponses.
- **chatbot/static/** : Répertoire contenant les fichiers statiques tels que les images ou les fichiers CSS.
- **chatbot/src/chatbot.py :** Fichier contenant la logique de l'assistant virtuel utilisant GPT-4o.
- **chatbot/src/token_manager.py :** Fichier contenant la logique de génération de connexion à l'interface de chat.
- **train_vectorestore.ipynb :** Notebook pour entraîner le vectorestore du retriever FAISS.

## Comment Utiliser le Projet
Pour lancer l'application (avec Docker) :

1. Installez les dépendances listées dans `chatbot/requirements.txt` :
    ```sh
    pip install -r chatbot/requirements.txt
    ```

2. Entraînez le vectorestore : assurez-vous d'avoir un fichier base de compétence (`base_cometence.txt` ou `base_competence.md`) à la racine du projet, représentant votre CV détaillé ou portfolio en format texte ou markdown.

3. Lancez la commande suivante pour générer puis exécuter l'image de l'application qui démarre sur la page de connexion :
    ```sh
    docker-compose up
    ```

4. Accédez à l'adresse suivante pour générer le token de connexion :
    ```
    http://127.0.0.1:8080/generate_token
    ```

5. Renseignez le token généré sur la page d'authentification :
    ```
    http://127.0.0.1:8080/
    ```
   Note : La session (token) expire au bout de 10 minutes après authentification.
