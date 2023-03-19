
class Manager:
    def __init__(self):
        self.actions = {}
        self.dostepne_operacje = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.int_tpl = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        self.fl_tpl = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.')
        self.historia = {}
        self.magazyn = {}
        self.konto = 0

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

    def execute(self, name, *args, **kwargs):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self, *args, **kwargs)


manager = Manager()


@manager.assign("pobierz_saldo")
def pobierz_saldo(manager):
    with open('saldo.txt') as sal:
        manager.konto = float(sal.readline().strip())


@manager.assign("nadpisz_saldo")
def nadpisz_saldo(manager, val):
    with open('saldo.txt', 'w') as sal:
        sal.write(f'{val}\n')


@manager.assign("wczytaj_historie")
def wczytaj_historie(manager):
    with open('log.txt') as log:
        pos = 0
        manager.historia.clear()
        for m in log:
            if pos == 0:
                key = int(m.strip())
                pos += 1
            elif pos == 1:
                opis1 = m.strip()
                pos += 1
            elif pos == 2:
                opis2 = m.strip()
                pos += 1
            elif pos == 3:
                opis3 = m.strip()
                pos += 1
            elif pos == 4:
                opis4 = m.strip()
                pos = 0
                manager.historia[key] = [opis1, opis2, opis3, opis4]


@manager.assign("zapisz_historie")
def zapisz_historie(manager, id, oper, par1, par2, par3):
    with open('log.txt', 'a') as log:
        log.write(f'{id}\n{oper}\n{par1}\n{par2}\n{par3}\n')


@manager.assign("wczytaj_magazyn")
def wczytaj_magazyn(manager):
    with open('mag.txt') as mag:
        poz = 0
        manager.magazyn.clear()
        for p in mag:
            if poz == 0:
                kex = p.strip()
                poz += 1
            elif poz == 1:
                ops1 = p.strip()
                poz += 1
            elif poz == 2:
                ops2 = float(p.strip())
                poz += 1
            elif poz == 3:
                ops3 = int(p.strip())
                poz = 0
                manager.magazyn[kex] = [ops1, ops2, ops3]


@manager.assign("nadpisz_magazyn")
def nadpisz_magazyn(manager, magazyn_new):
    f = open('mag.txt', 'w')
    f.close()
    for n in magazyn_new:
        id_prd = n
        prd = magazyn_new[n][0]
        cena_prd = magazyn_new[n][1]
        ilosc_prd = magazyn_new[n][2]
        with open('mag.txt', 'a') as mag:
            mag.write(f'{id_prd}\n{prd}\n{cena_prd}\n{ilosc_prd}\n')


while True:
    while True:
        print(f"Dostepne operacje: {manager.dostepne_operacje}")
        operacja = input("Podaj operacje: ")
        if operacja in manager.dostepne_operacje:
            break
        else:
            print("Operacja z poza listy dostępnych operacji")
