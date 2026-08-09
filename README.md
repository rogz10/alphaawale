# AlphaAwalé

Une implémentation d'AlphaZero pour le jeu de l'Awalé, écrite en Python.
Projet d'apprentissage : réseau de neurones, recherche arborescente et self-play,
sans aucune partie humaine.

## L'idée

L'Awalé a été résolu en 2002 par Romein et Bal. On peut donc recalculer, au moins
sur les finales, le coup optimal dans une position donnée — et savoir précisément
à quel point l'agent s'en approche.

C'est ce qui a motivé le choix du jeu. Plutôt que de juger l'agent sur des
adversaires arbitraires, on le compare à une vérité calculée :

```
« bat le joueur aléatoire »
     ne dit pas grand-chose, le joueur aléatoire est mauvais

« joue le coup optimal dans X % des positions de finale,
  mesuré sur N positions tirées au hasard dans l'oracle »
     se vérifie
```

Pour le reste, c'est un AlphaZero classique : un réseau qui produit une politique
et une valeur, un MCTS guidé par ce réseau, et un entraînement par parties contre
soi-même.

La méthode vient de DeepMind : c'est l'algorithme AlphaZero, décrit par Silver et
al. dans Science en 2018, appliqué ici à l'Awalé. Leur code n'ayant jamais été
publié, tout est réimplémenté à partir de l'article. Projet personnel, sans lien
officiel avec DeepMind.

## Pourquoi l'Awalé

Information parfaite, déterministe, six coups légaux au maximum — contre 362 au go
et 4 672 aux échecs. Les parties sont courtes et une position tient dans douze
entiers. L'ensemble tourne sur un ordinateur portable.

Une difficulté propre au jeu, en revanche : là où le go offre huit symétries pour
multiplier les données d'entraînement, l'Awalé n'en a quasiment aucune. Il faudra
donc davantage de parties de self-play à volume d'apprentissage égal.

## Les règles

Le jeu retenu est l'Oware abapa, dans la variante résolue par Romein et Bal.

Elle ne diffère de l'Awalé de club que sur un point : le grand chelem, c'est-à-dire
un coup qui capturerait toutes les graines restantes de l'adversaire.

| Variante | Grand chelem |
|---|---|
| Abapa de base | coup légal, mais la capture est annulée |
| Compétition internationale | coup légal, aucune capture |
| Résolue (retenue ici) | autorisé, la capture a lieu, la partie s'arrête |

Ce choix ne peut pas être revu en cours de route : l'oracle des finales est calculé
pour cette règle précise, et changer de variante invaliderait rétroactivement les
parties de self-play, l'oracle et le taux d'optimalité.

Le reste suit les règles classiques : douze trous, quarante-huit graines, semis
antihoraire, saut du trou d'origine au-delà de douze graines, capture à deux ou
trois en chaîne dans le camp adverse, obligation de nourrir l'adversaire, vingt-cinq
graines pour gagner.

## Avancement

Étape 1, le moteur de jeu — **terminée**.

- [x] `etat_initial()`, `afficher()`
- [x] `coups_possibles()` : trous jouables du joueur au trait
- [x] `semer()` : semis antihoraire, saut du trou d'origine, position de la dernière graine
- [x] `est_chez_adversaire()`, `graines_adversaire()`
- [x] `capturer()` : capture en chaîne
- [x] `coups_legaux()` : coups possibles, plus l'obligation de nourrir
- [x] `jouer()` : semis, capture, score, alternance du trait
- [x] `est_termine()`, `terminer()` : fin de partie et ramassage final

Critère franchi : **10 000 parties aléatoires, 1 034 220 coups**, invariant des 48 graines
vérifié à chaque coup, aucune exception. Après ramassage final, les greniers totalisent
toujours 48 graines.

Étapes suivantes.

- [ ] Viewer HTML pour rejouer une partie coup par coup ← en cours
- [ ] Joueurs de référence : aléatoire, puis minimax alpha-bêta
- [ ] MCTS pur (UCT, simulations aléatoires)
- [ ] Oracle des finales par analyse rétrograde, jusqu'à dix-huit graines
- [ ] AlphaZero : réseau politique/valeur, MCTS guidé, self-play
- [ ] Évaluation : taux d'optimalité en fonction des itérations d'entraînement

## Validation

Chaque étape a un critère chiffré, à franchir avant de passer à la suivante.

| Étape | Critère |
|---|---|
| Moteur | 10 000 parties aléatoires sans exception, invariant des graines vérifié à chaque coup |
| Minimax | profondeur 6 bat l'aléatoire dans plus de 95 % des parties |
| MCTS pur | 1 000 simulations battent minimax profondeur 4 |
| Oracle | cohérence par symétrie : une position et son miroir donnent des valeurs opposées |
| AlphaZero | le taux d'optimalité contre l'oracle augmente au fil des itérations |

L'invariant des graines est le principal détecteur de bug du projet :

```python
somme(trous) + captures_joueur_0 + captures_joueur_1 == 48
```

Toute graine perdue ou dupliquée le casse immédiatement.

## Structure

```
src/
    jeu.py            moteur : état, coups légaux, semis, capture, fin de partie
    joueurs.py        aléatoire, minimax alpha-bêta, humain
    mcts.py           recherche arborescente Monte-Carlo
    reseau.py         réseau : tête politique (6) et tête valeur (1)
    selfplay.py       génération de parties contre soi-même
    entrainement.py   boucle d'apprentissage
    finales.py        analyse rétrograde, construction de l'oracle
    evaluation.py     matchs, ELO interne, taux d'optimalité
tests/
donnees/              sorties générées, non versionnées
```

Le moteur et l'oracle sont en Python pur, testables sans GPU.

## Lancer

```bash
python3 src/jeu.py
```

Python 3.13 ou plus, numpy, PyTorch (backend MPS sur Apple Silicon), pytest.

## Références

L'algorithme, publié par DeepMind. David Silver dirige les projets AlphaGo et
AlphaZero ; *et al.* signifie « et les autres auteurs ».

- Silver et al., *[Mastering the game of Go without human
  knowledge](https://www.nature.com/articles/nature24270)*, Nature 550, 354–359,
  2017. AlphaGo Zero, premier agent entraîné sans aucune partie humaine.
  Lecture libre : [présentation
  DeepMind](https://deepmind.google/blog/alphago-zero-starting-from-scratch/).
- Silver et al., *[A general reinforcement learning algorithm that masters chess,
  shogi and Go through self-play](https://www.science.org/doi/10.1126/science.aar6404)*,
  Science 362, 1140–1144, 2018. AlphaZero, le même algorithme généralisé à trois
  jeux — c'est celui reproduit ici. L'article complet est accessible avec un compte
  Science gratuit. Sans compte : [présentation
  DeepMind](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)
  ou le [preprint
  PDF](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_preprint.pdf).

Le jeu, par d'autres équipes.

- Romein et Bal, *Awari is Solved*, ICGA Journal 25(3), Vrije Universiteit
  Amsterdam, 2002. La résolution complète du jeu, sur un cluster de 144 processeurs.
  Les bases de données publiées à l'époque sont aujourd'hui hors ligne, d'où
  l'oracle reconstruit à l'étape 4.
  [Notice](https://www.semanticscholar.org/paper/Awari-is-Solved-Romein-Bal/9651f4a7fd03be889d1e8a47407471ca38d68381) ·
  [Synthèse et historique](https://www.chessprogramming.org/Awari)
- [Oware, Wikipedia](https://en.wikipedia.org/wiki/Oware) — les règles, variation
  *abapa*.
