# 0. Simple Web Stack

![Simple Web Stack](./assets/0-simple_web_stack.png)

## Explication du schéma

**Le scénario :** Un utilisateur tape `www.foobar.com` dans son navigateur.

**Le flux complet (Aller + Retour) :**

```
Aller (Requête) :
┌─────────┐     ┌─────────┐     ┌─────────────────────────────────────────┐
│Client   │────▶│   DNS   │────▶│           Serveur Unique                │
│(Browser)│     │(Resolve)│     │  ┌─────────┐  ┌─────────┐  ┌────────┐  │
└─────────┘     └─────────┘     │  │  Nginx  │──│   App   │──│ MySQL  │  │
                                  │  │ (Web)   │  │ Server  │  │ (DB)   │  │
                                  │  └─────────┘  └─────────┘  └────────┘  │
                                  └─────────────────────────────────────────┘

Retour (Réponse HTTP) :
┌─────────┐     ┌─────────┐     ┌─────────────────────────────────────────┐
│Client   │◄────│   DNS   │◄────│           Serveur Unique                │
│(Browser)│     │(Resolve)│     │  ┌─────────┐  ┌─────────┐  ┌────────┐  │
└─────────┘     └─────────┘     │  │  Nginx  │◄─│   App   │◄─│ MySQL  │  │
                                  │  │ (Web)   │  │ Server  │  │ (DB)   │  │
                                  │  └─────────┘  └─────────┘  └────────┘  │
                                  └─────────────────────────────────────────┘
```

1. **DNS (Aller)** — Le navigateur demande au DNS : "Quelle est l'IP de `www.foobar.com` ?" → Réponse : `8.8.8.8`
2. **Requête HTTP** arrive sur le **serveur unique**
3. **Nginx (Web Server)** — Reçoit la requête. Si c'est du statique, il sert directement
4. **App Server** — Si c'est du dynamique, Nginx transmet à l'app server
5. **MySQL** — Si besoin de données, l'app server interroge la DB
6. **Retour** — La réponse remonte : MySQL → App → Nginx → puis repart au client via la **même connexion TCP**

**Communication :** Le serveur communique avec l'ordinateur de l'utilisateur via le **protocole TCP/IP** (HTTP sur port 80). La réponse utilise la **même connexion TCP** établie par la requête.

---

### Définitions des composants

- **Un serveur** est une machine physique ou virtuelle, généralement située dans un data center, qui fait tourner un OS.
- **Le rôle du domaine** (`www.foobar.com`) est de fournir un nom humainement lisible qui pointe vers l'IP du serveur via le DNS.
- **`www.foobar.com` est un A record** car il résout directement en une adresse IP (`8.8.8.8`).
- **Le rôle du web server (Nginx)** est de servir les pages web et le contenu statique (HTML, CSS, images).
- **Le rôle de l'application server** est de calculer le contenu dynamique (exécuter le code métier).
- **Le rôle de la database (MySQL)** est de stocker les données persistantes de l'application.
- **Le code base** contient les fichiers de l'application.
- **Le serveur communique** avec l'ordinateur de l'utilisateur via le réseau (protocole TCP/IP).

---

## Problèmes

- 🔴 **SPOF (Single Point of Failure)** — Un seul serveur. Si la machine tombe, le site est mort. Pas de backup.
- 🔴 **Downtime au déploiement** — Quand on déploie du nouveau code, il faut redémarrer Nginx. Le site est offline pendant ce temps.
- 🔴 **Impossible de scaler** — Si le traffic augmente, le serveur sature. On ne peut pas ajouter de capacité sans tout refaire.
