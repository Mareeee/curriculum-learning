# Teorija prostora znanja (KST) i učenje po kurikulumu

## Cilj
Proveriti da li se KST može koristiti za pravljenje kurikuluma za neuronske mreže. Mreže zaustavljene u nasumičnom trenutku tretiram kao "učenike", IITA iz njihovih odgovora izvodi relacije preduslova, a te relacije poredim sa ljudskim. Cilj je empirijska analiza.

## Istraživačka pitanja
1. Da li mreže uče veštine u redosledu sličnom ljudskom?
2. Gde se graf preduslova mreža poklapa sa ljudskim, a gde ne?
3. Da li kurikulum izveden iz KST grafa poboljšava učenje u odnosu na kontrole?
4. Koliko je graf stabilan (prag "rešeno", gustina, seedovi)?

## Ideja ukratko
- **Zadaci:** sopstveni generator sa seedom, jedan tekstualni zapis (npr. `73-58=`, `3/4-3/8=`). Oko 14 tipova: celi brojevi (sabiranje, oduzimanje sa pozajmicama, množenje) i razlomci (oduzimanje, mešoviti brojevi, skraćivanje, množenje).
- **Učenici:** mnogo nezavisnih malih transformera na nivou znakova (različit seed, veličina, redosled), svaki uči mešavinu svih tipova i staje jednom u nasumičnom trenutku.
- **Matrice:** (mreže × tipovi) za IITA i (mreže × pravi ljudski zadaci) za poređenje.
- **Poređenje sa ljudima:** `schoolarithm` (oduzimanje celih brojeva, 294 učenika × 8 zadataka) i Tatsuoka oduzimanje razlomaka (536 × 20 + Q-matrica veština). Ti zadaci se izbacuju iz treninga. Poredi se struktura (ivice preduslova, težina zadataka), ne broj koraka.
- **Kurikulum:** faze po veštinama (bez preduslova, sledeći sloj, sve). Kontrole sa istim budžetom: KST, ljudski, nasumičan, obrnut, ravnomerna mešavina, bez kurikuluma. Cilj 5 seedova.

## Koraci
1. Pretraga literature i skupova podataka
2. Definisanje tipova zadataka i ručnog ljudskog grafa
3. Probni trening (naučivost tipova, prag "rešeno", vreme jednog treninga)
4. Trening N mreža i pravljenje matrica
5. IITA (R paket DAKS): smer ivica, gustina grafa, poređenje sa ljudskim
6. Kurikulumi i kontrole
7. Rezultati i zaključci

## Rizici
- Tip koji niko ne reši (ili svi reše) ne nosi informaciju za IITA.
- Prag "rešeno" menja graf; graf može ispasti skoro prazan ili skoro pun.
- Veze između oblasti mogu poticati od zajedničkog zapisa, ne od zajedničke veštine.
- Ljudski podaci pokrivaju samo oduzimanje (celi brojevi i razlomci).
- Kurikulum će verovatno dati malu ili nikakvu korist, što je prihvatljivo.

## Literatura
- Chen et al., *Skill-it!*, NeurIPS 2023, [arXiv 2307.14430](https://arxiv.org/abs/2307.14430)
- Hložan i Segedinac, *Obučavanje dubokih neuronskih mreža vođeno prostorom znanja*, FTN, [DOI 10.24867/24BE18Hlozan](https://doi.org/10.24867/24BE18Hlozan)
- Lee et al., *Teaching Arithmetic to Small Transformers*, ICLR 2024, [arXiv 2307.03381](https://arxiv.org/abs/2307.03381)
- Ünlü i Sargin, *DAKS*, J. Stat. Softw. 37(2), 2010
- Tatsuoka, C., J. R. Stat. Soc. C 51(3), 2002; de Chiusole i Stefanutti, ENDM 42, 2013 (dokumentacija paketa, originali neotvoreni)
- Wu, Dyer i Neyshabur, *When Do Curricula Work?*, ICLR 2021 (proveriti pre citiranja)
