# 0. Simple Web Stack

![Simple Web Stack](./assets/0-simple_web_stack.png)

## Explication du schéma

**Le scénario :** Un utilisateur tape `www.foobar.com` dans son navigateur.

**Le flux de la requête :**

1. **DNS** — Le navigateur demande au DNS : "Quelle est l'IP de `www.foobar.com` ?" → Réponse : `8.8.8.8`
2. La requête HTTP arrive sur le **serveur unique**
3. **Web Server (Nginx)** — Reçoit la requête. S'il s'agit de fichiers statiques (HTML, CSS, images), il les sert directement
4. **Application Server** — Si la requête nécessite du calcul (ex: générer une page dynamique), Nginx la transmet à l'app server qui exécute le code
5. **Database (MySQL)** — Si l'application a besoin de données, elle interroge la base de données
6. La réponse remonte jusqu'à l'utilisateur

**Communication :** Le serveur communique avec l'ordinateur de l'utilisateur via le **protocole TCP/IP** (HTTP sur port 80).

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
