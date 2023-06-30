Projet Final

# Projet spécial
## Développement d'un outil d'aide à la prise de décision pour un pilote d'avion en détresse
***
## Table des matières
1. [Informations générales](#informations-générales)
2. [Installation et execution du projet](#installation-et-execution-du-projet)
3. [Options ajoutées](#options-ajoutées)
4. [Méthodes d'utilisation du fichier](#méthode-d'utilisation-du-fichier)
5. [Méthodes d'utilisation des options](#méthode-d'utilisation-des-options)
6. [Références](#références)
***
### Informations générales
***
L’objectif de ce projet est de fournir un programme permettant à un pilote d’avion 
survolant le Québec de déterminer les aéroports québécois sur lesquels il pourrait atterrir en cas 
d’urgence en fonction de sa position au moment de l’alerte.
Pour cela, différents types de paramètres sont pris en compte : 
- Les paramètres de l’avion.
- Les paramètres des aéroports québécois.
- Certains paramètres météorologiques.

Les paramètres utilisateurs sont les suivants : 
- La position GPS et l'altitude de l'avion
- Le cap suivi
- La vitesse
- La vitesse de l'avion en vol plané
- Le type d'avarie (moteur utilisable ou non)
- La quantité de carburant restante
- La distance de roulage minimum à l'atterrissage
- La finesse de l'avion


Vous retrouverez, dans ce fichier, une description des fonctionnalités qu'il présente, des données prises en compte, des hypothèses faites ainsi que la méthode de détermination des résultats.
***
### Installation et execution du projet
***
"""Dans ce dépôt, vous pouvez retrouver différents fichiers qui seront indispensables pour faire fonctionner ce projet :

* Un fichier README.md, décrivant le projet et la méthode d'utilisation (que vous êtes en train de lire actuellement). 
* Un dossier SolutionAtterrissage contenant tous les modules nécessaires pour l'utilisation du programme
* Un fichier main.py faisant appel aux modules contenus dans le dossier SolutionAtterrissage permettant d'exécuter le programme

Pour faire fonctionner le fichier, il faut télécharger (au minimum) les fichiers main.py et le dossier SolutionAtterrissage dans lequel se trouve tous les modules utilisés. 

Une fois l'installation de Prusa-Slicer terminée, il faut ouvrir le fichier '.STL' avec ce logiciel et générer le g-code correspondant. Puis, une fois que le g-code généré est enregistré sous un fichier '.gcode', vous pouvez ouvrir et exécuter le fichier python (des explications spécifiques sur l'utilisation du fichier python sont données par la suite). Enfin, une fois exécuté, vous aurez, dans le dossier où se trouve le fichier python, un nouveau fichier '.gcode' comportant les modifications et ayant la mention 'modifie'."""
***
### Options ajoutées
***
Le fichier python permet à l'utilisateur de rendre plus modulable et personnalisable la fabrication de pièces par l'imprimante 3D. Pour cela, cinq options ont été développées :
* La possibilité d'avoir une température variable en fonction des couches (variabilité linéaire par morceaux).

    ![image](https://github.com/NatGitEts/Mini_Projet_A_Groupe_L/assets/133153776/f0a53285-11b1-4793-9f37-c1f1c48f7dc5)

* La possibilité d'avoir une vitesse d'impression variable (variabilité en pourcentage de la vitesse de base).
* La possibilité de sur-extruder ou sous-extruder sur des intervalles et cela dépendemment de la température et de la vitesse sur l'intervalle.
* La possibilité de déplacer l'emplacement de début d'impression sur la zone disponible (déplacement du point d'origine X et Y).
* La possibilité d'ajouter un deuxième passage sans extrusion, à chaque couche d'impression, afin de réchauffer la couche venant d'être imprimée et d'améliorer la consolidation de la pièce. 

    ![image](https://github.com/NatGitEts/Mini_Projet_A_Groupe_L/assets/133153776/67887c39-be15-461e-b83e-17289f8c6aca)

***
### Méthodes d'utilisation du fichier
***
Le fichier ".py" que vous pouvez retrouver sur ce dépôt GitHub regroupe toutes les fonctions permettant de modifier le g-code voulu.
Le fichier a besoin d'un fichier ".gcode" en entrée qui est celui auquel vous voulez apporter des modifications (ici : *"xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode"*)

Ensuite, le code va vous demander une suite de données à fournir qui seront essentielles pour que les modifications soient implémentées correctement dans votre g-code. Chaque donnée à fournir est décrite sur la manière et les unités à utiliser.

La première entrée qui est demandée est le nombre de phase. Ce nombre correspond au nombre de différentes phases d'évolution des vitesses et températures.
De plus, il est tout à fait possible pour vous de ne pas déplacer le lieu d'impression.

Enfin, le code fournit en sortie un nouveau fichier ".gcode" comportant l'ensemble des modifications que vous avez voulu implémenter. 
***
### Méthodes d'utilisation des options
***
Les options présentées précédemment auront une influence sur le résultat d'impression. Afin que vous en fassiez le meilleur usage, voici des explications sur leur fonctionnement et sur leur méthode d'utilisation.

* La variation de la température : Il est possible de faire varier la température linéairement de manière croissante ou décroissante sur plusieurs couches d'impression. Il est également possible de changer le type de variation pour chaque phase définie. Ainsi, il vous sera possible de fixer la température d'entrée et la température de sortie pour chacune des phases. 

* La variation de vitesse : De la même manière que pour la température, il est possible de faire varier la vitesse d'un certain pourcentage en partant d'une vitesse d'entrée et allant jusqu'à une vitesse de sortie. Cette modification n'affecte que la vitesse lors de l'impression et non lors des mouvements sans sortie de matière. On peut effectuer des variations de vitesse différentes pour chaque phase créée.

* La variation de la quantité de matière extrudée : Dépendemment de la vitesse et de la température lors de l'impression, la buse va sortir plus ou moins de matière pour palier au phénomène de gonflement de l'extrudat. Par exemple, si la vitesse augmente pour une température fixe, il y aura un gonflement plus important et donc on fera en sorte que la buse envoie moins de matière (sous-extrusion) et inversement. Cette modification se réalise automatiquement en fonction des paramètres de température et de vitesse que vous aurez entrés initialement.

* Le changement de l'origine : Initialement, l'impression centre l'objet d'impression au milieu du lit. Mais, il est possible de modifier la position du début de l'impression sur la zone à disposition. Pour cela, il vous sera demandé d'entrer les distances de décalage selon x et y par rapport à la position de base. Ces distances sont en millimètres. Il est recommandé de faire attention à ne pas dépasser les distances atteignables par la buse et à ne pas entrer des distances amenant en dehors des dimensions de la zone d'impression.
  Si vous ne voulez pas décaler la position d'impression de votre pièce, c'est possible. Il suffit d'entrer "non" lorsqu'il vous est demandé.

* Le deuxième passage sans extrusion : Par défaut, cette fonction n'est pas active. Ce code python vous permet donc d'ajouter automatiquement un second passage après chaque couche qui chauffe la couche tout juste imprimée. Ce second passage est automatiquement adapté à l'objet souhaitant être imprimé.
***
## Références
***
Les lien pour accéder aux bases de données utilisées dans le code sont répertoriés ci-dessous : 
• Aéroport - Piste - Aéroport - Piste - Données Québec. 
https://www.donneesquebec.ca/recherche/dataset/aeroportpiste/resource/b66e3e23-10af-457d-b95e-b5011126fba
• Windy.com. Wind map & weather forecast - https://www.windy.com
