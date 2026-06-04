# 3. Scale Up

![Scale Up Infrastructure](./assets/3-scale_up.png)

## Explication du schéma

**Le scénario :** Un utilisateur tape `www.foobar.com` dans son navigateur.

**Le flux de la requête :**

1. **DNS** — Le navigateur demande au DNS : "Quelle est l'IP de `www.foobar.com` ?" → Réponse : IP virtuelle du cluster de Load Balancers
2. La requête arrive sur le **Load Balancer Cluster** (HAproxy 1 ou HAproxy 2)
3. Si HAproxy 1 tombe, HAproxy 2 prend le relais automatiquement (failover)
4. Le LB distribue la requête à un **Web Server** (Nginx)
5. Nginx sert les fichiers statiques et fait reverse proxy vers un **App Server**
6. L'App Server exécute le code métier et interroge le **MySQL Cluster** si besoin
7. MySQL Primary gère les écritures, Replica gère les lectures
8. La réponse remonte jusqu'à l'utilisateur

---

### Pourquoi on ajoute chaque élément

| Élément | Pourquoi on l'ajoute |
|---------|---------------------|
| **Serveurs additionnels** | Plus de redondance et de capacité — **2 web servers, 2 app servers** |
| **2ème Load Balancer (HAproxy)** | Configuré en **cluster** avec le premier. Si un LB tombe, l'autre prend le relais automatiquement. |
| **Séparation des composants** | Chaque type de serveur fait UNE SEULE chose : web, application, ou database |

---

### Spécificités techniques

**La séparation des tiers :**

- **Serveurs Web uniquement** — Nginx. Servent les assets statiques et font le reverse-proxy vers les app servers.
  - **2 serveurs** pour la redondance et la distribution de charge
- **Serveurs Application uniquement** — Exécutent le code métier (Gunicorn, uWSGI, etc.).
  - **2 serveurs** pour la redondance et la distribution de charge
- **Serveurs Database uniquement** — MySQL Primary-Replica. Gèrent uniquement les données.

**Pourquoi séparer :** Chaque composant a des besoins de ressources différents :
- La **DB** a besoin de beaucoup de RAM et de disque rapide (SSD)
- Le **web server** a besoin de bande passante réseau
- L'**app server** a besoin de CPU

En les séparant, on peut scaler chaque tier indépendamment selon ses besoins. Ex : si le traffic augmente mais pas les écritures DB, on ajoute juste des serveurs web.

**Le LB en cluster Active-Active :**
- Les deux load balancers sont actifs simultanément
- Ils partagent la configuration et l'état
- Si un tombe, l'autre continue de distribuer le traffic — **plus de SPOF au niveau du LB**

---

## Diagramme avec icônes

```
┌─────────┐     ┌─────────┐     ┌─────────────────────────┐
│  👤     │────►│   🌐    │────►│   ⚖️ LOAD BALANCER      │
│  USER   │     │   DNS   │     │   CLUSTER               │
└─────────┘     └─────────┘     │  ┌─────────┐┌─────────┐ │
                                │  │HAProxy 1││HAProxy 2│ │
                                │  │  ⚖️    ││  ⚖️    │ │
                                │  └────┬────┘└────┬────┘ │
                                └───────┼──────────┼──────┘
                                        │          │
                              ┌─────────┘          │
                              │    ┌─────────────────┘
                              │    │
                           ┌──▼──┐┌─▼──┐
                           │ 🌐  ││ 🌐  │  ← 2 Web Servers
                           │WEB 1││WEB 2│    (Nginx)
                           │ ⚡  ││ ⚡  │
                           └──┬──┘└──┬──┘
                              │      │
                           ┌──▼──┐┌──▼──┐
                           │ ⚙️  ││ ⚙️  │  ← 2 App Servers
                           │APP 1││APP 2│    (Python)
                           │ 🐍  ││ 🐍  │
                           └──┬──┘└──┬──┘
                              │      │
                           ┌──▼──┐┌──▼──┐
                           │ 🗄️  ││ 🗄️  │  ← MySQL Cluster
                           │ DB  ││ DB  │
                           │MASTER││REPLICA│
                           │ 📝  ││ 📖  │
                           └─────┘└─────┘
```

**Légende :**
- 👤 = Utilisateur
- 🌐 = DNS / Web Server
- ⚖️ = Load Balancer (HAProxy)
- ⚡ = Nginx
- ⚙️ = Application Server
- 🐍 = Python
- 🗄️ = Database
- 📝 = Primary (écritures)
- 📖 = Replica (lectures)

---

## Récap de l'évolution

```
ÉTAPE 0 : 1 serveur tout-en-un
  ❌ SPOF | ❌ Pas de scale | ❌ Downtime déploiement

ÉTAPE 1 : 3 serveurs + LB + DB Primary-Replica
  ✅ Redondance serveurs | ✅ Scale lectures DB
  ❌ LB = SPOF | ❌ Pas de sécurité | ❌ Pas de monitoring

ÉTAPE 2 : + Firewalls + HTTPS + Monitoring
  ✅ Sécurisé | ✅ Monitoré | ✅ Encrypté
  ❌ SSL termination au LB | ❌ 1 seul Master DB | ❌ Composants mélangés

ÉTAPE 3 : Cluster LB + Tiers séparés
  ✅ Plus de SPOF LB | ✅ Scale indépendant par tier
```
