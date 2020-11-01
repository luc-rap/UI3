import math
import operator
import random
import numpy
import copy
import time

p_mutacie = 0.1
pravdepodobnost_krizenia = 0.6


# vzdialenost dvoch miest na zaklade euklidovskej vzdialenosti
def vzdialenost(mesto_1, mesto_2):
    d = math.sqrt((mesto_1[0] - mesto_2[0])**2 + (mesto_1[1]-mesto_2[1])**2)
    return d


# vypocita celkovu vzdialenost celej cesty // chromozomu
def vzdialenost_cesty(cesta):
    dlzka_cesty = 0
    for i in range(0, len(cesta)):
        mesto_1 = cesta[i] # z ktoreho mesta ideme
        if i == len(cesta) - 1: # posledne mesto sa vracia do prveho
            mesto_2 = cesta[0]
            dlzka_cesty += vzdialenost(mesto_1, mesto_2)
        else:
            mesto_2 = cesta[i + 1] # nasledujuce mesto
            dlzka_cesty += vzdialenost(mesto_1, mesto_2)
    return dlzka_cesty


def fitness_cesty(dlzka_cesty):
    fitness = 1 / float(dlzka_cesty)
    # fitness = (dlzka_cesty)
    return fitness

# vypocitame celkovu sumu fitnessu
# vyratame pravdepodobnost jednotlivych ciest s fitness funkciami
# choice na zaklade tejto pravdepodobnosti vyberie sample. pravdepdobnost je asociovana s kazdym polickom v array
# rodicia populacie maju velkost populacie

def computeFitness(populacia):
    fitness_celkovo = []
    for i in populacia:
        fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(i))))
    suma_fitness = sum(fitness_celkovo)
    return suma_fitness


def roulette_wheel_selection(populacia):
    fitness_celkovo = []
    pravdepodobnost = []
    rodicia_populacie = []
    probabilities = []
    d = {}
    s = 0
    for i in populacia:
        #print(i)
        d[fitness_cesty(vzdialenost_cesty(i))] = i
        fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(i))))
    suma_fitness = float(sum(fitness_celkovo))
    rel_fitness = [f/suma_fitness for f in fitness_celkovo]
    # Generate probability intervals for each individual
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
    # Draw new population
    new_population = []
    #for n in xrange(num):
    r = random.uniform(0, suma_fitness)
    for (i, individual) in enumerate(populacia):
        if r <= probs[i]:
            return individual



def skrizit(rodic1, rodic2):
    #print("RODICIA")
    #print(rodic1)
    #print(rodic2)
    potomok = []
    rodic1_potomok = []
    rodic2_potomok = []
    prvy_bod_krizenia = int(random.random() * len(rodic1))
    #print(prvy_bod_krizenia)
    druhy_bod_krizenia = int(random.random() * len(rodic1))
    #print(druhy_bod_krizenia)

    start = min(prvy_bod_krizenia, druhy_bod_krizenia)
    end = max(prvy_bod_krizenia, druhy_bod_krizenia)

    for i in range(start, end):
        rodic1_potomok.append((rodic1[i][0],rodic1[i][1]))
    #print(rodic1_potomok)

    for j in rodic2:
        if j not in rodic1_potomok:
            rodic2_potomok.append(j)
    #print(rodic2_potomok)

    potomok = rodic2_potomok[:start] + rodic1_potomok + rodic2_potomok[start:]
    #print("SKRIZENE DIETA:")
    #print(potomok)
    return potomok


    # dvojbodove krizenie -  Z prvého rodiča vyberieme úsek cesty medzi dvoma náhodne zvolenými bodmi kríženia
    # a dáme ho do potomka na rovnaké miesto. Z druhého rodiča potom vyberieme zvyšné mestá v tom
    # poradí, ako sa nachádzajú v druhom rodičovi a zaplníme tým ostatné miesta vo vektore.


def vymen_susedov(dieta, swap):
    dieta[swap], dieta[swap+1] = dieta[swap+1], dieta[swap]
    return dieta


# vymena 2 susednych miest
def mutacia(dieta):
    #print(dieta)
    for i in range(len(dieta)):
        if random.random() < p_mutacie:
            swap_index = int(random.random() * len(dieta)) # index
            dieta = vymen_susedov(dieta, swap_index-1)

    return dieta


def tournament_selection(populacia, fitness_list):
    tournament_size = 5
    turnaj = []
    fit = []
    best_candidate = []
    best_fitness = 0
    for i in range(0, tournament_size):
        random_index = int(random.random() * len(populacia))
        turnaj.append(populacia[random_index])
        fit.append(fitness_list[random_index])
    #fittest = [x for y, x in sorted(zip(fit, turnaj))]
    #print(fittest)
    for i in range(0, tournament_size):
        if fit[i] > best_fitness:
            best_fitness = fit[i]
            best_candidate = turnaj[i]

    return best_candidate

# nahodne premiesana cesta je jedna populacia
def vytvor_populaciu(zoznam_miest, velkost_populacie):
    populacia = []

    for i in range(0, velkost_populacie):
        nova_populacia = random.sample(zoznam_miest, len(zoznam_miest))
        populacia.append(nova_populacia)

    return populacia


def vyber_naj(populacia):
    max_fitness = 0
    best_cesta = []
    index = 0
    index_maxa = 0
    for i in populacia:
        if fitness_cesty((vzdialenost_cesty(i))) > max_fitness:
            max_fitness = fitness_cesty((vzdialenost_cesty(i)))
            best_cesta = i
            index_maxa = index
        index += 1


    return best_cesta, max_fitness, index_maxa

