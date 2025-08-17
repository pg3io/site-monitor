# 🌐 Site Monitor

Un outil de monitoring en temps réel pour surveiller la disponibilité de vos sites web et APIs.

## 📋 Description

Site Monitor est un outil en ligne de commande qui permet de surveiller en temps réel l'état de plusieurs sites web ou APIs simultanément. Il affiche un tableau dynamique avec les informations essentielles de chaque site :
- Horodatage du dernier check
- URL du site
- Statut (UP/DOWN avec code de retour)
- Temps de réponse
- **Trend** : Graphiques sparkline montrant l'évolution des temps de réponse

## ✨ Fonctionnalités

- 🔄 Monitoring en temps réel
- 🎨 Interface colorée et intuitive
- ⏱️ Intervalle de vérification personnalisable
- 🚦 Détection des différents types d'erreurs (Timeout, SSL, Connection)
- 📊 Affichage clair en format tableau
- 🔍 Temps de réponse précis
- 📈 **Graphiques sparkline** pour visualiser les tendances de performance

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/PG3/site-monitor.git
cd site-monitor
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 🐳 Utilisation avec Docker

### Depuis GitHub Container Registry
```bash
# Récupérer l'image
docker pull ghcr.io/pg3io/site-monitor:latest

# Lancer le monitoring avec les options par défaut
docker run ghcr.io/pg3io/site-monitor https://site1.com https://site2.com

# Lancer avec un intervalle personnalisé
docker run ghcr.io/pg3io/site-monitor --interval 5 https://site1.com https://site2.com
```

### Construction locale
```bash
# Construire l'image
docker build -t site-monitor .

# Lancer le monitoring
docker run -t site-monitor https://site1.com https://site2.com

# Lancer avec des options personnalisées
docker run -t site-monitor --interval 5 https://site1.com https://site2.com
```

## 💻 Utilisation

### Commande de base
```bash
python monitor.py https://site1.com https://site2.com
```

### Avec intervalle personnalisé
```bash
python monitor.py -i 5 https://site1.com https://site2.com
```

### Options disponibles
- `sites` : Liste des URLs à monitorer (obligatoire)
- `-i, --interval` : Intervalle de vérification en secondes (défaut: 10)

## 📸 Exemple de sortie

```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Time   ┃ Site                                     ┃  Status  ┃ Response Time ┃           Trend           ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 15:30:45 │ https://site1.com                        │ UP (200) │         145ms │    ▃▄▅▆▇█▆▅▄▃▂▁         │
│ 15:30:45 │ https://site2.com                        │ DOWN     │          N/A  │                          │
└──────────┴──────────────────────────────────────────┴──────────┴───────────────┴───────────────────────────┘
```

### 📈 Colonne Trend

La nouvelle colonne **Trend** affiche des graphiques sparkline (▁▂▃▄▅▆▇█) qui montrent l'évolution des temps de réponse en temps réel :
- Les caractères bas (▁▂) représentent des temps de réponse rapides
- Les caractères hauts (▆▇█) représentent des temps de réponse plus lents
- L'historique des 50 dernières mesures est conservé en mémoire
- Les graphiques se construisent progressivement au fil des vérifications
- L'historique est perdu à l'arrêt du programme (pas de cache persistant)

## 🛠️ Prérequis

- Python 3.6+
- Bibliothèques Python :
  - requests
  - rich

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤖 Note sur l'IA

Ce projet a été développé avec l'assistance de Claude (Anthropic), un modèle d'IA, dans le cadre d'une collaboration humain-IA pour créer un outil de monitoring efficace et maintenable.

## ✍️ Auteur

- PG3

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commit vos changements
4. Push sur la branche
5. Ouvrir une Pull Request 