# Plan pour la vu isometric
L'idee est de travailler sur tout le jeu avec notre systeme de grille en 2D et donc vu de haut ( vue aerienne )
```unset
   r o w s
 c [][][][]
 o [][][][]  ---> tout le jeu est base dessus ( COLS and ROWS )
 l [][][][]
 s [][][][]
```
Tout notre systeme de position ne sera definis que par des `[col, row]` et non pas des `(x, y)` en pixels
car je definis que tout est caller par rapport a la grille et les cases qui la compose.

on peux donc faire un simple system de deplacement avec un dico de direction
```python
MOVES = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
}

class Chicken:
    ...
    def move(self, dcol: int, drow: int) -> None:
        """Permet de faire bouger notre chickene et de mettre a jour notre image de face_dir"""
        self.col += dcol
        self.row += drow
        self.img = self.face_dir[(dcol, drow)].copy() # on a comme cle un tuple[int, int] et plus un str

class App:
    ...
    def on_events(self) -> None:
        for event in pg.event.get():
            ...
            # permet avec un ligne de gere les 4 directions du chicken
            if event.type == pg.KEYDOWN and event.key in MOVES:
                self.chicken.move(*MOVES[event.key])
```
ensuite et seulement lors de la prise de vu par la camera tout va etre afficher en fonction des parametres choisis
par cette derniere on applique les coordonne de l'ecran et la transformation isometric est gere par un petit code a par [iso.py](src/utils/iso.py).

## Pour resumer
Dans le jeu on aura deux type de coordonnees :
 - les coordonnees monde ==> [col, row]
 - les coordonnees ecran ==> (x, y)

chacun est utiliser dans un context precis, les coordonnee monde sont celle que tout notre jeu va employer ( toute la logic du jeu )
ensuite seulement arriver a la camera on appliquere les coordonnee ecran ( qui sont calculer a la vole par cette derniere ) pour
ensuite etre utiliser pour l'affichage.

## Choses a mettre en place pour le jeu 
Cree une `class` de base *Entity* qui sera herite par tout le monde et qui acceuillera tout les info que une entite a besoin d'avoir
et notre system de position avec des [col, row] pour tout le monde.
### Pour le element qui se deplace de maniere continu dans le jeu sur les row
- Le poulet et les obstacles fixes ont une position entière [col, row].
- Une voiture ou un train a une position décimale sur sa ligne, par exemple col = 3.4, avec une longueur en cases.
- Les collisions comparent des intervalles, pas des égalités.

## Le saut du poulet
- La logique change `[col, row]` tout de suite quand le saut est accepté.
- La vue garde la case de départ et un timer `t` de 0 à 1 pour afficher le saut.
- Pendant un saut, une seule touche est mémorisée. Elle est jouée à la fin du saut.
- **Règle** : la logique ne lit jamais la position affichée.

## Les entités mobiles
- Chaque frame : `col += vitesse * dt`.
- En sortie d'écran, l'entité revient de l'autre côté.
- Collision : on compare des intervalles `[col, col + longueur)`, pas des égalités.
- On teste la collision à l'atterrissage du poulet et à chaque frame.
- Un poulet sur un tronc ou un train est porté : on ajoute le déplacement de la plateforme à sa position logique.

## L'affichage
- Les entités passent par une seule fonction de projection, la caméra ne fait que décaler le résultat.
- Ordre de dessin : on trie par `col + row`, ce qui est devant dessine en dernier.
