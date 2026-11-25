# Teorija prostora znanja (KST) i učenje po kurikulumu

## Cilj
Proveriti da li se KST može koristiti za pravljenje kurikuluma za neuronske mreže. Mreže zaustavljene u nasumičnom trenutku tretiram kao "učenike", IITA iz njihovih odgovora izvodi relacije preduslova, a te relacije poredim sa ljudskim. Cilj je empirijska analiza, ne to da kurikulum "uspe".

## Istraživačka pitanja
1. Da li mreže uče veštine u redosledu sličnom ljudskom?
2. Gde se graf preduslova mreža poklapa sa ljudskim, a gde ne?
3. Da li kurikulum izveden iz KST grafa poboljšava učenje u odnosu na kontrole?
4. Koliko je graf stabilan (prag "rešeno", gustina, seedovi)?

## Ideja ukratko
- **Zadaci:** sopstveni generator sa seedom, jedan tekstualni zapis (npr. `73-58=`, `3/4-3/8=`). Celi brojevi i razlomci spojeni u jednu oblast, da graf može da pokaže i veze između oblasti.
- **Učenici:** mnogo nezavisnih malih transformera na nivou znakova (različit seed, veličina, redosled), svaki uči mešavinu svih tipova i staje jednom u nasumičnom trenutku.
- **Matrice:** (mreže × tipovi) za IITA i (mreže × pravi ljudski zadaci) za poređenje.
- **Poređenje sa ljudima:** Tatsuoka oduzimanje razlomaka (536 učenika × 20 zadataka + Q-matrica veština). Ti zadaci se izbacuju iz treninga. Poredi se struktura (ivice preduslova, težina zadataka), ne broj koraka.
- **Kurikulum:** faze po veštinama (bez preduslova, sledeći sloj, sve). Kontrole sa istim budžetom: KST, ljudski, nasumičan, obrnut, ravnomerna mešavina, bez kurikuluma. Cilj 5 seedova.

## Metodologija i rezultati (dnevnik)

### ```01.11.2026.``` priprema
- Razradio zadatak i beleške: mreže zaustavljene nasumično daju obrasce rešeno/nerešeno, IITA iz njih izvodi preduslove, iz preduslova se pravi kurikulum.
- Pretraga literature: Skill-it! (Chen et al.) i rad Hložan i Segedinac pročitani u celini, ostalo pregledano samo delimično (vidi Literatura).
- Pretraga ljudskih skupova odgovora: razmatrani `schoolarithm`, `fraction17`, Tatsuoka, Eedi, ASSISTments, Peru (Zenodo) i AMATUS. Odbačeni su oni sa retko popunjenom matricom, višestrukim izborom ili neprikladnom populacijom.
- Odluka da radim sa sopstvenim generatorom zadataka, jer javni skupovi ne pokrivaju sve operacije.

### ```10.11.2026.``` generator i ljudski skup
- **Generator (`generator.py`):** 19 tipova zadataka (7 celobrojnih, 12 razlomaka), generisanje sa seedom, izlaz u CSV (`zadaci.csv`, 1900 zadataka pri 100 po tipu). Rešenja sam proverio ponovnim računanjem: 0 pogrešnih. U proveri uzorkom (5000 po tipu) nijedan zapis ne pripada više od jednom tipu.
- **Tatsuoka zadaci (`tatsuoka_zadaci.csv`):** 20 stavki prepisano u isti zapis kao generisani zadaci, sa tačnim rešenjem i dodeljenim tipom. Sve stavke generator može da proizvede (proveren uzorkom). Stavke pokrivaju 10 od 19 tipova, ostali služe samo za poređenje mašina sa mašinom.
- **Ljudski odgovori (`tatsuoka_odgovori.csv`, `tatsuoka_Q.csv`):** preuzeti iz R paketa GDINA (`realdata_Tatsuoka1990`) preko `main.py`. Odgovori: 536 × 20, samo 0/1, bez rupa (367 različitih obrazaca). Q-matrica: 20 × 8. Kodiranje 1 = tačno proveren po težini stavki (najlakše su stavke sa istim imeniocem, najteže one sa pozajmicom i različitim imeniocima).
- **Ručni graf preduslova (`prostor znanja.svg`):** 13 čvorova (grupe stavki iz 17 od 20 stavki), 17 ivica. Pravilo: veštine A su pravi podskup veština B. Veštine čvorova sam uporedio sa Q-matricom i poklapaju se za sve stavke na slici. Graf sadrži sve ivice pokrivanja tog pravila, bez tranzitivno suvišnih. Stavke 4, 19 i 20 (jedine sa veštinom 3) nisu na slici.

