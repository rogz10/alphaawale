# AlphaAwalé

**AlphaZero appliqué à l'Awalé**, écrit intégralement à la main en Python — réseau, MCTS et self-play, sans aucune partie humaine.

> Ce n'est pas un projet « faire une IA qui joue ».
> C'est un projet de **mesure** : produire un chiffre défendable.

```
❌  « mon agent bat le joueur aléatoire »

✅  « mon agent joue le coup optimal dans 94,3 % des positions de finale,
     mesuré sur 10 000 positions tirées au hasard dans l'oracle »
```

L'Awalé est **fortement résolu** (Romein & Bal, 2002). On peut donc calculer une
vérité terrain et évaluer l'agent contre elle, au lieu de le comparer à des
adversaires arbitraires.

---

## Les règles — variante figée ⚠️

Le jeu retenu est l'**Oware abapa**, dans la **variante résolue** de Romein & Bal.

Elle ne diffère de l'Awalé de club que sur un point, mais ce point change tout :

| Variante | Grand chelem (capturer toutes les graines adverses) |
|---|---|
| Abapa de base | coup légal, mais la capture est annulée |
| Compétition internationale | coup légal, aucune capture |
| **Résolue — celle d'ici** | **autorisé, la capture a lieu, la partie s'arrête** |

Ce choix est **définitif**. L'oracle des finales sera calculé pour cette règle ;
changer de variante en cours de route invaliderait rétroactivement toutes les
mesures — parties de self-play, oracle, taux d'optimalité.

Le reste suit les règles classiques : 12 trous, 48 graines, semis antihoraire,
saut du trou d'origine au-delà de 12 graines, capture à 2 ou 3 en chaîne dans le
camp adverse, obligation de nourrir l'adversaire, 25 graines pour gagner.

---

## Avancement

**Étape 1 — moteur de jeu** *(en cours)*

- [x] `etat_initial()` — la position de départ
- [x] `afficher()` — le plateau en terminal
- [x] `coups_possibles()` — trous jouables du joueur au trait
- [x] `semer()` — semis antihoraire, saut du trou d'origine, position de la dernière graine
- [x] `est_chez_adversaire()`
- [ ] `capturer()` — capture en chaîne
- [ ] `coups_legaux()` — coups possibles + obligation de nourrir
- [ ] `jouer()` · `est_termine()`

**Étapes suivantes**

- [ ] Viewer HTML — rejouer une partie coup par coup
- [ ] Joueurs de référence — aléatoire, puis minimax alpha-bêta
- [ ] MCTS pur (UCT, simulations aléatoires)
- [ ] Oracle des finales par analyse rétrograde (≤ 18 graines)
- [ ] AlphaZero — réseau politique/valeur, MCTS guidé, self-play
- [ ] Évaluation : taux d'optimalité vs itérations d'entraînement

---

## Critères de validation

Chaque étape a un critère chiffré. Pas de passage à la suivante sans l'avoir franchi.

| Étape | Critère |
|---|---|
| Moteur | 10 000 parties aléatoires sans exception, invariant des 48 graines vérifié à chaque coup |
| Minimax | profondeur 6 bat l'aléatoire dans > 95 % des parties |
| MCTS pur | 1 000 simulations battent minimax profondeur 4 |
| Oracle | cohérence par symétrie : une position et son miroir donnent des valeurs opposées |
| AlphaZero | le taux d'optimalité contre l'oracle augmente au fil des itérations |

L'**invariant des 48 graines** est le détecteur de bug central du projet :

```python
somme(trous) + captures_joueur_0 + captures_joueur_1 == 48
```

Toute graine perdue ou dupliquée le casse immédiatement.

---

## Structure

```
src/
├── jeu.py            moteur : état, coups légaux, semis, capture, fin de partie
├── joueurs.py        aléatoire, minimax alpha-bêta, humain
├── mcts.py           recherche arborescente Monte-Carlo
├── reseau.py         réseau : tête politique (6) + tête valeur (1)
├── selfplay.py       génération de parties contre soi-même
├── entrainement.py   boucle d'apprentissage
├── finales.py        analyse rétrograde → oracle
└── evaluation.py     matchs, ELO interne, taux d'optimalité
tests/
donnees/              sorties générées (non versionnées)
```

Le moteur et l'oracle sont du **Python pur** — testables sans GPU.

---

## Lancer

```bash
python3 src/jeu.py
```

**Stack** : Python 3.13+ · numpy · PyTorch (backend MPS, GPU Apple Silicon) · pytest

---

## Références

- Silver et al., *Mastering the game of Go without human knowledge*, Nature 2017
- Silver et al., *A general reinforcement learning algorithm that masters chess, shogi and Go through self-play*, Science 2018
- Romein & Bal, *Awari is Solved*, Vrije Universiteit Amsterdam, 2002 — bases de données aujourd'hui hors ligne, d'où l'oracle maison
- [Oware — Wikipedia](https://en.wikipedia.org/wiki/Oware), variation *abapa*
# alphaawale