if __name__ == '__main__':
    pocet_miest = 20
    zoznam_miest = []
    generacie = 1000
    fitness_celkovo = []
   # for i in range(0, pocet_miest):
       # x = int(random.random() * 200)
        #y = int(random.random() * 200)
        #zoznam_miest.append((x, y))
    zoznam_miest.append((60, 200))
    zoznam_miest.append((180, 200))
    zoznam_miest.append((100, 180))
    zoznam_miest.append((140, 180))
    zoznam_miest.append((20, 160))
    zoznam_miest.append((80 ,160))
    zoznam_miest.append((200 ,160))
    zoznam_miest.append((140 ,140))
    zoznam_miest.append((40 ,120))
    zoznam_miest.append((120 ,120))
    zoznam_miest.append((180 ,100))
    zoznam_miest.append((60 ,80))
    zoznam_miest.append((100 ,80))
    zoznam_miest.append((180 ,60))
    zoznam_miest.append((20 ,40))
    zoznam_miest.append((100 ,40))
    zoznam_miest.append((200 ,40))
    zoznam_miest.append((20 ,20))
    zoznam_miest.append((60 ,20))
    zoznam_miest.append((160 ,20))

    #zoznam_miest.append((20833.3333	,17100))
    #zoznam_miest.append((20900	,17066.6667))
    #zoznam_miest.append((21300	,13016.6667))
    #zoznam_miest.append((21600,	14150))
    #zoznam_miest.append((21600	,14966.6667))
    #zoznam_miest.append((21600,	16500))
    #zoznam_miest.append((22183.3333,13133.3333))
    #zoznam_miest.append((22583.3333,	14300))
    #zoznam_miest.append((22683.3333	,12716.6667))
    #zoznam_miest.append((23616.6667,	15866.6667))
    #zoznam_miest.append((23700,	15933.3333))
    #zoznam_miest.append((23883.3333,	14533.3333))
    #zoznam_miest.append((24166.6667	,13250))
    #zoznam_miest.append((25149.1667	,12365.8333))
    #zoznam_miest.append((26133.3333	,14500))
    #zoznam_miest.append((26150	,10550))
    #zoznam_miest.append((26283.3333,	12766.6667))
    #zoznam_miest.append((26433.3333	,13433.3333))
    #zoznam_miest.append((26550	,13850))
    #zoznam_miest.append((26733.3333,11683.3333))
    #zoznam_miest.append((27026.1111,13051.9444))
    #zoznam_miest.append((27096.1111	,13415.8333))
    #zoznam_miest.append((27153.6111	,13203.3333))
    #zoznam_miest.append((27166.6667	,9833.3333))
    #zoznam_miest.append((27233.3333	,10450))
    #zoznam_miest.append((27233.3333	,11783.3333))
    #zoznam_miest.append((27266.6667	,10383.3333))
    #zoznam_miest.append((27433.3333,12400))
    #zoznam_miest.append((27462.5,12992.2222))

    populacia = vytvor_populaciu(zoznam_miest, 50)
    eliteSize = int(0.1 * 50)

    start = time.time()
    for generation in range(generacie):
        nova_populacia = []
        fitness_celkovo = []
        fitness_list = []
        #fitness = computeFitness(populacia) # fitnes celej populacie
        for i in populacia:
            fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(i))))
        #fitness_list = list(reversed(sorted(fitness_celkovo)))
        #print(fitness_celkovo)
        print(populacia)
        print(fitness_celkovo)
        zipped_pairs = zip(fitness_celkovo, populacia)
        populacia_sorted = [x for _, x in reversed(sorted(zipped_pairs))]
        #fitness_list = (sorted(fitness_celkovo))
        print("____________________")
        print(populacia_sorted)

        #print(fittest)



        #populacia = [x for y, x in sorted(zip(fitness_list, populacia))]
        #fitness_celkovo, populacia = ((list(t) for t in zip(reversed(*sorted(zip(fitness_celkovo, populacia))))))

        fittest = populacia_sorted[0]
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        fittest = populacia_sorted[1]
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        fittest = populacia_sorted[2]
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        fittest = populacia_sorted[3]
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        fittest = populacia_sorted[4]
        nova_populacia.append(fittest)# vrati najlepsiu cestu

        for gen in range(0, len(populacia)-eliteSize):
            #parent1 = roulette_wheel_selection(populacia)
            #parent2 = roulette_wheel_selection(populacia)
            parent1 = tournament_selection(populacia, fitness_celkovo)
            parent2 = tournament_selection(populacia, fitness_celkovo)
            #if random.random() < pravdepodobnost_krizenia:
            offspring = skrizit(parent1, parent2)
            nova_populacia.append(offspring)
        for gen in range(0, len(populacia)-eliteSize):
            nova_populacia[gen] = mutacia(nova_populacia[gen])
        populacia = nova_populacia



    stop = time.time()
    print("Hladanie trvalo: ", (stop - start), "s")
    fittest, dlzka, index = vyber_naj(populacia)
    print(fittest)
    fitness_celkovo = []
    fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(fittest))))
    suma_fitness = sum(fitness_celkovo)

    #print(suma_fitness)

    print(1/suma_fitness)


        # velkost populacie - aspon 20 -  pocet roznych shuffled ciest
        # 20 nahodnych jedincvo
        # jedinec == jedna mozna cesta == chromozom
        # jedno mesto - gen
        # fitnes skore - dlzka celej cesty
        #  Je potrebné implementovať aspoň dve metódy výberu rodičov z populácie.




