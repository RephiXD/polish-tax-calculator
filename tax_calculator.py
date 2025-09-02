MINIMALNA_SKLADKA_ROCZNA = 4581.36 #2025r.
STAWKA_PODATEK_LINIOWY = 0.19
STAWKA_SKALA_PODATKOWA_I = 0.12
STAWKA_SKALA_PODATKOWA_II = 0.32
PROG_SKALA_PODATKOWA_I = 30000
PROG_SKALA_PODATKOWA_II = 120000

def pobierz_dodatnia_wartosc(komunikat): # 0 również
    while True:
        try:
            wartosc = float(input(komunikat))
            if wartosc < 0:
                print("Błąd: Wartość nie może być ujemna. Spróbuj ponownie.")
            else:
                return wartosc
        except ValueError:
            print("Błąd: Wprowadzono niepoprawny format liczby. Spróbuj ponownie.")

def pobierz_rok_w_zakresie(komunikat):
    while True:
        try:
            wartosc = int(input(komunikat))
            if 2030 >= wartosc >= 2022:
                return wartosc
            else:
                print("Błąd: Rok nie jest w oczekiwanym zakresie (2022-2030). Spróbuj ponownie.")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawny format liczby. Spróbuj ponownie.")

def pobierz_stawke_ryczaltu(komunikat):
    while True:
        try:
            wartosc = float(input(komunikat))
            if 0 <= wartosc <= 17:  # stawki ryczałtu 0-17%
                return wartosc / 100  # zwracamy jako wartość dziesiętną
            else:
                print("Błąd: stawka musi być między 0 a 17%. Spróbuj ponownie.")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawny format liczby. Spróbuj ponownie.")

def oblicz_dochod(przychod, koszty):
    return przychod - koszty

def oblicz_skladke_zdrowotna_skala(dochod):
    return max(dochod * 0.09, MINIMALNA_SKLADKA_ROCZNA)

def oblicz_skladke_zdrowotna_linia(dochod):
    return max(dochod * 0.049, MINIMALNA_SKLADKA_ROCZNA)

def oblicz_podatek_skala(dochod):
    if dochod <= PROG_SKALA_PODATKOWA_I:
        podatek = 0
    elif PROG_SKALA_PODATKOWA_II >= dochod > PROG_SKALA_PODATKOWA_I:
        podatek = (dochod - PROG_SKALA_PODATKOWA_I)*STAWKA_SKALA_PODATKOWA_I
    elif dochod > PROG_SKALA_PODATKOWA_II:
        podatek = (dochod - PROG_SKALA_PODATKOWA_II)*STAWKA_SKALA_PODATKOWA_II + (PROG_SKALA_PODATKOWA_II - PROG_SKALA_PODATKOWA_I) * STAWKA_SKALA_PODATKOWA_I #podatek dla 120 000zł = 10 800zł
    return podatek

def oblicz_podatek_liniowy(dochod):
    podatek = (dochod) * STAWKA_PODATEK_LINIOWY
    return podatek

def oblicz_podatek_ryczalt(przychod, stawka):
    return przychod * stawka

def drukuj_raport(rok, dochod, podatek_skala, podatek_linia, skladka_skala, skladka_linia, podatek_ryczalt, dochod_po_skali, dochod_po_linii, dochod_po_ryczalcie):
    print(f"Dochód za rok {rok} wynosi {dochod:_.2f}zł.".replace('_', ' '))
    print(f"Skala podatkowa: {podatek_skala:_.2f} zł. Składka zdrowotna: {skladka_skala:_.2f} zł. Dochód netto: {dochod_po_skali:_.2f} zł.".replace('_', ' '))
    print(f"Podatek liniowy: {podatek_linia:_.2f} zł. Składka zdrowotna: {skladka_linia:_.2f} zł. Dochód netto: {dochod_po_linii:_.2f} zł.".replace('_', ' '))
    print(f"Ryczałt: podatek {podatek_ryczalt:_.2f} zł, dochód netto {dochod_po_ryczalcie:_.2f} zł.".replace('_', ' '))

    max_docho = max(dochod_po_skali, dochod_po_linii, dochod_po_ryczalcie)
    if max_docho == dochod_po_skali:
        print("Najkorzystniejsza forma: skala podatkowa.")
    elif max_docho == dochod_po_linii:
        print("Najkorzystniejsza forma: podatek liniowy.")
    else:
        print("Najkorzystniejsza forma: ryczałt.")


def main():
    rok = pobierz_rok_w_zakresie("Jaki rok chciałbyś rozliczyć? (2022-2030) ")
    przychod = pobierz_dodatnia_wartosc("Podaj przychód w złotówkach za obecny rok. ")
    koszty = pobierz_dodatnia_wartosc(f"Jakie koszty w złotówkach poniosła twoja działalność w roku {rok} ? ")

    dochod = oblicz_dochod(przychod, koszty)
    stawka_ryczalt = pobierz_stawke_ryczaltu("Podaj swoją stawkę ryczałtu. ")

    if przychod > 0:
        podatek_ryczalt = oblicz_podatek_ryczalt(przychod, stawka_ryczalt)
        dochod_po_ryczalcie = (przychod - podatek_ryczalt) - koszty
    else:
        podatek_ryczalt = 0.0
        dochod_po_ryczalcie = dochod

    if dochod > 0:
        podatek_skala = oblicz_podatek_skala(dochod)
        podatek_linia = oblicz_podatek_liniowy(dochod)

        skladka_skala = oblicz_skladke_zdrowotna_skala(dochod)
        skladka_linia = oblicz_skladke_zdrowotna_linia(dochod)

        podatek_linia_po_odliczeniu = max(podatek_linia - (skladka_linia * 0.5), 0)

        dochod_po_skali = dochod - (podatek_skala + skladka_skala)
        dochod_po_linii = dochod - (podatek_linia_po_odliczeniu + skladka_linia)

    else:
        podatek_skala = 0.0
        podatek_linia = 0.0
        podatek_ryczalt = 0.0
        skladka_skala = MINIMALNA_SKLADKA_ROCZNA
        skladka_linia = MINIMALNA_SKLADKA_ROCZNA
        dochod_po_skali = dochod - skladka_skala
        dochod_po_linii = dochod - skladka_linia
        print("Za bieżący rok poniosłeś stratę lub wyszedłeś na zero. Podatek wynosi 0 zł.")

    drukuj_raport(rok, dochod, podatek_skala, podatek_linia, skladka_skala, skladka_linia, podatek_ryczalt, dochod_po_skali, dochod_po_linii, dochod_po_ryczalcie)

if __name__ == "__main__":
    main()