![Ručni graf preduslova za Tatsuoka stavke](prostor%20znanja.svg)

### ```22.11.2026.``` Q-matrica i IITA
- Razjasnio sam razliku: Q-matrica je tabela koju pišu stručnjaci (koja stavka traži koje veštine), a iz nje se računa graf preduslova. IITA pravi graf samo iz tačnih i netačnih odgovora učenika, bez znanja o veštinama.
- Odluka: ove nedelje prvo MLP, a transformer tek ako MLP uspe.

### ```23.11.2026.``` Q-graf i IITA na ljudskim podacima
- **Q-graf:** stavka `a` je preduslov za `b` ako su veštine stavke `a` deo veština stavke `b`. Dobio sam 101 par i graf se poklapa sa mojim ručnim crtežom (17 od 17 ivica). To nije nezavisna provera, jer je crtež napravljen iz iste Q-matrice.
- **IITA:** napisao sam je u Pythonu (jedna od tri varijante, minimalno korigovana). Nisam je poredio sa originalnim R paketom DAKS, jer nemam R. Na simuliranim učenicima, napravljenim iz Q-grafa, pronalazi 99 od 101 pravih parova, uz 21 višak.
- **Rezultat na 536 učenika:** IITA daje 204 para koji se slažu u jedan lanac od 12 koraka, bez grananja. Sa Q-grafom ima 91 zajednički par (Jaccard 0,43). Svih 10 parova koje ima samo Q-graf imaju "preduslov" koji je rešen ređe od stavke koja od njega zavisi.
- Kod sam podelio u pakete `kst/` i `tasks/`, a podatke u `data/`.

![IITA graf za ljudske podatke](iita_graph.png)

### ```25.11.2026.``` provera lanca i čišćenje zadataka
- **Zašto je graf jedan lanac:** kod je u redu, lanac se ponovi i kad ponovo nasumično izvučem učenike, a redosled stavki prati njihovu težinu. Verovatno je razlog to što su sve stavke iz iste oblasti, pa ko je dobar rešava sve. To je pretpostavka, nisam je testirao.
- **Čišćenje zadataka:** iz `tasks.csv` sam izbacio duplikate i 20 Tatsuoka zadataka, a cilj je 1000 zadataka po tipu (ranije 100). Ukupno ih je 14332, jer 7 tipova nema dovoljno različitih zadataka (npr. množenje jednocifrenih ima samo 64). Ostaje nejednak broj po tipu.
- Ranijih 1900 zadataka je 19 tipova × 100. Tatsuoka stavke nisu dodatni zadaci, nego primeri unutar tipova.
- **Format odgovora:** `3/2`, skraćen razlomak. Ceo broj je bez imenioca (`2`), a mešoviti brojevi se pojavljuju samo u zadacima, ne u odgovorima.

### Početni plan i trenutna odluka

| | Početni plan | Sada |
|---|---|---|
| Tipova zadataka | oko 14 (7 + 7) | 19 (7 celih + 12 razlomaka) |
| Zašto | nacrt, nije bio konačan | morali smo da pokrijemo svih 20 Tatsuoka stavki (nepravi razlomci, mešoviti brojevi, različiti imenioci) |
| Ljudski skupovi | `schoolarithm` + Tatsuoka (+ `fraction17` opciono) | samo Tatsuoka |
| Celi brojevi | poređenje sa decom (`schoolarithm`) | samo mašina sa mašinom, jer `schoolarithm` ima samo oduzimanje sa pozajmicom |

