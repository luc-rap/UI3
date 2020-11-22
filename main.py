import math
import random
import numpy
import time
import matplotlib.pyplot as plt

# pravdepodobnost mutacie
p_mutacie = 0.1


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

# prevratena hodnota dlzky celej cesty
def fitness_cesty(dlzka_cesty):
    fitness = 1 / float(dlzka_cesty)
    return fitness

# vyber rodica pomocou rulety
def roulette_wheel_selection(populacia, fitness_celkovo):
    s = 0
    suma_fitness = float(sum(fitness_celkovo))
    r = numpy.random.uniform(0, suma_fitness)
    for i in range(0, len(populacia)):
        s += fitness_celkovo[i]
        if s > r:
            return populacia[i]


# dvojbodove krizenie
def skrizit(rodic1, rodic2):
    potomok = []
    rodic1_potomok = []
    rodic2_potomok = []
    # nahodne vyberiem dve suradnice - dva body krizenia z prveho rodica
    prvy_bod_krizenia = int(random.random() * len(rodic1))
    druhy_bod_krizenia = int(random.random() * len(rodic1))

    start = min(prvy_bod_krizenia, druhy_bod_krizenia)
    end = max(prvy_bod_krizenia, druhy_bod_krizenia)
    # usek z prveho rodica dame na rovnake miesto v potomkovi
    for i in range(start, end):
        rodic1_potomok.append((rodic1[i][0], rodic1[i][1]))
    # z druheho rodica vyberame zvysne mesta
    for j in rodic2:
        if j not in rodic1_potomok:
            rodic2_potomok.append(j)
    # finalny potomok
    potomok = rodic2_potomok[:start] + rodic1_potomok + rodic2_potomok[start:]
    return potomok


# vymena susedov na mutaciu
def vymen_susedov(dieta, swap):
    dieta[swap], dieta[swap+1] = dieta[swap+1], dieta[swap]
    return dieta


# mutacia s urcitou pravdepodobnostou
def mutacia(dieta):
    if random.random() < p_mutacie:
        swap_index = int(random.random() * len(dieta))
        dieta = vymen_susedov(dieta, swap_index-1)
    return dieta


# vyber turnajom - vyberiem 3 a z nich najlepsieho
def tournament_selection(populacia, fitness_list):
    tournament_size = 3
    turnaj = []
    fit = []
    best_candidate = []
    best_fitness = 0
    for i in range(0, tournament_size):
        random_index = int(random.random() * len(populacia))
        turnaj.append(populacia[random_index])
        fit.append(fitness_list[random_index])
    for i in range(0, tournament_size):
        if fit[i] > best_fitness:
            best_fitness = fit[i]
            best_candidate = turnaj[i]
    return best_candidate


# nahodnym premiesanim vytvori populaciu
def vytvor_populaciu(zoznam_miest, velkost_populacie):
    populacia = []
    for i in range(0, velkost_populacie):
        nova_populacia = random.sample(zoznam_miest, len(zoznam_miest))
        populacia.append(nova_populacia)
    return populacia


# vyberie jedinca s najlepsim fitnes
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

    zoznam_miest = []
    volba = input("Vyber testovania: subor - stlacte s / nahodne suradnice - stlacte ns: ")
    if volba == 's':
        nazov_suboru = input("Zadajte nazov suboru: ")
        try:
            with open(nazov_suboru, 'r') as f:
                for row in f:
                    x, y = row.strip().split()
                    zoznam_miest.append((int(x), int(y)))
        except FileNotFoundError:
            print("Subor nenajdeny.")
            exit()

    elif volba == 'ns':
        pocet_miest = int(input("Zadajte pocet miest (20-40): "))
        for i in range(0, pocet_miest):
            x = int(random.random() * 200)
            y = int(random.random() * 200)
            zoznam_miest.append((x, y))

    else:
        print("Neznamy prikaz.")
        exit()

    generacie = int(input("Zadajte pocet generacii (napr. velkost: 500): "))
    vyber_rodica = input("Zadajte sposob vyberu rodicov: turnaj - stlacte t / ruleta - stlacte r ")
    velkost_populacie = int(input("Zadajte velkost populacie (napr. 100-150) "))

    # vykreslenie grafu
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for first, second in zip(zoznam_miest[:-1], zoznam_miest[1:]):
        ax1.plot([first[0], second[0]] , [first[1], second[1]], 'b')
    ax1.plot([zoznam_miest[0][0], zoznam_miest[-1][0]], [zoznam_miest[0][1], zoznam_miest[-1][1]], 'b')
    for c in zoznam_miest:
        ax1.plot(c[0], c[1], 'ro')

    povodna_dlzka = vzdialenost_cesty(zoznam_miest)
    print("Povodna dlzka: ", povodna_dlzka)
    # vytvori nultu generaciu, pociatocnu populaciu
    populacia = vytvor_populaciu(zoznam_miest, velkost_populacie)
    print(populacia)
    eliteSize = int(0.1 * velkost_populacie)
    # velkost elity je 10% z velkosti populacie

    start = time.time()

    for generacia in range(generacie):
        nova_populacia = []
        fitness_celkovo = []
        fitness_list = []
        for i in populacia:
            fitness_celkovo.append(fitness_cesty((vzdialenost_cesty(i))))

        # usporiada miesta podla fitnes, aby sme mohli vybrat najlepsich do elity
        zipped_pairs = zip(fitness_celkovo, populacia)
        populacia_sorted = [x for _, x in (sorted(zipped_pairs))]

        populacia_sorted = list(reversed(populacia_sorted))
        #priemerna fitnes
        # print(sum(fitness_celkovo) / velkost_populacie)
        for i in range(0, eliteSize):
            fittest = populacia_sorted[i]
            nova_populacia.append(fittest)
        # tvorba novej generacie
        for gen in range(0, len(populacia)-eliteSize):
            if vyber_rodica == 't':
                parent1 = tournament_selection(populacia, fitness_celkovo)
                parent2 = tournament_selection(populacia, fitness_celkovo)
            elif vyber_rodica == 'r':
                parent1 = roulette_wheel_selection(populacia_sorted, list(reversed(sorted(fitness_celkovo))))
                parent2 = roulette_wheel_selection(populacia_sorted, list(reversed(sorted(fitness_celkovo))))
            else:
                print("Neznamy prikaz")
                exit()

            offspring = skrizit(parent1, parent2)
            offspring = mutacia(offspring)
            nova_populacia.append(offspring)
        populacia = nova_populacia

    stop = time.time()

    print("Hladanie trvalo: ", (stop - start), "s")

    fittest, dlzka, index = vyber_naj(populacia)
    fittest.append(fittest[0])
    konecna_dlzka = vzdialenost_cesty(fittest)
    print(fittest)
    # vykreslenie grafu
    for first, second in zip(fittest[:-1], fittest[1:]):
        ax2.plot([first[0], second[0]], [first[1], second[1]], 'b')
    ax2.plot([fittest[0][0], fittest[-1][0]], [fittest[0][1], fittest[-1][1]], 'b')
    for c in fittest:
        ax2.plot(c[0], c[1], 'ro')

    print("Konecna dlzka: ", konecna_dlzka)
    plt.show()






