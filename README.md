   # 🤖 Mon Premier Agent IA

   Un agent conversationnel intelligent développé en Python, capable d'utiliser des outils (Function Calling) pour répondre précisément aux questions. Ce projet est conçu pour être **100% gratuit** et robuste face aux blocages réseau.

   ## ✨ Fonctionnalités
   - **Outil de calcul** : Résout des expressions mathématiques.
   - **Outil temporel** : Donne l'heure et la date actuelles.
   - **API Gratuite** : Utilise l'API OpenRouter pour un accès sans carte bancaire.
   - **Robustesse Réseau** : Contourne les blocages SSL des antivirus via `curl.exe`.

   ## 🚀 Installation

   1. Clonez ce dépôt :
      ```bash
      git clone https://github.com/VOTRE_PSEUDO/mon-premier-agent.git
      cd mon-premier-agent
      ```
   2. Installez la dépendance :
      ```bash
      pip install python-dotenv
      ```
   3. Configurez votre clé API :
      - Créez un fichier `.env` à la racine du projet.
      - Ajoutez votre clé OpenRouter : `OPENROUTER_API_KEY=sk-or-v1-...`

   ## 💻 Utilisation
   ```bash
   python agent.py