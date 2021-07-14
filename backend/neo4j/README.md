# Initialize the Neo4j Graph
In order to initialize the Neo4j Graph the following scripts have to be executed:

* InitializeMosesBase.py -> InitializeVolltextSuche.py
    * have to be started in order.
* InitializeIsis.py
    * can be started whenever


# isis.txt
In order to define what can be found through the isis search, the .txt file defines a few types of data.
All sets of data are separated by "--!--".
* If there is no specification the System treats it as Text. In a Text, Keywords are extracted and upon finding them the entire Text is returned.
* "--S--": This is a set. If the search matches the set keywords the entire set will be returned.
    * "--D--": This is the data that will be returned.
* "--P--": The Parent that represents the Primary data. If the Parent is found all the children are returned as well.
    * "--C--": If only the Child is found, the Parent and the found child will be returned.