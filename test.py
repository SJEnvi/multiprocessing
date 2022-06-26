from multiprocessing import shared_memory, Process
import random
import numpy as np

tablica_liczb = []
sprawdzenie = 0

# #Funckja sumująca pojedyncze części tabeli
def find_min(polowa_tablicy):
    mini = polowa_tablicy[0]
    for element in polowa_tablicy:
        if element < mini:
            mini = element
    print(polowa_tablicy)
    print(mini)

def suma_polowy(polowa_tablicy,name):
    existing_shm = shared_memory.SharedMemory(name=name)
    wynik = []
    for x in range(0, len(polowa_tablicy), 2):
        wynik.append(polowa_tablicy[x]+polowa_tablicy[x+1])
    c = np.ndarray((len(polowa_tablicy),), dtype=np.int64, buffer=existing_shm.buf)
    while len(wynik) < len(polowa_tablicy):
        wynik.append(0)
    c[:] = wynik[:]
    existing_shm.close()


if __name__ == '__main__':
    # #Losujemy x elementów do tablicy
    wybor = input("Wybierz czy chciałbyś zsumować listę, czy znaleźć minimum (sum/min): ").lower()
    for n in range(10):
        tablica_liczb.append(random.randint(0, 100))
    if wybor == "min":
        find_min(tablica_liczb)
    elif wybor == "sum":
        # Dla sprawdzenia wyniku policzymy sumę również prostym sposobem
        for number in tablica_liczb:
            sprawdzenie += number
        print(f"Poprawny wynik {sprawdzenie}")
        nieparzysty_element = 0
        #Wyrzucamy nieparzyste elementy z listy i gdy połówki list mają nieparzystą liczbę to przesuwamy index podziału by znów były parzyste
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

            #tworzymy wspolną pamięć i listy które będą się w niej zapisywać, bedą one przechowywać nasze wyniki z funkcji suma_polowy
            a = np.array(pierwsza_czesc_listy)
            d = np.array(druga_czesc_listy)
            shm1 = shared_memory.SharedMemory(create=True, size=a.nbytes)
            shm2 = shared_memory.SharedMemory(create=True, size=a.nbytes)
            buff_1 = np.ndarray(a.shape, dtype=a.dtype, buffer=shm1.buf)
            buff2 = np.ndarray(d.shape, dtype=d.dtype, buffer=shm2.buf)
            #kopiujemy listy do wspolnej pamieci
            buff_1[:] = a[:]
            buff2[:] = d[:]
            print(f"to jest buff1 = {buff_1}")
            print(f"to jest buff2 = {buff2}")

            #Odpalamy 2 prosesy
            P1 = Process(target=suma_polowy, args=(buff_1, shm1.name))
            P2 = Process(target=suma_polowy, args=(buff2, shm2.name))
            P1.start()
            P2.start()
            P1.join()
            P2.join()
            buff1 = np.delete(buff_1, np.where(buff_1 == 0))
            buff2 = np.delete(buff2, np.where(buff2 == 0))
            #konwertuje listy numpy na listy pythona, żeby pętla mogla zacząć się od nowa
            buff1 = buff1.tolist()
            buff2 = buff2.tolist()
            print(f"Zsumowana polowa pierwszej listy = {buff1}")
            print(f"Zsumowana polowa drugiej listy = {buff2}")
            temp = []
            if nieparzysty_element != 0:
                temp = [nieparzysty_element]
            tablica_liczb = buff1 + buff2 + temp
            nieparzysty_element = 0

        del buff_1, buff2
        print(f'Oto wynik liczenia ze wspolbieznoscia: {tablica_liczb}')
        # Zwalniamy pamięć
        shm1.close()
        shm2.close()
        shm1.unlink()
        shm2.unlink()
    else:
        print("Niepoprawny imput...")

