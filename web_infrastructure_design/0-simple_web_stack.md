# 0. Simple Web Stack

![Simple Web Stack](./assets/0-simple_web_stack.png)

- Un serveur est une machine physique ou virtuelle. Un serveur est généralement situé dans un data center. Un serveur fait tourner un OS.
- Le rôle d'un web server est de servir les pages web (contenu statique).
- Le rôle d'un application server est de calculer le contenu dynamique.
- Le rôle d'une database est de stocker les données de l'application.
- Le code base contient les fichiers de l'application.
- Le serveur communique sur un réseau (TCP/IP).

## Problèmes

- Ce serveur est un point de défaillance unique car rien n'est redondant.
- Le site serait temporairement indisponible quand du nouveau code est déployé et que le web server doit être redémarré.
- Cette infrastructure ne peut pas scaler et ne pourra pas gérer du traffic qui dépasserait la capacité du serveur.
