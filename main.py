import math
import operator
import random
import numpy
import copy

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
                #break
    #return new_population

    #for i in fitness_celkovo:
        #pravdepodobnost.append(i / suma_fitness)
    #rodicia_populacie.append(populacia[numpy.random.choice(len(populacia), p=pravdepodobnost)])

    #return populacia[numpy.random.choice(len(populacia), p=pravdepodobnost)]

    #dict = list(reversed(sorted(d.items())))
    #print("suma fitnes", suma_fitness)
    #fitness_celkovo = list(reversed(sorted(fitness_celkovo)))
    #r = random.uniform(0, suma_fitness)
    #print("r: ", r)
    #for i in range(len(populacia)):
        #print(fitness_cesty((vzdialenost_cesty(i))))
        #print((dict[i][0]))
        #s += fitness_celkovo[i]
        #print(s)
        #if s > r:
            #return populacia[i]

    #print(suma_fitness)
    #for i in fitness_celkovo:
    #    pravdepodobnost.append(i / suma_fitness)
    #rel_fitness = [f / suma_fitness for f in fitness_celkovo]
    #probabilities = [sum(rel_fitness[:i+1])
    #                 for i in range(len(rel_fitness))]
    #chosen = []
    #for n in range(2):
    #    r = random.random()
     #   for (i, individual) in enumerate(populacia):
        #    if r <= probabilities[i]:
      #          chosen.append(list(individual))
          #      break
   # return chosen


    #for j in range(0, len(populacia)):
        #rodicia_populacie.append(populacia[numpy.random.choice(len(populacia), p=pravdepodobnost)])
    #print(rodicia_populacie)
    #return populacia[numpy.random.choice(len(populacia), p=pravdepodobnost)]


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


def krizenie(rodicia_populacie):
    deti = []

    for i in range(0, len(rodicia_populacie)-1): # posledny sa s niekym krizi?
        if random.random() < pravdepodobnost_krizenia:
            dieta = skrizit(rodicia_populacie[i], rodicia_populacie[i+1])
            deti.append(dieta)
    #print("DETI:")
    #print(deti)
    return deti


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


#def tournament_selection(populacia):
  #  print(populacia[numpy.random.choice(len(populacia), size=10)])
  #  tournament_contestants = populacia[numpy.random.choice(len(populacia), size=10)]
  #  tournament_contestants_fitness = computeFitness(tournament_contestants)
  #  return tournament_contestants[numpy.argmin(tournament_contestants_fitness)]


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
#def TSP(generacie=100, popsize=20, zoznam_miest):
    #deti = krizenie(roulette_wheel_selection(populacia))
   # populacia = vytvor_populaciu(zoznam_miest, 20)
   # nova_populacia = []
   # for gen in range(0, len(populacia)):
    #    parent1 = roulette_wheel_selection(populacia)
    #    parent2 = roulette_wheel_selection(populacia)
    #    offspring = skrizit(parent1, parent2)
    #    nova_populacia.append(offspring)
   # for gen in range(0, len(populacia)):
    #    nova_populacia[gen] = mutacia(nova_populacia[gen])
   # populacia = nova_populacia
    #print(deti)
    #mutacia_deti = []
    #for i in range(0, len(deti)):
        #mutacia_deti.append(mutacia(deti[i]))
    #print("MUTACIA")
    #print(mutacia_deti)
    #return mutacia_deti

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

    populacia = vytvor_populaciu(zoznam_miest, 50)
    eliteSize = 5


    for generation in range(generacie):
        #fitness = 0
        #print('\nGeneration: {0}'.format(generation + 1))
        #print('Population: {0}'.format(populacia))
        nova_populacia = []
        fitness = computeFitness(populacia) # fitnes celej populacie
        # najdem najlepsieho a ulozim ho do elity
        #print('Fitness:    {0}'.format(fitness))
        print(fitness)
        fittest, dlzka, index = vyber_naj(populacia)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu = copy.deepcopy(populacia)
        #print(index)
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu
        popuu.pop(index)
        fittest, dlzka, index = vyber_naj(popuu)
        nova_populacia.append(fittest)# vrati najlepsiu cestu

        #print("Fittest ", dlzka)
        ##print(fittest)
        #nova_populacia.append(fittest) # ponecha si najlepsieho
        #print(nova_populacia)
        for gen in range(0, len(populacia)-7):
            parent1 = roulette_wheel_selection(populacia)
            parent2 = roulette_wheel_selection(populacia)
            #print(parent1)
            #print(parent2)
            #parent1 = tournament_selection(populacia)
            #parent2 = tournament_selection(populacia)
            #if random.random() < pravdepodobnost_krizenia:
            offspring = skrizit(parent1, parent2)
            nova_populacia.append(offspring)
        for gen in range(0, len(populacia)-7):
            nova_populacia[gen] = mutacia(nova_populacia[gen])
        populacia = nova_populacia

    fittest, dlzka, index = vyber_naj(populacia)
    #print(populacia[0])
    fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(fittest))))
    suma_fitness = sum(fitness_celkovo)

    print(suma_fitness)

    #print(1/suma_fitness)


        # velkost populacie - aspon 20 -  pocet roznych shuffled ciest
        # 20 nahodnych jedincvo
        # jedinec == jedna mozna cesta == chromozom
        # jedno mesto - gen
        # fitnes skore - dlzka celej cesty
        #  Je potrebné implementovať aspoň dve metódy výberu rodičov z populácie.