# wykonujemy zadane operacje
    manager.execute("pobierz_saldo")
    if operacja == "saldo":
        saldo_add = input("Podaj kwote do dodania(odjęcia) do konta <int>/<float>: ")
        if saldo_add != '':
            if manager.konto + float(saldo_add) < 0:
                print("Operacja niemozliwa do wykonania")
            else:
                manager.konto += float(saldo_add)
                manager.execute("nadpisz_saldo", manager.konto)
                manager.execute("wczytaj_historie")
                manager.execute("zapisz_historie", len(manager.historia) + 1, 'saldo', manager.konto, '-', '-')
        else:
            print("Podano pustą wartosc - operacja niemozliwa do wykonania")
    elif operacja == "konto":
        manager.execute("pobierz_saldo")
        print(f"Stan konta wynosi: {manager.konto}")
    elif operacja == "lista":
        print("Stan magazynu: ")
        komunikat = "Magazyn jest pusty"
        manager.execute("wczytaj_magazyn")
        for i in manager.magazyn:
            print(f"Nazwa: {manager.magazyn[i][0]}, cena: {manager.magazyn[i][1]}, ilosc: {manager.magazyn[i][2]}")
            komunikat = ''
        if komunikat != '':
            print(komunikat)
    elif operacja == "magazyn":
        produkt = input("Podaj nazwe produktu: ")
        kontrolna = 0
        if produkt == '':
            print("Podano pusta nazwa - operacja niemozliwa do wykonania")
        else:
            manager.execute("wczytaj_magazyn")
            print("Stan magazynu dla podanego produktu: ")
            info = 'Magazyn jest pusty'
            kontrolna = 1
            for element in manager.magazyn:
                if produkt == manager.magazyn[element][0]:
                    print(f"Nazwa: {manager.magazyn[element][0]}, cena: {manager.magazyn[element][1]},"
                          f" ilosc: {manager.magazyn[element][2]}")
                    kontrolna = 0
                elif produkt != manager.magazyn[element][0]:
                    info = "Brak w magazynie"
            if kontrolna == 1:
                print(info)
    elif operacja == "przeglad":
        manager.execute("wczytaj_historie")
        if len(manager.historia) < 1:
            print("Brak wpisow")
        else:
            od = input("Podaj numer wpisu od ktorego chcesz rozpoczac<int>: ")
            do = input("Podaj numer wpisu do ktorego chcesz kontynuowac<int>: ")
            if od == '' and do == '':
                print("Podano puste wartosci - wyswietlam cala historia")
                for i in manager.historia:
                    print(i, ": ", manager.historia[i])
            elif od == '' and do != '':
                # sprawdzamy wprowadzona wartosc czy jest int+
                noint = 0
                for y in do:
                    if y not in manager.int_tpl:
                        noint = 1
                if noint == 1 or do == '0':
                    print("Podana wartosc jest niepoprawna")
                    print(f"Dopuszczalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}")
                else:
                    print("Wyswietlam historie od poczatku do podanej wartosci")
                    for i in manager.historia:
                        if i <= int(do):
                            print(i, ": ", manager.historia[i])
            elif od != '' and do == '':
                noint = 0
                for y in od:
                    if y not in manager.int_tpl:
                        noint = 1
                if noint == 1 or od == '0':
                    print("Podana wartosc jest niepoprawna")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}")
                else:
                    print("Wyswietlam historie od podanej wartosci do konca")
                    for i in manager.historia:
                        if i >= int(od):
                            print(i, ": ", manager.historia[i])
            elif od != '' and do != '':
                noint = 0
                for y in od:
                    if y not in manager.int_tpl:
                        noint = 1
                for z in do:
                    if z not in manager.int_tpl:
                        noint = 1
                if noint == 1:
                    print("Przynajmniej  jedna podana wartosc jest niepoprawna")
                elif int(od) == 0 or int(do) == 0:
                    print("Podano niedopuszczalna zerowa wartosc")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}")
                elif int(od) > int(do):
                    print("Wartosc poczatkowa wieksza od koncowej")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}")
                else:
                    print("Wyswietlam historie dla podanego zakresu wartosci")
                    for i in manager.historia:
                        if int(od) <= i <= int(do):
                            print(i, ": ", manager.historia[i])
    elif operacja == "zakup":
        nazwa = input("Podaj nazwe produktu: ")
        cena = input("Podaj cene produktu<int><float>: ")
        ilosc = input("Podaj ilosc produktow<int>: ")
        if nazwa == '' or cena == '' or ilosc == '':
            print("Operacja niemozliwa - podano pusta wartosc")
        else:
            # sprawdzamy poprawnosc ceny i ilosci
            noint = 0
            for y in cena:
                if y not in manager.fl_tpl:
                    noint = 1
            for z in ilosc:
                if z not in manager.int_tpl:
                    noint = 1
            if noint == 1 or cena == '0' or ilosc == '0':
                print("Przynajmniej  jedna podana wartosc jest niepoprawna")
            else:
                manager.execute("pobierz_saldo")
                ilosc = int(ilosc)
                # jako identyfikatora uzyjemy sumy nazwy i ceny - bo mozemy miec te same produkty o roznych cenach
                magazyn_add = nazwa + cena, nazwa, float(cena), ilosc
                # Najpierw sprawdzamy czy mamy wystarczajace srodki na koncie
                if manager.konto < (float(magazyn_add[2]) * int(magazyn_add[3])):
                    print("Operacja niemozliwa - brak wystarczajacych srodkow na koncie")
                else:
                    manager.execute("wczytaj_magazyn")
                    if magazyn_add[0] not in manager.magazyn:
                        # jesli takiego produktu niema w magazynie dopisujemy do magazynu
                        manager.magazyn[magazyn_add[0]] = [magazyn_add[1], magazyn_add[2], magazyn_add[3]]
                        manager.konto -= magazyn_add[2] * magazyn_add[3]
                        manager.execute("nadpisz_saldo", manager.konto)
                        manager.execute("nadpisz_magazyn", manager.magazyn)
                        print("Dodano produkt do magazynu")
                        manager.execute("wczytaj_historie")
                        manager.execute("zapisz_historie", len(manager.historia)+1, 'zakup', nazwa, float(cena), ilosc)
                    else:
                        # jesli taki produkt istnieje dodajemy tylko ilosc sztuk
                        x = manager.magazyn[magazyn_add[0]][1]
                        y = manager.magazyn[magazyn_add[0]][2] + ilosc
                        manager.magazyn[magazyn_add[0]] = [nazwa, x, y]
                        manager.konto -= magazyn_add[2] * magazyn_add[3]
                        manager.execute("nadpisz_saldo", manager.konto)
                        manager.execute("nadpisz_magazyn", manager.magazyn)
                        print("Zmodyfikowano liczbe produktow w magazynie")
                        manager.execute("wczytaj_historie")
                        manager.execute("zapisz_historie", len(manager.historia)+1, 'zakup', nazwa, float(cena), ilosc)
    elif operacja == "sprzedaz":
        nazwa = input("Podaj nazwe produktu: ")
        cena = input("Podaj cene produktu<int><float>: ")
        ilosc = input("Podaj ilosc produktow<int>: ")
        # weryfikujemy poprawnosc zlecenia
        if nazwa == '' or cena == '' or ilosc == '':
            print("Operacja niemozliwa - podano pusta wartosc")
        else:
            noint = 0
            for y in cena:
                if y not in manager.fl_tpl:
                    noint = 1
            for z in ilosc:
                if z not in manager.int_tpl:
                    noint = 1
            if noint == 1 or cena == '0' or ilosc == '0':
                print("Przynajmniej  jedna podana wartosc jest niepoprawna")
            else:
                ilosc = int(ilosc)
                magazyn_mv = nazwa + cena, nazwa, float(cena), ilosc
                # sprawdzamy czy mamy taki produkt
                manager.execute("wczytaj_magazyn")
                if magazyn_mv[0] not in manager.magazyn:
                    print("Produktu o takiej nazwie i cenie niema w magazynie")
                else:
                    # sprawdzamy czy mamy wystarczajaca ilosc sztuk
                    if ilosc > manager.magazyn[magazyn_mv[0]][2]:
                        print(f"Dostepna ilosc produktu jest mniejsza i wynosi: {manager.magazyn[magazyn_mv[0]][2]}")
                    else:
                        # jesli zlecenie zabiera wszystkie sztuki produktu usuwamy produkt z magazynu
                        if ilosc == manager.magazyn[magazyn_mv[0]][2]:
                            del manager.magazyn[magazyn_mv[0]]
                            manager.konto += magazyn_mv[2] * magazyn_mv[3]
                            manager.execute("nadpisz_saldo", manager.konto)
                            manager.execute("nadpisz_magazyn", manager.magazyn)
                            print(f"Sprzedano caly zapas produktu o nazwie: {magazyn_mv[1]} i cenie: {magazyn_mv[2]}")
                            manager.execute("wczytaj_historie")
                            manager.execute("zapisz_historie", len(manager.historia)+1,
                                            'sprzedaz', nazwa, float(cena), ilosc)
                        # jesli taki produkt istnieje modyfikujemy tylko ilosc sztuk
                        else:
                            x = manager.magazyn[magazyn_mv[0]][1]
                            y = manager.magazyn[magazyn_mv[0]][2] - ilosc
                            manager.magazyn[magazyn_mv[0]] = [nazwa, x, y]
                            manager.konto += magazyn_mv[2] * magazyn_mv[3]
                            manager.execute("nadpisz_saldo", manager.konto)
                            manager.execute("nadpisz_magazyn", manager.magazyn)
                            print(f"Zmodyfikowano ilosc produktu o nazwie: {magazyn_mv[1]} i cenie: {magazyn_mv[2]} "
                                  f"obecny stan to {manager.magazyn[magazyn_mv[0]][2]}")
                            manager.execute("wczytaj_historie")
                            manager.execute("zapisz_historie", len(manager.historia)+1,
                                            'sprzedaz', nazwa, float(cena), ilosc)
    # koniec - konczymy program
    elif operacja == "koniec":
        print("Koniec programu")
        break
