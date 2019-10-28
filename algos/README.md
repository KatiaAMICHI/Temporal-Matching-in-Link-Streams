Folder mainClass: une classe pour chaque algorithme différents (chaque class est documenter):
    * BBR19: algorithms décrie dans J. Baste et al, qui suit le même code dans le js (coder avec antoine roux)
    * DC (Divide and conquer heuristic) 
    * LS ( Local search heuristic)
    * greedy_algorithm (qui implement le même algorithm pour trouver un gamma-matching)
    * commonObjects: contient les deux class Edge et GammaEdge et une méthode LivingVertices qui trouver les sommets appartenant a un edge
    * DP (qui ne fonctionne pas encore)
    
Folder mains: qui contient les methods permetant de tester tous les lagorithms avec toutes les base de données présent dans res\
    * mainAllResult: contient une méthode pour tester tout les algorithms sur tous les dossiers présent dans res/ sur un nombre varier de gamma (on peut spéssifeir une base en particulier pour les test avec la variable base)
    * mainFile: pour tester tous les algorithms sur un seul fichier
    * mainReport: qui teste les algorithms que les fichier présent dans le dossier FilesRapport/ qui contient les fichiers présenter dans le rapport
    
drowResult: permet de faire des plots des résultats

maxMAtchingGraph: 
