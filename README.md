# 🌐 Site Monitor

Un outil de monitoring en temps réel pour surveiller la disponibilité de vos sites web et APIs.

## 📋 Description

Site Monitor est un outil en ligne de commande qui permet de surveiller en temps réel l'état de plusieurs sites web ou APIs simultanément. Il affiche un tableau dynamique avec les informations essentielles de chaque site :
- Horodatage du dernier check
- URL du site
- Statut (UP/DOWN avec code de retour)
- Temps de réponse

## ✨ Fonctionnalités

- 🔄 Monitoring en temps réel
- 🎨 Interface colorée et intuitive
- ⏱️ Intervalle de vérification personnalisable
- 🚦 Détection des différents types d'erreurs (Timeout, SSL, Connection)
- 📊 Affichage clair en format tableau
- 🔍 Temps de réponse précis

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
╭────────────────────────────────────────────────────────────────────────╮
│   Website Monitoring | Last Check: 2024-01-20 15:30:45 | Interval: 10s │
├──────────┬─────────────────┬────────────────┬──────────────────────────┤
│   Time   │      Site       │     Status     │      Response Time       │
├──────────┼─────────────────┼────────────────┼──────────────────────────┤
│ 15:30:45 │ https://site1.com │   UP (200)    │         145ms           │
│ 15:30:45 │ https://site2.com │ DOWN (Timeout) │          N/A            │
╰──────────┴─────────────────┴────────────────┴──────────────────────────╯
```

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