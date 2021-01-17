# Projet Python
Projet Python E3FI-2020 du premier semestre
Le dashboard représente les résultats des élections présidentielles françaises entre 1995 et 2017
## Présentation du Dashboard
### Utilisation de l'application
Une fois l'application lancée, vous aurez accès au Dashboard permettant de visualiser les différentes représentations des données. Divers composants permettent de modifier l'affichage des données, donnant ainsi une vision sur les résulats de toutes les communes et départements de France. \
![composants selection](http://privftp.esiee.fr/~fouquoir/E3/Python_Projet/example_images/composants_01.png) ![composants selection](http://privftp.esiee.fr/~fouquoir/E3/Python_Projet/example_images/composants_02.png) \
Ces options vous permettent de visualiser les données de chaque département voire de chaque commune (échelle spécifique à la carte).
Par défault, les premières données affichées sont celles de l'Ain, et le taux de participation à l'échelle nationale en 1995.
### Exemple de Dashboard
Le dashboard ci-dessous montre les données spécifiques à la Lozère en 2017. 
![composants selection](http://privftp.esiee.fr/~fouquoir/E3/Python_Projet/example_images/lozere.png)

### Durée de chargement
Le chargement de la page peut prendre quelques minutes en fonction de la puissance de votre machine. Lorsque l'onglet de l'application dans le navigateur cesse d'afficher "Updating..." , les données que vous avez sélectionnées sont toutes affichées. 

## User guide
Ces instructions permettent de faire tourner l'application sur votre machine.
### Prérequis
S'assurer que python est bien installé sur votre machine. Si ce n'est pas le cas veuillez suivre les [instructions d'installation de python](https://www.python.org/downloads/). \
\
L'application utilise plusieurs modules de python qu'il faudra s'assuer d'avoir installé pour la faire fonctionner.
```
$ pip install plotly dash dash_core_components dash_html_components pandas json io urllib requests
```
### Installation de l'application
Pour installer l'application il suffit de cloner le projet, en exécutant la commande suivante : 
````
$ git clone https://git.esiee.fr/fouquoir/projet-python.git
````

L'application peut ensuite être lancée : \
Sur Linux ou Mac OS X 
````
$ cd /path/projet-python/
$ python3 main.py
````
Sur Windows :
`````
$ cd /path/projet-python/
$ python main.py
`````
L'application tourne sur le port 8051 donc il suffit de se rendre sur localhost:8051 dans le navigateur de votre choix.

## Developper guide
### Arbre du projet 
````
projet-python/
|-- assets/
|   |-- style.css
|   |--favicon.ico
|
|-- example_images/
|   |-- composants_01.png
|   |-- composants_01.png
|   |-- expl_dashboard.png   
|   |-- lozere.png
|
|
|-- appFunctions.py
|-- main.py
|-- README.md
````
### Fonctions des fichiers
Le repertoire assets contient un fichier css qui permet de définir le style de l'appliation. Celui-ci contient des éléments personalisés et des extraits de https://codepen.io/chriddyp/pen/bWLwgP.css . \
Le repertoire example_images contient des 
Le module appFuntions.py contient des fonctions usuelles pour l'application, pour desencombrer le fichier principal.
Le fichier main.py contient le code de l'application. 
#### main.py
Ce fichier contient une application qui exploitent les données de plusieurs csv pour produire un dashboard avec Dash. Tous les csv contenant les données des csv proviennent de dava.gouv.fr dont ont la même structure, ce qui permet de facilement intégrer des nouvelles données dans l'application. 
Le code suit les recommendations de [PEP 8](https://pep8.org), donc la modification ou l'ajout d'éléments devrait se faire facilement, en lisant les commentaires et la documentation. 
## Rapport d'analyse
### Présentation
Ce projet a pour but d'analyser les résultats des élections présidentielles en France métropolitaine en fonction des départements et villes. A travers les cartes choroplèthes et les graphiques, nous avons pu créer une application qui permet de mettre en avant les disparités des votes en fonction de la zone étudiée, ainsi que son orientation politique. Les résultats obtenus ont pu confirmer certaines de nos attentes, par exemple que l'Est parisien vote à gauche et l'Ouest à droite. D'autres résultats ont été plus surprenant, comme le fait que les deux départements Corse ont un taux de participation inférieur à 75% pour toutes les élections dont nous avons exploité les données.
Les résulats obtenus sont présentés ci-dessous, en deux temps d'abord les resultats pour le taux de participation, puis pour les candidats élus.

### Le taux de participation
Le taux de participation est illustré par une carte choroplèthe et un histogramme, accompagné d'un diagramme de points, qui ensemble permettent de se donner une idée de la participation des français aux élections . Ces données montrent l'implication des français dans la vie politique. Les résultats que nous avons obtenus sont révélateurs en ce qui concerne le désintérêt de certaines régions face à une élection si importante. Si on prend l'exemple de la Corse, en regardant le nombre d'abstentions en fonction du nombre de votants, on voit qu'en moyenne pour 10 votants on a 5 abstentions. Ce résultat reflété par la carte qui montre que la participation des haute et basse Corse reste bien en dessous de tous les autres départements de la métropole. \
L'échelle départementale de la carte offre aussi la possibilité d'étudier les inégalités de participation entre les communes d'un même département. Cette vision est intéressante, puisqu'elle montre qu'au sein d'un même environnement les citoyens n'adoptent pas les mêmes comportements. Ceci est un résultat auquel nous nous attendions, puisque nous pensions retrouver un lien entre le taux de participation et le niveau de vie des citoyens. Par exemple, en Seine-Saint-Denis, les villes comme Clichy-sous-Bois qui ont la réputation d'être peu fréquentables ont un taux de participation beaucoup plus faible que les villes dites bourgeoises comme Gournay-sur-Marne. \
L'histogramme nous permet de voir que depuis le passge au quinquennat, les citoyens sont tout de même plus actif lors des élections, puisqu'à travers tous les départements, la valeurs moyenne de la participation a augementé.
### Les candidats 
La popularité des candidats est illustrée par une carte choroplèthe et un diagramme circulaire. Il est plus difficile de trouver des liens qui se poursuivent d'année en année avec le choix des candidats dans les départements, néanmoins on peut observer une tendnace pour la droite au nord du pays et pour la gauche au sud. Ceci illustre une tendance traditionnelle plus conservatrice au Nord de la France qu'au Sud. On observe aussi une tendance dans les grandes agglomérations à voter pour des candidats socialistes et dans les endroits plus ruraux pour des candidats plus conservateurs. En 2017, au second tour nous pouvons remarquer qu'une majorité des départements avec un taux de chômage élevé ont voté pour Marine Le Pen alors que les départements avec une plus grande partie de leur population employée ont préféré voter pour Emmanuel Macron. On remarque aussi suite à ces élections de 2017, l'apparition de nouveaux partis politiques, du moins au second tour, venant remplacer la dichotomie traditionelle entre le parti socialiste et les républicains. Ces nouveaux partis sont bien évidemment "La République en Marche" de Mr Macron et le "Rassemblement National" de Mme Le Pen. 
Les résultats de ces élections ont montré un penchant de plus en plus fort et régulier que les français ont pour voter pour le parti d'extrême droite.
### Conclusion
Ce Dashboard permet de mettre en évidence les résultats prévus mais aussi de dévoiler des disparités auquelles nous ne nous attendions pas. Les liens entre le niveau de vie et le rapport à la politique sont bien illustrés, et montrent qu'un effort supplémentaire devrait être fait pour que ces populations se sentent d'avantage concernées par la politique et exercent leur droit de vote. La carte choroplèthe met à la lumière du jour la montée alarmante de l'extrême droite qui prend du terrain dans les départements moins urbanisés. 
Nous attendons les prochaines élections en 2022 pour voir l'évolution de nos analyses, qui nous l'espérons seront positives. 



## Auteurs
Richard Fouquoire
Emily Renard