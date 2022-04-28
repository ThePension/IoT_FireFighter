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
