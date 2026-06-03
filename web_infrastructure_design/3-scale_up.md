# 3. Scale Up

![Scale Up Infrastructure](./assets/3-scale_up.png)

## Explication du schéma

**Le scénario :** Un utilisateur tape `www.foobar.com` dans son navigateur.

**Le flux complet (Aller + Retour) :**

```
Aller (Requête) :
┌─────────┐     ┌─────────┐     ┌─────────────────┐     ┌─────────────────┐
│Client   │────▶│   DNS   │────▶│  LB Cluster     │────▶│   Web Servers   │
│(Browser)│     │(Resolve)│     │  (HAproxy 1   │     │   (Nginx only)  │
└─────────┘     └─────────┘     │   HAproxy 2)    │     │                 │
                                  │  Active-Active  │     └────────┬────────┘
                                  │   Failover      │              │
                                  └─────────────────┘              ▼
                                                          ┌─────────────────┐
                                                          │  App Servers    │
                                                          │ (Gunicorn, etc.)│
                                                          └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  MySQL Cluster  │
                                                          │  Primary ───────┼──▶ Replica
                                                          │   (R+W)         │
                                                          └─────────────────┘

Retour (Réponse HTTP) :
┌─────────┐     ┌─────────┐     ┌─────────────────┐     ┌─────────────────┐
│Client   │◄────│   DNS   │◄────│  LB Cluster     │◄────│   Web Servers   │
│(Browser)│     │(Resolve)│     │  (HAproxy 1   │     │   (Nginx only)  │
└─────────┘     └─────────┘     │   HAproxy 2)    │     │                 │
                                  │  Active-Active  │     └────────▲────────┘
                                  │   Failover      │              │
                                  └─────────────────┘              │
                                                          ┌─────────────────┐
                                                          │  App Servers    │
                                                          │ (Gunicorn, etc.)│
                                                          └────────▲────────┘
                                                                   │
                                                                   │
                                                          ┌─────────────────┐
                                                          │  MySQL Cluster  │
                                                          │  Primary ◀──────┼──◀ Replica
                                                          │   (R+W)         │
                                                          └─────────────────┘
```

1. **DNS (Aller)** — Le navigateur demande au DNS : "Quelle est l'IP de `www.foobar.com` ?" → Réponse : IP virtuelle du cluster de Load Balancers
2. **LB Cluster** — HAproxy 1 ou HAproxy 2 reçoit la requête. Si un tombe, l'autre prend le relais (failover)
3. **Web Servers (Nginx)** — Servent les assets statiques et font reverse proxy vers les App Servers
4. **App Servers** — Exécutent le code métier et interroge le MySQL Cluster si besoin
5. **MySQL Cluster** — Primary gère les écritures, Replica gère les lectures
6. **Retour** — La réponse remonte : MySQL → App → Web → LB Cluster → Client

---

### Pourquoi on ajoute chaque élément

| Élément | Pourquoi on l'ajoute |
|---------|---------------------|
| **1 serveur additionnel** | Plus de redondance et de capacité |
| **2ème Load Balancer (HAproxy)** | Configuré en **cluster** avec le premier. Si un LB tombe, l'autre prend le relais automatiquement. |
| **Séparation des composants** | Chaque type de serveur fait UNE SEULE chose : web, application, ou database |

---

### Spécificités techniques

**La séparation des tiers :**

- **Serveurs Web uniquement** — Nginx. Servent les assets statiques et font le reverse-proxy vers les app servers.
- **Serveurs Application uniquement** — Exécutent le code métier (Gunicorn, uWSGI, etc.).
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
