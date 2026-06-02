# Holberton Web Infrastructure Lab

Lab pratique avec Vagrant + VirtualBox pour simuler une architecture web distribuée.

**100% GRATUIT — tout tourne sur ton PC local.**

## Architecture

```
+---------+        +----------------------+
|  User   | -----> |  LB (HAproxy)        |
| Browser |        |  192.168.56.10:80    |
+---------+        +----------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
    +-------------------+       +-------------------+
    |  Web1 (Nginx+App) |       |  Web2 (Nginx+App) |
    |  192.168.56.11    |       |  192.168.56.12    |
    +-------------------+       +-------------------+
              |                           |
              +-------------+-------------+
                            |
                            v
                   +-------------------+
                   |  DB (MySQL)       |
                   |  192.168.56.13    |
                   +-------------------+
```

| VM | IP | Rôle | RAM | CPU |
|---|---|---|---|---|
| lb | 192.168.56.10 | HAproxy Load Balancer (Round Robin) | 512MB | 1 |
| web1 | 192.168.56.11 | Nginx + Flask App Server | 512MB | 1 |
| web2 | 192.168.56.12 | Nginx + Flask App Server | 512MB | 1 |
| db | 192.168.56.13 | MySQL Database | 512MB | 1 |

## Prérequis

**Besoin :**
- VirtualBox (gratuit) : https://www.virtualbox.org/
- Vagrant (gratuit) : https://www.vagrantup.com/
- ~2GB de RAM libre sur ton PC
- Virtualisation activée dans le BIOS (VT-x / AMD-V)

**Installer :**
```bash
# Ubuntu/Debian
sudo apt install virtualbox vagrant

# macOS
brew install --cask virtualbox
brew install --cask vagrant

# Windows
# Télécharge les installateurs depuis les sites officiels
```

## Lancer le Lab

```bash
cd vagrant-lab
vagrant up
```

Premier lancement = télécharge l'image Ubuntu (~600MB) + provisionne les 4 VMs. Compte ~10-15 minutes.

## Tester

```bash
# Depuis ton PC (hôte), accède au load balancer
curl http://192.168.56.10
# Résultat alternatif : web1 ou web2 (Round Robin)

# Se connecter à une VM
vagrant ssh lb      # Load Balancer
vagrant ssh web1    # Web Server 1
vagrant ssh web2    # Web Server 2
vagrant ssh db      # Database

# Sur lb, vérifier HAproxy status
curl http://localhost:80
cat /etc/haproxy/haproxy.cfg

# Sur web1/web2, vérifier Nginx + Flask
systemctl status nginx
systemctl status flask-app
curl http://localhost:5000

# Sur db, vérifier MySQL
sudo mysql -u appuser -p -h 192.168.56.13
# Mot de passe : holberton123
SHOW DATABASES;
```

## Commandes Utiles

```bash
vagrant up              # Démarre toutes les VMs
vagrant halt            # Éteint toutes les VMs
vagrant destroy -f      # Supprime toutes les VMs
vagrant reload          # Redémarre et re-provisionne
vagrant status          # Voir l'état des VMs
```

## Ce que tu peux pratiquer

- **Architecture distribuée** : 4 serveurs séparés, communication réseau privé
- **Load Balancer** : HAproxy en Round Robin, 2 backends
- **Reverse Proxy** : Nginx forward vers Flask app (port 5000)
- **Database** : MySQL accessible depuis les 2 app servers
- **SSH dans chaque tier** : comprendre la séparation des responsabilités

## Whiteboard Training

Utilise ce lab pour visualiser les concepts Holberton :
1. **Dessine** l'architecture avec les IPs et flèches
2. **Explique** le flow : User → LB → Web → DB → retour
3. **Identifie** les SPOFs (ici : LB et DB sont encore des SPOFs — pas de cluster HAproxy, pas de replica DB)
4. **Simule** une panne : `vagrant halt web1` puis teste `curl http://192.168.56.10` → HAproxy redirige tout sur web2

## Nettoyage

```bash
vagrant destroy -f
```

Supprime toutes les VMs. Ton PC retrouve ses 2GB de RAM. Rien n'est laissé.

---

**Ressources :** ~2GB RAM, ~4GB disque (image Ubuntu + VMs)
**Coût :** 0€
