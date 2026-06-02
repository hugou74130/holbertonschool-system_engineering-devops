# Holberton Web Infrastructure Lab — Docker Version

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

