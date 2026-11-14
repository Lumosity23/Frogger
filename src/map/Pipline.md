# Pipeline de génération du monde (pour Ju)

Ce document décrit **ce qu'il faut construire** et **dans quel ordre**. Il ne contient pas tout le code :
il y a quelques exemples pour te lancer, le reste c'est à toi de le réfléchir et de l'écrire.
Les fichiers concernés : [generate_world.py](generate_world.py), [chunk.py](chunk.py), [grid.py](grid.py),
et un peu [scene.py](../scene.py).

---

## 1. L'idée en une phrase

> On **crée tous les objets une seule fois** au lancement du jeu. Ensuite, pendant toute la vie du programme,
> on ne fait que **modifier** des objets existants (changer leur type, leur position, leur vitesse...).
> **Aucun `Chunk(...)`, `Pig(...)` ou `HayBale(...)` ne doit être appelé pendant une partie.**

Pourquoi ? Créer et détruire des objets 60 fois par seconde (ou à chaque nouvelle partie) coûte du temps,
remplit le garbage collector et peut faire saccader le jeu. Réutiliser les mêmes objets est gratuit.
C'est ça qu'on appelle un code *optimisé* ici.

---

## 2. La boucle de jeu complète

Le jeu n'est pas juste « une partie » : c'est une boucle avec des états.

```
       MENU  ──(PLAY)──►  PLAYING  ── (poulet mort)──► GAME_OVER
        ▲                                                   |
        │◄────────(RESTART / retour menu)────────────────┘
        │
        └──(LEADERBOARD)──► LEADERBOARD ──(retour)──► MENU
```

- `MENU` : boutons PLAY et LEADERBOARD.
- `PLAYING` : la partie tourne (update + draw de la scène).
- `GAME_OVER` : écran de fin, on enregistre le score ([score.py](../utils/score.py)).
- `LEADERBOARD` : liste des meilleurs scores.

Les écrans du menu ne sont pas ton sujet. Ce qui est ton sujet : **ce qui se passe quand on passe de `MENU` à `PLAYING`**
(et à chaque restart) : une nouvelle map, issue d'une nouvelle seed, **sans rien recréer**.

---

## 3. Les deux grandes phases

### Phase A : le « GRAND INIT » (une seule fois, au démarrage de l'app)

À faire dans `App.on_init()` / `Scene.__init__()`, et **plus jamais après** :

1. Créer la `Grid` → elle crée tous les `Chunk` (un par ligne). Ils sont tous `SAFE` par défaut.
2. Créer le **pool d'entités** : toutes les entités dont on pourrait avoir besoin, déjà instanciées.
   C'est le rôle de `generate_entity()`.
3. Créer le poulet.

Après ça, la mémoire est « figée » : le nombre d'objets ne change plus.

### Phase B : `new_game(seed)` (à chaque nouvelle partie, boucle de jeu)

Cette phase ne fait **que modifier** les structures de la phase A. Dans l'ordre :

| # | Étape | Ce que ça modifie |
|---|-------|-------------------|
| 0 | **Reset** : vider tous les chunks, remettre toutes les entités dans le pool | `chunk.entities`, état des entités |
| 1 | **Seed** : en tirer une nouvelle et créer le générateur aléatoire | rien (juste le `rng`) |
| 2 | **Config des chunks** : donner un type, une vitesse, une direction à chaque chunk | `chunk.type`, `chunk.velocity`, `chunk.direction` |
| 3 | **Ranger les chunks** dans la grille, avec des zones `SAFE` entre les zones | l'ordre/les types des lignes |
| 4 | **Config des entités** + **ranger les entités** dans leur chunk | `entity.col`, `chunk += entity` |
| 5 | **Placer le poulet** sur la ligne de départ | position du poulet |

Après l'étape 5, on lance la boucle `update` / `draw` et on **ne touche plus** à la génération.

---

## 4. La seed : tout le hasard passe par elle

Règle d'or : **une même seed doit toujours donner exactement la même map.**
Et une **nouvelle seed est tirée à chaque nouvelle partie**.

Il existe déjà `get_seed()` dans [generate_world.py](generate_world.py) (à relire et vérifier !).

Le principe : on crée **un seul** générateur par partie et on le passe en paramètre partout.

```python
rng = np.random.default_rng(seed)       # créé une fois dans new_game
rng.integers(0, 3)                      # ✅ tout le hasard vient de rng
# random.randint(...)                   # ❌ INTERDIT : pas lié à la seed
# np.random.randint(...)                # ❌ INTERDIT : générateur global
```

Conséquences à retenir :
- Toutes tes fonctions de génération prennent `rng` (ou `seed`) en argument.
- **L'ordre des appels à `rng` compte.** Si tu changes l'ordre, tu changes la map. C'est normal,
  mais il ne doit jamais dépendre de ce que fait le joueur, ni du temps (`dt`), ni de l'ordre d'un `set`.
