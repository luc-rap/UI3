import matplotlib.pyplot as plt
import math
import numpy
import random


def vzdialenost(mesto_1, mesto_2):
    d = math.sqrt((mesto_1[0] - mesto_2[0])**2 + (mesto_1[1]-mesto_2[1])**2)
    return d


# vypocita celkovu vzdialenost celej cesty
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


def simulovane_zihanie(zoznam_miest):

    cena = vzdialenost_cesty(zoznam_miest)
    teplota = 20 # da sa menit podla potreby, ale je prisposobena na 20 az 40 miest podla zadania
    factor = 0.9999 # alfa faktor - cooling factor

    for i in range(8000): # da sa menit podla potreby, ale pocet iteracii je +/- prisposobeny 20 az 40 miest podla zadania
        #print(i, cena)
        # pocet etap
        for j in range(10):
            # vymen dve nahodne suradnice
            s1, s2 = numpy.random.randint(0, len(zoznam_miest), size=2)
            zoznam_miest[s1], zoznam_miest[s2] = zoznam_miest[s2], zoznam_miest[s1]
            cena_nova = vzdialenost_cesty(zoznam_miest)

            if cena_nova < cena:
                cena = cena_nova
            else: # ak nova cena nie je lepsia, tak s nejakou pravdepodobnostou si ju aj tak mozem vybrat
                x = numpy.random.uniform()
                if x < numpy.exp((cena-cena_nova) / teplota): # pravdepdobnost, ze prijme riesenie
                    cena = cena_nova
                else: # ked neprijme riesenie, vratime naspat, skusame znovu
                    zoznam_miest[s1], zoznam_miest[s2] = zoznam_miest[s2], zoznam_miest[s1]

        teplota *= factor

    return zoznam_miest


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
        # je mozne zadat aj ine velkosti, ako bolo v zadani, ale nie je na to prisposobena teplota
        for i in range(0, pocet_miest):
            x = int(random.random() * 200)
            y = int(random.random() * 200)
            zoznam_miest.append((x, y))

    else:
        print("Neznamy prikaz.")
        exit()
    povodna_dlzka = vzdialenost_cesty(zoznam_miest)
    print("Povodna dlzka: ", povodna_dlzka)
    # vykreslenie grafu
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for first, second in zip(zoznam_miest[:-1], zoznam_miest[1:]):
        ax1.plot([first[0], second[0]] , [first[1], second[1]], 'b')
    ax1.plot([zoznam_miest[0][0], zoznam_miest[-1][0]], [zoznam_miest[0][1], zoznam_miest[-1][1]], 'b')
    for c in zoznam_miest:
        ax1.plot(c[0], c[1], 'ro')

    zoznam_miest = simulovane_zihanie(zoznam_miest)

    # vykreslenie grafu
    for first, second in zip(zoznam_miest[:-1], zoznam_miest[1:]):
        ax2.plot([first[0], second[0]] , [first[1], second[1]], 'b')
    ax2.plot([zoznam_miest[0][0], zoznam_miest[-1][0]], [zoznam_miest[0][1], zoznam_miest[-1][1]], 'b')
    for c in zoznam_miest:
        ax2.plot(c[0], c[1], 'ro')

    konecna_dlzka = vzdialenost_cesty(zoznam_miest)
    zoznam_miest.append(zoznam_miest[0])
    print(zoznam_miest)
    print("Konecna dlzka: ", konecna_dlzka)
    plt.show()