### Zapažanja i otvorena pitanja
- Prva verzija generatora je mogla da proizvede samo 4 od 20 Tatsuoka stavki (2, 6, 15, 16), pa sam dodao tipove i proširio imenioce.
- Tip sa skraćivanjem rezultata se preklapao sa tipom sa istim imeniocem. Popravljeno: oni sada ne dele zapise.
- Mali prostor zadataka daje mnogo duplikata (npr. množenje jednocifrenih: 55 od 100). Rešeno 25.11.: duplikati i 20 Tatsuoka stavki su izbačeni.
- Veština 3 ("skraćivanje pre oduzimanja") je u Q-matrici u stavkama 4, 19 i 20, što se slaže sa tabelom iz arXiv 1303.0426, a ne sa tvrdnjom u radu da je samo u stavci 4. Stavka 11 ima nepravi razlomak, ali nema veštinu 3.
- Format odgovora odlučen 25.11.: `3/2`, skraćen.

## Koraci
1. Pretraga literature i skupova podataka - urađeno
2. Definisanje tipova zadataka i ručnog ljudskog grafa - u toku (tipovi i graf gotovi, mapiranje na veštine delimično)
3. Probni trening (naučivost tipova, prag "rešeno", vreme jednog treninga)
4. Trening N mreža i pravljenje matrica
5. IITA (R paket DAKS): smer ivica, gustina grafa, poređenje sa ljudskim
6. Kurikulumi i kontrole
7. Rezultati i zaključci

## Struktura projekta
```
main.py                    generiše zadatke i Tatsuoka stavke
download_human_data.py     ponovno preuzimanje ljudskih podataka iz R-a (traži R)
project_paths.py           putanje do svih fajlova sa podacima
tasks/                     generator zadataka (celi brojevi, razlomci, Tatsuoka stavke)
kst/                       Q-matrica, IITA, simulacija, crtanje grafova
notebooks/                 01_q_graph.ipynb, 02_iita.ipynb
data/generated/tasks.csv   generisani zadaci
data/tatsuoka/             items.csv, answers.csv, q_matrix.csv
```
Dnevnik ispod pominje stara imena fajlova (`generator.py`, `zadaci.csv`, `tatsuoka_zadaci.csv`, `tatsuoka_odgovori.csv`, `tatsuoka_Q.csv`). Nova imena su u strukturi iznad.

## Pokretanje
`python main.py` generiše `data/generated/tasks.csv` i `data/tatsuoka/items.csv`. Ljudski podaci (`answers.csv`, `q_matrix.csv`) su već u projektu. Za ponovno preuzimanje treba R: `python download_human_data.py`. Notebook-ovi se pokreću iz `notebooks/` (`jupyter lab`).

## Rizici
- Tip koji niko ne reši (ili svi reše) ne nosi informaciju za IITA.
- Prag "rešeno" menja graf; graf može ispasti skoro prazan ili skoro pun.
- Veze između oblasti mogu poticati od zajedničkog zapisa, ne od zajedničke veštine.
- Ljudski podaci pokrivaju samo oduzimanje razlomaka. Za celobrojne operacije i množenje nema ljudskog poređenja.
- Kurikulum će verovatno dati malu ili nikakvu korist, što je prihvatljivo.

## Literatura
- Chen et al., *Skill-it!*, NeurIPS 2023, [arXiv 2307.14430](https://arxiv.org/abs/2307.14430)
- Hložan i Segedinac, *Obučavanje dubokih neuronskih mreža vođeno prostorom znanja*, FTN, [DOI 10.24867/24BE18Hlozan](https://doi.org/10.24867/24BE18Hlozan)
- Lee et al., *Teaching Arithmetic to Small Transformers*, ICLR 2024, [arXiv 2307.03381](https://arxiv.org/abs/2307.03381) (pregledan samo apstrakt)
- Ünlü i Sargin, *DAKS*, J. Stat. Softw. 37(2), 2010 (pregledana dokumentacija)
- Tatsuoka, C., J. R. Stat. Soc. C 51(3), 2002 (original neotvoren, podaci iz R paketa GDINA)
- Wu, Dyer i Neyshabur, *When Do Curricula Work?*, ICLR 2021 (proveriti pre citiranja)