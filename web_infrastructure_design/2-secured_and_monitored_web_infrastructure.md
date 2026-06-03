# 2. Secured and Monitored Web Infrastructure

![Secured and Monitored Web Infrastructure](./assets/2-secured_and_monitored_web_infrastructure.png)

- Le firewall filtre le traffic réseau entrant et sortant d'une machine.
- L'étudiant a dessiné un firewall sur le diagramme.
- Le load balancer est un point de défaillance unique.
- HTTPS est configuré pour que si quelqu'un intercepte le traffic, il ne puisse pas le lire.
- Le monitoring peut être utilisé pour vérifier si quelque chose est cassé ou lent.
- Le setup de monitoring est composé d'un client qui collecte les données et les envoie au système de monitoring.
- Configurer le monitoring pour : collecter les données du web server ; avoir une alerte déclenchée si le QPS devient hors de contrôle.

## Problèmes

- Terminer le SSL au niveau du load balancer est un problème car le traffic entre le load balancer et les web servers n'est pas encrypté.
- N'avoir qu'un seul serveur MySQL capable d'accepter des écritures est un problème car si le master tombe, l'application ne peut plus écrire dans la database.
- Avoir les mêmes composants sur tous les serveurs (database, web server et application server) peut être un problème car leur consommation ne va pas croître de la même manière entre eux (on pourrait vouloir avoir plus de database servers que de application servers par exemple).
- Avoir les mêmes composants sur tous les serveurs peut être un problème car quand il y a de la maintenance sur un serveur pour un composant spécifique, ça affecte les autres composants qui sont dessus.
