# Holberton Web Infrastructure Design — Synthèse Complète

## Acronymes à Connaître

| Acronyme | Signification | Définition Rapide |
|----------|---------------|-------------------|
| **LAMP** | Linux, Apache, MySQL, PHP/Python/Perl | Stack web classique : OS + serveur web + base de données + langage |
| **SPOF** | Single Point of Failure | Point unique de défaillance — si ça tombe, tout tombe |
| **QPS** | Queries Per Second | Requêtes par seconde — métrique de charge |

---

## Concepts Clés

### 1. Server (Serveur)
Une machine physique ou virtuelle qui fournit des ressources, services ou données à d'autres machines (clients) via un réseau. Dans notre contexte, elle héberge la stack web complète (Nginx, app server, base de données, code).

### 2. Web Server (Serveur Web — ex: Nginx)
- Reçoit les requêtes HTTP des utilisateurs
- Sert les fichiers statiques (HTML, CSS, JS, images)
- Fait du reverse proxy : transmet les requêtes dynamiques au serveur d'application
- Gère les connexions et la terminaison SSL (HTTPS)

**Web Server vs Application Server:**
| Web Server | Application Server |
|------------|-------------------|
| Sert du contenu statique | Exécute du code métier |
| Gère les connexions HTTP | Génère du contenu dynamique |
| Reverse proxy vers l'app | Communique avec la base de données |
| Nginx, Apache HTTPD | Gunicorn, uWSGI, Tomcat |

### 3. DNS (Domain Name System)
Système qui traduit les noms de domaine lisibles par l'humain (ex: `www.foobar.com`) en adresses IP numériques (ex: `8.8.8.8`). C'est l'annuaire téléphonique d'Internet.

**Types de DNS Records:**
| Record | Type | Usage |
|--------|------|-------|
| **A** | Address | Mappe un domaine vers une IPv4 |
| **AAAA** | Address (IPv6) | Mappe vers une IPv6 |
| **CNAME** | Canonical Name | Alias d'un autre domaine |
| **MX** | Mail Exchange | Serveur de messagerie |
| **TXT** | Text | Vérification, SPF, DKIM |
| **NS** | Name Server | Indique quel serveur DNS gère le domaine |

Dans `www.foobar.com`, `www` est un sous-domaine avec un **record A** pointant vers l'IP du serveur.

### 4. Database (Base de Données — ex: MySQL)
Système de gestion de données structurées. Stocke, récupère, met à jour et supprime des données. Le serveur d'application interroge la BDD pour persister l'état de l'application (utilisateurs, sessions, contenu).

### 5. Load Balancer (Répartiteur de Charge — ex: HAproxy)
Distribue le trafic entrant entre plusieurs serveurs backend. Évite la surcharge d'un seul serveur et fournit la redondance.

**Algorithmes de distribution:**
- **Round Robin** : distribue séquentiellement (serveur 1, 2, 3, 1, 2...)
- **Least Connections** : envoie vers le serveur avec le moins de connexions actives
- **IP Hash** : même client = même serveur (sessions persistantes)

### 6. Monitoring (Supervision)
Collecte de métriques, logs et événements en temps réel pour :
- Détecter les anomalies avant qu'elles n'impactent les utilisateurs
- Diagnostiquer les problèmes
- Planifier la capacité (scaling)
- Configurer des alertes sur seuils (CPU, mémoire, QPS, erreurs)

**Monitoring QPS** : parser les logs d'accès du web server (ex: logs Nginx) et compter les requêtes par seconde via une requête log dans l'outil de monitoring (ex: Sumologic).

---

## Redondance & Haute Disponibilité

### SPOF (Single Point of Failure)
Un composant unique dont la défaillance entraîne la panne de tout le système. Exemples :
- Un seul serveur (toute la stack sur une machine)
- Un seul load balancer
- Une seule base de données primaire (pour les écritures)

**Solution :** Dupliquer les composants critiques.

### High Availability Cluster

| Type | Description |
|------|-------------|
| **Active-Active** | Tous les nœuds traitent du trafic simultanément. Meilleure utilisation des ressources, mais plus complexe à synchroniser. |
| **Active-Passive** | Un nœud actif traite le trafic, l'autre est en veille. Si l'actif tombe, le passif prend le relais. Plus simple, mais gaspille des ressources. |

---

## HTTPS & Sécurité

### HTTPS (HTTP Secure)
HTTPS = HTTP + TLS/SSL (chiffrement). Il assure :
- **Confidentialité** : personne ne peut lire les données en transit
- **Intégrité** : les données ne peuvent pas être modifiées
- **Authenticité** : le client sait qu'il parle au vrai serveur (certificat)

### Firewall (Pare-feu)
Dispositif de sécurité réseau qui contrôle le trafic entrant et sortant selon des règles de sécurité. Il agit comme une barrière entre un réseau interne de confiance et un réseau externe non fiable.

---

## Déploiement Sans Downtime

**Problème :** Redémarrer le serveur web ou la base de données pour déployer du code = site indisponible.

**Solutions :**
1. **Blue-Green Deployment** : 2 environnements identiques. Déployer sur l'un, switcher le trafic, rollback instantané si problème.
2. **Rolling Deployment** : déployer sur un serveur à la fois, en maintenant les autres actifs.
3. **Load Balancer + Health Checks** : retirer un serveur du pool, déployer, le remettre quand healthy.
4. **Database Migrations** : exécuter les migrations en backward-compatible (ajouter colonne, puis changer le code, puis supprimer colonne).

---

## Architecture en 4 Étapes (Résumé Visuel)

### Étape 0 : Simple Web Stack (1 serveur)
```
User → DNS (www A → 8.8.8.8) → Server [Nginx + App + Code + MySQL]
```
**Problèmes :** SPOF total, downtime maintenance, non scalable.

### Étape 1 : Distributed (3 serveurs)
```
User → DNS → HAproxy → [Server 1 (Nginx+App+Code)] + [Server 2 (Nginx+App+Code)]
                                    ↓
                              MySQL Primary-Replica
```
**Problèmes :** LB et DB Primary = SPOFs, pas de firewall, pas de HTTPS, pas de monitoring.

### Étape 2 : Secured & Monitored (3 serveurs + sécurité)
```
User → DNS → Firewall → HAproxy (SSL) → Firewalls → [2 App Servers + Monitoring]
                                          ↓
                                    Firewall → MySQL + Monitoring
```
**Problèmes :** SSL terminé au LB (trafic interne non chiffré), 1 seul MySQL qui écrit, composants mélangés.

### Étape 3 : Scaled Up (séparation des tiers)
```
User → DNS → Firewall → [HAproxy 1] ↔ [HAproxy 2] (cluster)
                                ↓
                        Firewall → [Web Server] → [App Server] → [Database]
                        (Nginx)      (Gunicorn)      (MySQL)
```
**Avantage :** Chaque tier sur sa propre machine, scalable indépendamment, vraie séparation des responsabilités.

---



## Checklist Mentale Avant la Review

- [ ] Je peux dessiner l'architecture 0, 1, 2, 3 de tête
- [ ] Je peux expliquer chaque composant en 2 phrases max
- [ ] Je connais les 3 acronymes : LAMP, SPOF, QPS
- [ ] Je peux expliquer Active-Active vs Active-Passive
- [ ] Je peux expliquer Primary-Replica (Master-Slave)
- [ ] Je connais les 3 problèmes de chaque architecture
- [ ] Je peux dire pourquoi HTTPS > HTTP
- [ ] Je peux dire ce qu'est un firewall
- [ ] Je sais comment monitorer le QPS (parser les logs Nginx)

---
