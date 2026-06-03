# 3. Scale Up

![Scale Up Infrastructure](./assets/3-scale_up.png)

- Un serveur contenant un web server, application server, database, et code base pour qu'il y ait de la redondance avec l'autre serveur.
- Un load balancer est ajouté pour distribuer le traffic entre les 2 serveurs (ou failover).
- Le load balancer est configuré pour avoir un setup active-active.
- Le cluster MySQL Master-Replica utilise la réplication pour garder les données synchronisées.
- Le Master database node peut accepter des lectures/écritures tandis que le Replica peut seulement accepter des lectures.
- Le load balancer est toujours un point de défaillance unique.
- Il n'y a pas de firewall sur les serveurs.
- Le traffic n'est pas encrypté.
- Il n'y a pas de monitoring.

## Avancé

- Le load balancer est configuré comme un cluster pour que si un tombe, l'autre prenne le relais.
- Des serveurs additionnels contenant un seul composant à l'intérieur (comme un web server, application server ou database).
