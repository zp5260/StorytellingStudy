import csv

# Definicija slovarja za shranjevanje imen in odgovorov
podatki = []

# Branje CSV datoteke
with open('preQa.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Pridobivanje imena in odgovora na izbrani vprašanji
        ime = row['Person']
        odgovor_videoigre = row['Koliko ur na mesec zdaj igrate videoigre?']
        odgovor_glasba = row['Ali ste se na kakršenkoli način ukvarjali z glasbo ali dejavnostmi povezanimi z glasbo (petje, ples...)?']

        # Dodajanje imena in odgovorov v seznam
        podatki.append({'Ime': ime, 'Odgovor na videoigre': odgovor_videoigre, 'Odgovor na glasbo': odgovor_glasba})

# Ustvarjanje nove CSV datoteke s pridobljenimi podatki
with open('izbrani_podatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Ime', 'Odgovor na videoigre', 'Odgovor na glasbo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for podatek in podatki:
        writer.writerow(podatek)

print("Podatki so bili uspešno shranjeni v datoteko 'izbrani_podatki.csv'.")
