import math
import random
import numpy


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

# vypocitame celkovu sumu fitnessu
# vyratame pravdepodobnost jednotlivych ciest s fitness funkciami
# choice na zaklade tejto pravdepodobnosti vyberie sample. pravdepdobnost je asociovana s kazdym polickom v array
# rodicia populacie maju velkost populacie
def roulette_wheel_selection(populacia):
    fitness_celkovo = []
    pravdepodobnost = []
    rodicia_populacie = []
    for i in populacia:
        fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(i))))
    suma_fitness = sum(fitness_celkovo)
    print(suma_fitness)
    for i in fitness_celkovo:
        pravdepodobnost.append(i / suma_fitness)
    for j in range(0, len(populacia)):
        rodicia_populacie.append(populacia[numpy.random.choice(len(populacia), p=pravdepodobnost)])
    print(rodicia_populacie)
    return rodicia_populacie


def skrizit(rodic1, rodic2):
    print("RODICIA")
    print(rodic1)
    print(rodic2)
    potomok = []
    rodic1_potomok = []
    prvy_bod_krizenia = int(random.random() * len(rodic1))
    print(prvy_bod_krizenia)
    druhy_bod_krizenia = int(random.random() * len(rodic1))
    print(druhy_bod_krizenia)

    start = min(prvy_bod_krizenia, druhy_bod_krizenia)
    end = max(prvy_bod_krizenia, druhy_bod_krizenia)



    for i in range(start, end):
        rodic1_potomok.append((rodic1[i][0],rodic1[i][1]))
    print(rodic1_potomok)





    return potomok


    # dvojbodove krizenie -  Z prvého rodiča vyberieme úsek cesty medzi dvoma náhodne zvolenými bodmi kríženia
    # a dáme ho do potomka na rovnaké miesto. Z druhého rodiča potom vyberieme zvyšné mestá v tom
    # poradí, ako sa nachádzajú v druhom rodičovi a zaplníme tým ostatné miesta vo vektore.


def krizenie(rodicia_populacie):
    deti = []
    pravdepodobnost_krizenia = 0.6
    for i in range(0, len(rodicia_populacie)-1): # posledny sa s niekym krizi?
        if random.random() < pravdepodobnost_krizenia:
            dieta = skrizit(rodicia_populacie[i], rodicia_populacie[i+1])
            deti.append(dieta)


def tournament_selection():
    pass


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
    populacia = vytvor_populaciu(zoznam_miest, 10)
    krizenie(roulette_wheel_selection(populacia))
    ##for i in populacia:
       # print(fitness_cesty((vzdialenost_cesty(i))))

        # velkost populacie, generacie - aspon 20 -  pocet roznych shuffled ciest
        # 20 nahodnych jedincvo
        # jedinec == jedna mozna cesta == chromozom
        # jedno mesto - gen
        # fitnes skore - dlzka celej cesty
        #  Je potrebné implementovať aspoň dve metódy výberu rodičov z populácie.




