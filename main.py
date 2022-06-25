import multiprocessing, random


tablica_liczb = [10, 200, 20, 30, 50, 10, 5, 1, 9, 1, 22]
temp_memory = []
sprawdzenie = 0

def suma_polowy(polowa_tablicy):
    wynik = []
    temp = []
    for x in range(0, len(polowa_tablicy), 2):
        wynik.append(polowa_tablicy[x]+polowa_tablicy[x+1])
    global temp_memory
    temp_memory += wynik + temp

for n in range(1000):
    tablica_liczb.append(random.randint(1, 2000))

if __name__ == '__main__':
    for number in tablica_liczb:
        sprawdzenie += number
    print(sprawdzenie)
    temp_memory = []
    nieparzysty_element = 0
    while len(tablica_liczb) > 1:
        if len(tablica_liczb) % 2 == 1:
            nieparzysty_element += tablica_liczb.pop()
        polowa_dlugosci_listy = len(tablica_liczb) // 2
        if polowa_dlugosci_listy%2 == 0:
            pierwsza_czesc_listy = tablica_liczb[:polowa_dlugosci_listy]
            druga_czesc_listy = tablica_liczb[polowa_dlugosci_listy:]
        else:
            pierwsza_czesc_listy = tablica_liczb[:polowa_dlugosci_listy+1]
            druga_czesc_listy = tablica_liczb[polowa_dlugosci_listy+1:]
        suma1 = suma_polowy(pierwsza_czesc_listy)
        sum1 = suma_polowy(druga_czesc_listy)
        P1 = multiprocessing.Process(target=suma_polowy, args=[pierwsza_czesc_listy])
        P2 = multiprocessing.Process(target=suma_polowy, args=[druga_czesc_listy])
        P1.start()
        P2.start()
        P1.join()
        P2.join()
        tablica_liczb = temp_memory
        temp_memory = []
    print(tablica_liczb[0] + nieparzysty_element)



