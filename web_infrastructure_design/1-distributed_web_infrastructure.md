# 1. Distributed Web Infrastructure

![Distributed Web Infrastructure](./assets/1-distributed_web_infrastructure.png)

## Explication du schéma

**Le scénario :** Un utilisateur tape `www.foobar.com` dans son navigateur.

**Le flux complet (Aller + Retour) :**

```
Aller (Requête) :
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────────────────────┐
│Client   │────▶│   DNS   │────▶│ HAproxy │────▶│      Serveur 1 ou 2      │
│(Browser)│     │(Resolve)│     │  (LB)   │     │  ┌─────────┐  ┌────────┐ │
└─────────┘     └─────────┘     └─────────┘     │  │  Nginx  │──│  App   │ │
                                                  │  │ (Web)   │  │ Server │ │
                                                  │  └─────────┘  └────────┘ │
                                                  │              │             │
                                                  │         ┌────▼────┐        │
                                                  │         │  MySQL  │        │
                                                  │         │Primary ─┼──▶ Replica
                                                  │         │  (R+W)  │        │
                                                  │         └─────────┘        │
                                                  └──────────────────────────┘

Retour (Réponse HTTP) :
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────────────────────┐
│Client   │◄────│   DNS   │◄────│ HAproxy │◄────│      Serveur 1 ou 2      │
│(Browser)│     │(Resolve)│     │  (LB)   │     │  ┌─────────┐  ┌────────┐ │
└─────────┘     └─────────┘     └─────────┘     │  │  Nginx  │◄─│  App   │ │
                                                  │  │ (Web)   │  │ Server │ │
                                                  │  └─────────┘  └────────┘ │
                                                  │              ▲             │
                                                  │         ┌────┴────┐        │
                                                  │         │  MySQL  │        │
                                                  │         │Primary ◀─┼──◀ Replica
                                                  │         │  (R+W)  │        │
                                                  │         └─────────┘        │
                                                  └──────────────────────────┘
```

1. **DNS (Aller)** — Le navigateur demande au DNS : "Quelle est l'IP de `www.foobar.com` ?" → Réponse : IP du Load Balancer
2. **HAproxy** reçoit la requête et la distribue à un serveur (Round Robin)
3. **Nginx → App → MySQL** sur le serveur choisi
4. **Retour** — La réponse remonte : MySQL → App → Nginx → HAproxy → Client (même connexion TCP)

---

### Pourquoi on ajoute chaque élément

| Élément | Pourquoi on l'ajoute |
|---------|---------------------|
| **Load Balancer (HAproxy)** | Distribuer le traffic entre les 2 serveurs pour éviter la surcharge d'un seul |
| **2ème serveur** | Redondance + double capacité de traitement |
| **Primary-Replica MySQL** | Le Primary gère les écritures, le Replica les lectures = on peut scale les requêtes de lecture |

---

### Spécificités techniques

- **Algorithme du LB : Round Robin** — Les requêtes arrivent une par une : requête 1 → serveur 1, requête 2 → serveur 2, requête 3 → serveur 1, etc. C'est simple et équitable.

- **Active-Active vs Active-Passive :**
  - **Active-Active** (ce qu'on utilise ici) → Les deux serveurs traitent les requêtes **en même temps**. Toute la puissance est utilisée.
  - **Active-Passive** → Un serveur travaille, l'autre attend en standby. Si le premier tombe, le second prend le relais. Moins efficace mais plus simple.

- **MySQL Primary-Replica (Master-Slave) :**
  - Le **Primary** reçoit toutes les requêtes d'écriture (INSERT, UPDATE, DELETE)
  - Il écrit ces changements dans un **binary log**
  - Le **Replica** se connecte au Primary, lit le binary log, et applique les mêmes changements sur sa propre copie des données
  - C'est **asynchrone** — le Replica peut avoir un léger retard sur le Primary

- **Différence Primary vs Replica pour l'application :**
  - Le **Primary** accepte **lectures + écritures**
  - Le **Replica** accepte seulement **lectures** (read-only)

---

## Problèmes

- 🔴 **Le load balancer est un SPOF** — S'il tombe, plus de distribution = site mort
- 🔴 **Pas de firewall** — Les serveurs sont exposés directement à Internet
- 🔴 **Pas de HTTPS** — Le traffic est en clair, interceptable par un attaquant
- 🔴 **Pas de monitoring** — On ne sait pas si quelque chose est cassé ou lent
- 🔴 **Mêmes composants sur chaque serveur** — Si on veut plus de puissance DB, on est obligé d'ajouter aussi Nginx + App Server sur la même machine, ce qui n'est pas optimal
