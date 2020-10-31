import math
import random


# vzdialenost dvoch miest na zaklade euklidovskej vzdialenosti
def vzdialenost(mesto_1, mesto_2):
    d = math.sqrt((mesto_1[0] - mesto_2[0])**2 + (mesto_1[1]-mesto_2[1])**2)
    return d


# vypocita celkovu vzdialenost celej cesty // chromozomu
def vzdialenost_cesty(cesta):
    dlzka_cesty = 0
    for i in range(0, len(cesta)):
        mesto_1 = cesta[i] # z ktoreho mesta ideme
        meato_2 = None
        if i == len(cesta) - 1: # posledne mesto sa vracia do prveho
            mesto_2 = cesta[0]
            dlzka_cesty += vzdialenost(mesto_1, mesto_2)
        else:
            mesto_2 = cesta[i + 1] # nasledujuce mesto
            dlzka_cesty += vzdialenost(mesto_1, mesto_2)
    return dlzka_cesty


def fitness_cesty(dlzka_cesty):
    fitness = 1 / float(dlzka_cesty)
    return fitness


# nahodne premiesana cesta je jedna populacia
def vytvor_populaciu(zoznam_miest, velkost_populacie):
    populacia = []
    #print(zoznam_miest)
    #random.shuffle(zoznam_miest)

    for i in range(0, velkost_populacie):
        nova_populacia = random.sample(zoznam_miest, len(zoznam_miest))
        populacia.append(nova_populacia)

    return populacia

# pocet generacii == pocet iteracii, kolkkokrat to bude bezat
def geneticky_algoritmus(populacia, velkost_populacie, pocet_generacii):
    pass


if __name__ == '__main__':
    pocet_miest = 5
    zoznam_miest = []

    for i in range(0, pocet_miest):
        x = int(random.random() * 200)
        y = int(random.random() * 200)
        zoznam_miest.append((x, y))

    print(zoznam_miest)
    pokus = vytvor_populaciu(zoznam_miest, 10)
    print(pokus)
    for i in pokus:
        print(vzdialenost_cesty(i))

        # velkost populacie, generacie - aspon 20 -  pocet roznych shuffled ciest
        # 20 nahodnych jedincvo
        # jedinec == jedna mozna cesta == chromozom
        # jedno mesto - gen
        # fitnes skore - dlzka celej cesty