- N'utilise pas `rng` dans `update()` ou `draw()`, sauf si c'est lui aussi déterministe.

---

## 5. Config des chunks (étape 2 et 3)

Un chunk = une ligne de la grille. Il possède déjà : `type`, `velocity`, `direction`
(voir [chunk.py](chunk.py)). Les types sont dans le dico `chunk_type` de [generate_world.py](generate_world.py) :
`SAFE`, `ROAD`, `PIG`, `END`.

### Règles de la map

1. **Départ** : la/les première(s) ligne(s) (là où le poulet apparaît) sont **toujours `SAFE`**.
2. **Arrivée** : la/les dernière(s) ligne(s) sont **toujours `END`/`SAFE`**.
3. Entre deux **zones** de types différents, on met **au moins une ligne `SAFE`** (zone tampon).
4. Une **zone** = plusieurs lignes consécutives du même type (par exemple 3 lignes de `ROAD`).
5. Un chunk `SAFE` **n'accepte aucune entité** (sauf le poulet).
6. Pour un chunk mobile, `direction` vaut `1` ou `-1` et `velocity` est tirée par `rng`.

Schéma d'une map possible (le numéro = la ligne, 30 lignes dans la grille actuelle) :

```
  0  END     ← arrivée
  1  SAFE
  2  PIG
  3  PIG
  4  SAFE    ← tampon obligatoire entre deux zones
  5  ROAD
  6  ROAD
  7  ROAD
  8  SAFE
  ...
 28  SAFE    ← départ (le poulet commence ici)
 29  SAFE
```

### Exemple de départ (à compléter par toi)

Pense en **zones** plutôt que ligne par ligne :

```python
def plan_zones(rng, nb_rows: int) -> list[tuple[str, int]]:
    """Retourne la liste des zones : [("SAFE", 2), ("ROAD", 3), ("SAFE", 1), ("PIG", 2), ...]
    - commence et finit par SAFE
    - jamais deux zones dangereuses collées (il y a toujours un SAFE entre)
    - la somme des tailles == nb_rows
    """
    ...


def apply_zones(chunks: dict[int, Chunk], zones: list[tuple[str, int]], rng) -> None:
    """Parcourt les zones et MODIFIE chaque chunk (type, velocity, direction).
    On ne crée aucun Chunk ici : on modifie ceux de la Grid."""
    ...
```

> ⚠️ Indice : que se passe-t-il si la somme des zones ne tombe pas pile sur `nb_rows` ?
> Pense à la fin de la liste, et à ce qu'on fait avec les lignes qui restent.

---

## 6. Config et rangement des entités (étape 4)

### Le pool

`generate_entity()` crée **tout** le stock d'entités au démarrage : par exemple 10 `Pig` et 12 `HayBale`
(dico `entity_set` dans le fichier). Elles sont rangées dans des listes, **pas encore dans les chunks**.

Pendant `new_game`, on ne fait que **piocher** dans le pool :

```python
entity = pool[Pig].pop()       # on prend une entité libre (pas de Pig(...) !)
entity.col = ...               # on la positionne
chunk += entity                # on la range dans le chunk (Chunk.__iadd__ règle aussi entity.row)
```

Et au reset (étape 0), on fait l'inverse : on retire tout des chunks et on remet dans le pool.

```python
def reset_world(grid, pool) -> None:
    """Vide les chunks et remet toutes les entités dans le pool. Ne crée rien."""
    ...
```

> ⚠️ Si le pool est vide quand tu veux piocher : c'est que ton pool est trop petit pour le pire cas.
> Ne crée **pas** une entité à la volée : agrandis le pool au départ, ou arrête de remplir ce chunk.

### Combien d'entités dans un chunk ? → `logic_size`

Les entités ont une taille logique `lsize` (un `HayBale` fait 4 cases de long).
Un chunk expose déjà `chunk.logic_size` = la somme des longueurs des entités qu'il contient.

Règle simple : on ajoute des entités **tant que** `chunk.logic_size + taille_de_la_suivante <= largeur de la grille`
(en pratique il faut même laisser de la place, sinon la ligne est infranchissable pour le poulet).

À toi de choisir : **quel pourcentage de la ligne peut être rempli ?** Et comment espacer les entités
(positions `col` régulières ? aléatoires sans chevauchement ?). Teste visuellement.

### Quelle entité dans quel type de chunk ?

À définir dans un dico, par exemple :

```python
CHUNK_ENTITIES: dict[str, list[type]] = {
    "SAFE": [],
    "ROAD": [...],
    "PIG":  [...],
    "END":  [],
}
```

