def etat_initial():
    return {
        "trous":[4]*12,
        "scores":[0,0],
        "trait":0
    }


def afficher(etat):# fonction qui affiche l'etat du jeu
    
    rangee_du_bas=etat["trous"][:6]
    rangee_du_haut=etat["trous"][6:][::-1]
    ligne_bas= ""
    ligne_haut= ""
    for tb in rangee_du_bas:
        ligne_bas=ligne_bas + f"{tb:4}"
    for th in rangee_du_haut:
        ligne_haut= ligne_haut + f"{th:4}"
    print(f"ligne de haut : {ligne_haut}")
    print(f"ligne du bas  : {ligne_bas}")
    print(f"Score - J0: {etat['scores'][0]}, Score - J1:{etat['scores'][1]}")

def coups_possibles(etat):# fonction qui renvoie la liste des trous possibles a semer, en fonction du trait
    if etat["trait"]==0:
        ma_range=etat["trous"][:6]
        decalage=0
    else:
        ma_range=etat["trous"][6:]
        decalage=6
    resultat=[]
    for i, trou in enumerate(ma_range):
        if trou >0:
            resultat.append(i+decalage)

    return resultat
def semer(trous, depart): # fonction qui seme les graines dans les trous, en fonction de la position de depart
    #liste_dernier=[]
    new_holes=trous.copy()
    seeds=new_holes[depart] # nombre de graines contenues dans le trous de depart
    new_holes[depart]=0 # remise a 0 du trou de depart
    position=depart
    for seed in range(seeds):
        position=(position +1) %12 # %12 permet de revenir au debut de la liste si on depasse la derniere case 
        if position== depart:
            #position+=1
            position=(position+1)%12
        new_holes[position]+=1
        #liste_dernier.append(new_holes[position])
        #for last in liste_dernier:
        #last_position=liste_dernier[-1]
    return new_holes, position
    #print(f"copie des trous:{new_holes}")
#copi=semer({"trous": [1,2,3,4,5,6,7,8,9,10,11,12], "scores": [0,0], "trait": 0})
def est_chez_adversaire(position,trait): # fonction qui verifie si la position de la derniere graine semee est chez l'adversaire
    return position // 6!=trait

def capturer(trous,derniere,trait): # fonction qui capture les graines de l'adversaire, en fonction de la position de la derniere graine semee
    new=trous.copy()
    total=0
    position=derniere
    while est_chez_adversaire(position,trait) and (new[position]==2 or new[position]==3):
        total+=new[position]
        new[position]=0
        position=(position-1)%12 # %12 permet de revenir au debut de la liste si on depasse la derniere case (il se declenche que si franchit la couture entre le trou 0 et le trou 11)
    return new,total


if __name__=="__main__":
    etat=etat_initial()
    print(etat)
    print(sum(etat["trous"]))
    afficher(etat)
    etat_test = {"trous": [1,2,3,4,5,6,7,8,9,10,11,12], "scores": [0,0], "trait": 0}
    afficher(etat_test)
    test_trait_0 = {"trous": [0,3,0,5,1,0, 2,2,2,2,2,2], "scores": [0,0], "trait": 0}
    test_trait_1 = {"trous": [0,3,0,5,1,0, 2,2,2,2,2,2], "scores": [0,0], "trait": 1}
    print(coups_possibles(test_trait_0))    
    print(coups_possibles(test_trait_1))
    print("*"*50)
    print("semer:\n")
    plateau = [4,4,4,4,4,4, 4,4,4,4,4,4]
    print(semer(plateau, 2))
    anneau = [0,0,0,0,0,0, 0,0,0,0,0,3]
    print(semer(anneau,11))
    print("test invariant")
    pile = [12,1,1,1,1,1, 1,1,1,1,1,1]
    gros = [13,1,1,1,1,1, 1,1,1,1,1,1]
    print(semer(pile, 0))
    print(semer(gros, 0))
    print(sum(pile))
    print(sum(gros))
    print(semer([4,4,4,4,4,4, 4,4,4,4,4,4], 2)) 
    print(semer([0,0,0,0,0,0, 0,0,0,0,0,3], 11))   
    print(semer([12,1,1,1,1,1, 1,1,1,1,1,1], 0))   
    print(semer([13,1,1,1,1,1, 1,1,1,1,1,1], 0))    
    print(semer([1,1,1,1,1,1, 1,1,1,1,1,12], 11))   
    print("="*50)
    trous,derniere =semer([4,4,4,4,4,4, 4,4,4,4,4,4], 2)
    #print(sum(trous))
    print(derniere)
    trous, derniere = semer([0,0,0,0,0,0, 0,0,0,0,0,3], 11)
    print(derniere)
    trous, derniere = semer([13,1,1,1,1,1, 1,1,1,1,1,1], 0)
    print(derniere)
    print(est_chez_adversaire(7, 0))
    print(est_chez_adversaire(3, 0))
    print(est_chez_adversaire(7, 1))
    print(est_chez_adversaire(3, 1))
    print("capturer")
    t, n = capturer([0,0,0,0,0,0, 2,3,4,0,0,0], 8, 0)
    print(t, n)
    t, n = capturer([0,0,0,0,0,0, 2,3,2,0,0,4], 8, 0)
    print(t, n) 
    t, n = capturer([0,0,0,0,0,0, 0,0,4,0,0,0], 8, 0)
    print(t, n)
    t, n = capturer([0,0,2,0,0,0, 0,0,0,0,0,0], 2, 0)
    print(t, n)
    t, n = capturer([0,0,0,0,0,0, 2,5,2,0,0,0], 8, 0)
    print(t, n)
    t, n = capturer([0,0,0,3,0,0, 0,0,0,0,0,0], 3, 0)
    print(t,n)    # [0,0,0,3,0,0, 0,0,0,0,0,0]  et  0

