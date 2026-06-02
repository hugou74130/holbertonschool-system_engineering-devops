# Holberton Web Infrastructure Lab — Docker Version

**Alternative légère à Vagrant.** Même architecture, mais en containers Docker.

## Pourquoi Docker ?

- **Plus rapide** : ~30 secondes pour tout lancer
- **Plus léger** : pas de VMs, pas de VirtualBox
- **Natif sur Arch** : `pacman -S docker docker-compose`
- **Même résultat** : LB + 2 Web Servers + DB

## Architecture

```
User → http://localhost:8080 → HAproxy (LB)
                              ↓
                    +---------+---------+
                    |                   |
                    v                   v
               web1:5000           web2:5000
               (Flask+Nginx)      (Flask+Nginx)
                    |                   |
                    +---------+---------+
                              |
                              v
                         db:3306
                         (MySQL)
```

| Service | Rôle | Port exposé |
|---|---|---|
| `lb` | HAproxy Load Balancer (Round Robin) | `localhost:8080` |
| `web1` | Flask App Server | interne uniquement |
| `web2` | Flask App Server | interne uniquement |
| `db` | MySQL Database | interne uniquement |

## Prérequis (Arch)

```bash
sudo pacman -S docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Relog toi (déconnecte/reconnecte) pour le groupe docker
```

## Lancer le Lab

```bash
cd docker-lab
docker-compose up --build
```

Attends ~30 secondes (télécharge les images + build + démarre).

## Tester

```bash
# Depuis un autre terminal
curl http://localhost:8080
# Rafraîchis plusieurs fois — tu verras alterner entre web1 et web2

# Voir les logs
docker-compose logs -f

# Entrer dans un container
docker exec -it holberton-lb sh
docker exec -it holberton-web1 sh
docker exec -it holberton-db mysql -u appuser -p
# Mot de passe : holberton123
```

## Commandes Utiles

```bash
docker-compose up -d       # Lancer en arrière-plan
docker-compose down        # Arrêter et supprimer
docker-compose ps          # Voir l'état
docker-compose logs lb     # Voir les logs du LB
docker-compose stop        # Arrêter (conserve les containers)
docker-compose start       # Relancer
docker system prune -f     # Nettoyer tout
```

## Ce que tu peux pratiquer

- **Load Balancer** : `curl localhost:8080` plusieurs fois → Round Robin alterne entre web1/web2
- **SPOF simulation** : `docker-compose stop web1` → curl marche toujours (redirige sur web2)
- **Séparation des tiers** : chaque service est isolé, communique via le réseau Docker
- **Monitoring** : `docker stats` pour voir CPU/RAM en temps réel

## Whiteboard Training

Même exercice que pour la review Holberton :
1. Dessine l'architecture avec les flèches
2. Explique le flow : User → LB → Web → DB → retour
3. Identifie les SPOFs (ici : LB et DB sont encore des SPOFs)
4. Simule une panne : `docker-compose stop web1`, teste avec curl

## Nettoyage

```bash
docker-compose down -v   # Supprime containers + volumes + réseau
```

**Ressources :** ~200MB RAM, presque rien en disque
**Coût :** 0€ — tout est local

---

## Différence Vagrant vs Docker

| | Vagrant | Docker |
|---|---|---|
| VMs | 4 VMs complètes | 4 containers légers |
| RAM | ~2GB | ~200MB |
| Temps de lancement | ~10-15 min | ~30 sec |
| VirtualBox | Oui | Non |
| Réalisme | Plus proche du vrai serveur | Suffisant pour apprendre |

**Conseil :** Utilise Docker pour apprendre vite. Passe à Vagrant plus tard si tu veux vraiment simuler des machines physiques.