Remarque : dans `chunk_type`, chaque type a un tuple `(int, bool)`. À toi de comprendre/décider ce que
signifient ces valeurs (indice : le `bool` ressemble à « est-ce que ce chunk bouge ? », et l'entier à une taille
ou un poids de zone). **Si ce n'est pas clair, demande à Timo avant de coder.**

### Les entités mobiles

Un chunk mobile fait avancer ses entités (voir `Chunk.update`). Pense à ce que ça implique :
si une entité sort de l'écran, elle doit revenir de l'autre côté (cf. [communication.md](../../communication.md),
section *Les entités mobiles*). C'est à ajouter dans la boucle, **sans créer d'objet**.

---

## 7. Placer le poulet (étape 5)

Aujourd'hui, [scene.py](../scene.py) crée le poulet en dur et le range dans `grid.grid[28]`.
Dans ta version : le poulet est créé **une fois** au grand init, et à chaque `new_game` on :
- remet sa position à la ligne de départ (`col`, `row`, `last_pos`),
- le remet vivant (`is_alive = True`),
- le range dans le bon chunk (**attention** : il ne doit pas rester dans l'ancien chunk du reset).

---

## 8. Ce qui existe déjà et ce qui est cassé

Le fichier [generate_world.py](generate_world.py) est un début, il n'est **pas fonctionnel**. Quelques pièges à repérer :

- `entity_set[entity_type].value` : `entity_set[...]` est un `int`, pas une `Enum`. `.value` n'existe pas.
- `generate_world()` utilise `grid_size` qui n'est défini nulle part.
- `integers(0, 1, ...)` ne renvoie que des `0` (la borne haute est exclue !).
- `Scene.prep_world()` appelle `generate_world()` et `generate_entity()` sans leurs arguments.
- `get_chunk_type` et `entity_distribution` sont vides.
- `get_seed()` : pense-t-elle vraiment à retourner une nouvelle seed à chaque appel ? Pourrait-on faire plus simple ?

Ce n'est pas obligé de garder ces noms de fonctions : si tu vois une meilleure organisation, propose-la.

---

## 9. Plan de travail conseillé

Avance dans cet ordre, et **teste après chaque étape** (un simple `print` du résultat suffit au début).

- [ ] **1.** `generate_entity()` : le pool se crée correctement (bon nombre d'entités par type).
- [ ] **2.** `get_seed()` + création du `rng` : la même seed redonne la même suite de nombres.
- [ ] **3.** `plan_zones()` : affiche la liste de zones, vérifie les règles (début/fin SAFE, tampons).
- [ ] **4.** `apply_zones()` : affiche le type de chacun des 30 chunks.
- [ ] **5.** Distribution des entités dans les chunks, avec `logic_size`.
- [ ] **6.** `reset_world()` + `new_game(seed)` : enchaîne plusieurs parties **sans rien recréer**.
- [ ] **7.** Brancher le tout dans `Scene` et dans la boucle menu → play → game over → menu.
- [ ] **8.** *(Bonus)* tests unitaires de la seed.

> Vérification utile à l'étape 6 : après dix `new_game()` d'affilée, le nombre total d'entités
> (pool + chunks) doit être **identique** à celui du début. Si ça augmente ou diminue, il y a une fuite.

---

## 10. Bonus : tests unitaires (seulement à la fin)

L'objectif est très simple : **vérifier qu'une même seed donne toujours la même map.**

Pour comparer deux maps, on les résume en une « signature » (une structure simple qu'on peut comparer avec `==`) :

```python
def world_signature(grid) -> list:
    """Résumé comparable d'un monde : pour chaque chunk, son type, sa direction,
    et la position de ses entités."""
    ...
```

Puis les tests (avec `pytest`, ou de simples `assert` dans un fichier de [src/tests](../tests)) :

```python
def test_same_seed_same_map():
    a = build_world(seed=12345)
    b = build_world(seed=12345)
    assert world_signature(a) == world_signature(b)


def test_different_seed_different_map():
    assert world_signature(build_world(1)) != world_signature(build_world(2))


def test_start_and_end_are_safe():
    ...   # à toi d'écrire : première et dernière ligne
```

Si `test_same_seed_same_map` échoue, cherche un hasard qui ne vient pas de `rng` (voir section 4).

---

## 11. Résumé en 5 règles

1. Tout est **créé une fois** au grand init. Jamais de `Chunk(...)` / `Pig(...)` pendant une partie.
2. Pendant la partie, on **modifie** les structures existantes, on ne les recrée pas.
3. Ordre de construction : **chunks** (types) → **zones SAFE** → **entités** dans les chunks → poulet.
4. Début et fin de la map : toujours `SAFE` (départ et arrivée). Entre deux zones : toujours un `SAFE`.
5. Tout le hasard vient d'**une seed**, nouvelle à chaque partie. Même seed = même map.

Bon courage Ju, si un point est flou, demande avant de coder dans la mauvaise direction ! 🐔
