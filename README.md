## Contexte

- Lorsque l'air s'assèche et que les températures sont enlevées, les risques d'incendie augmentent (copeaux, bois de la structure, ...).
- La combinaison entre les capteurs de température et d'humidité permet de déterminer les risques d'incendie.

## Objectifs

- Utiliser les capteurs de température, d'humidité et la caméra (détection de fumée ou flamme ?) dans le but de détecter un début d'incendie ou des conditions propices à un incendie.

## Éléments de solution

- PI-Cam, Capteur d'humidité / température
- MQTT
- InfluxDB
- Dashboard avec couleurs (vert = risque faible, orange = risque modéré, rouge = risque élevé, noir = incendie)
- Notifications en cas de risques élevés ou d'incendie (alarme, mail, voyant de couleur)

## Docs

Toutes la documentation utile pour le projet se trouve dans le dossier `doc`

## Déployement

Dans le dossier `depencencies` se trouvent toutes les archives utile au déploiement.

### Virtual Machine

- voir la liste des paquets dans `apt.list` et `pip.list`
- copier le dossier `src/common` et `src/concentrator`

#### Variables d'environnement

- modifier et lancer le script dans `src/concentrator/setup_environement.sh`

### Raspberry

- ajouter le repository de debian buster pour installer les dépendances de pip `/etc/apt/sources.list` et y ajouter `deb [Index of /debian](http://ftp.de.debian.org/debian) bullseye main`
- compiler python 3.7.2 avec l'archive locale dans le dossier de dépendances
- voir la liste des paquets dans `apt.list` et `pip.list`
- copier le dossier `src/common` et `src/satelite`

#### Variables d'environnement

- modifier et lancer le script dans `src/satelite/setup_environement.sh`

### Grafana

- la config du dashboard se trouve le dossier `doc`, fichier `grafana_dashboard.json`

## Lancer les clients

- sur la Machine virtuel lancer le script `concentrator/concentrator.py`
- sur le raspberry lancer le script `satelite/firefighter.py`

## Sources

- https://github.com/tobybreckon/fire-detection-cnn
