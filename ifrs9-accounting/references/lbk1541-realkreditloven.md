# LBK 1541 — Lov om realkreditlån og realkreditobligationer m.v.

Reference: Lovbekendtgørelse nr. 1541 af 18/11/2025.
Kilde: https://www.retsinformation.dk/eli/lta/2025/1541

## Indholdsfortegnelse

1. [Matchfunding-definitionen (§ 1a)](#1-matchfunding)
2. [Midlernes anvendelse og koncernintern funding (§ 20)](#2-midlerne)
3. [Balanceprincippet (§ 18a)](#3-balanceprincippet)
4. [Refinansiering og obligationsforlængelse (§ 6)](#4-refinansiering)
5. [Lånegrænser (§ 5)](#5-lånegrænser)
6. [Obligationstyper (§ 18, § 33a, § 33b)](#6-obligationstyper)
7. [Matched funding-effekt på P&L](#7-matched-funding-effekt)
8. [Kursskæring vs. kursregulering](#8-kursskæring-vs-kursregulering)
9. [Koncernintern realkreditstruktur (§ 20, stk. 3)](#9-koncernintern)

---

## 1. Matchfunding-definitionen (§ 1a, nr. 1)

Matchfunding er lovdefineret i § 1a, nr. 1:
Et system der sikrer at betalingsstrømmene mellem forpligtelser og aktiver matches ved kontraktlige vilkår, så:
(a) betalinger fra låntagere og derivatmodparter forfalder, FØR der foretages udbetalinger til investorer i RO/SDRO/SDO og derivatmodparter,
(b) de modtagne beløb værdimæssigt mindst svarer til udbetalingerne,
(c) de modtagne beløb inkluderes i serien med seriereservefond eller gruppen af serier med fælles seriereservefond, indtil betalingerne til investorerne forfalder.

§ 1a, nr. 2 definerer "udgående nettopengestrømme" som alle udgående betalingsstrømme der forfalder på en dag (hovedstol, rente, derivatbetalinger) fratrukket alle indgående betalingsstrømme der forfalder samme dag for krav relateret til dækkende aktiver.

Regnskabsmæssig konsekvens: Matchfunding sikrer at kursregulering (IFRS 9 5.7.1) på aktiv og passiv er identisk — samme kurs, samme nominel, samme serie. Al kursregulering netter til 0 i P&L.

---

## 2. Midlernes anvendelse og koncernintern funding (§ 20)

**§ 20, stk. 1:** Midler fremkommet ved udstedelse af RO eller SDRO eller andre finansielle instrumenter kan ALENE anvendes til udlån mod pant i fast ejendom eller til udlån til offentlig myndighed/mod selvskyldnergaranti fra offentlig myndighed. Dog kan der stilles supplerende sikkerhed for SDRO (jf. § 33d, stk. 1).

**§ 20, stk. 2:** Finanstilsynet kan fastsætte regler om, at midler i begrænset omfang kan anvendes til andet end udlån mod pant i fast ejendom (jf. BEK 1425 om obligationsudstedelse, balanceprincip og risikostyring).

**§ 20, stk. 3 — Koncernintern funding:** Finanstilsynet kan tillade, at der i koncernforhold kan udstedes RO, SDO, SDRO og andre finansielle instrumenter i ét realkreditinstitut til finansiering af realkreditlån i et ANDET realkreditinstitut. Forudsætninger:
(1) Det udstedende institut har til hensigt at sælge obligationerne til aftagere der IKKE er koncernforbundne.
(2) Obligationer udstedt af ét realkreditinstitut til brug for det koncernforbundne instituts udstedelse på markedet skal overdrages til EJE.

Regnskabsmæssig konsekvens: § 20, stk. 3 er hjemlen for koncerninterne realkreditstrukturer, hvor ét realkreditinstitut yder realkreditlånet mens et andet koncernforbundet realkreditinstitut udsteder obligationerne. Obligationerne overdrages til eje mellem institutterne. Bogføring følger IFRS 9, men den juridiske struktur er to separate realkreditinstitutter med koncerninterne flows.

---

## 3. Balanceprincippet (§ 18a)

Alle betalingsforpligtelser vedrørende RO skal være dækket af betalingskrav der vedrører de dækkende aktiver i de enkelte serier med seriereservefond eller gruppen af serier med fælles seriereservefond.

Balanceprincippet operationaliseres i BEK 1425 (Obligationsbekendtgørelsen), der definerer to varianter:
- **Specifikt princip (BEK 1425 kap. 3):** Klassisk 1:1-match. Konverterbar-til-konverterbar. Netting er perfekt.
- **Overordnet princip (BEK 1425 kap. 2):** Stresstestbaseret. Tillader betalingsforskelle inden for risikogrænser. Netting er tilnærmet men ikke perfekt.

Se `references/bek1425-balanceprincip.md` for detaljer.

Regnskabsmæssig konsekvens: Under det specifikke princip er korrespondancen 1:1, og kursregulering netter perfekt. Under det overordnede princip kan residuale betalingsforskelle skabe P&L-volatilitet ud over kursskæring.

---

## 4. Refinansiering og obligationsforlængelse (§ 6)

Når løbetiden på realkreditlån er længere end obligationernes løbetid (RTL-lån), gælder:

- **§ 6, stk. 1:** Fast forrentede obligationer ≤ 12 mdr. ved refinansiering: renteloft +5pp ift. seneste refinansiering. Ved manglende salg: tvungen forlængelse 12 mdr.
- **§ 6, stk. 2:** Fast forrentede 12-24 mdr.: renteloft +5pp ift. tilsvarende obligation 11-14 mdr. tidligere.
- **§ 6, stk. 3:** Variabelt forrentede ≤ 24 mdr.: rente kan ikke stige mere end +5pp, og forbliver uændret i 12 mdr.
- **§ 6, stk. 5:** Generel forlængelsesregel: 12 mdr. ad gangen indtil refinansiering lykkes.
- **§ 6, stk. 7-9:** Rentefastsættelse ved forlængelse: seneste rente +5pp.
- **§ 6, stk. 11:** Forlængelse fratager IKKE låntager retten til hel eller delvis indfrielse.

Regnskabsmæssig konsekvens: Ved refinansiering sker derecognition (IFRS 9 3.3.1) af den gamle obligation og initial recognition (5.1.1) af den nye. Kursdifferencer ved refinansiering er realiseret P&L. I matched funding netter dette stadig, da udlånets FV-justering modsvarer den nye obligations FV. Ved tvungen forlængelse (§ 6, stk. 5) forbliver den eksisterende obligation i bøgerne med ny rente — ingen derecognition, men renteændringen påvirker FV og dermed kursregulering.

---

## 5. Lånegrænser (§ 5)

| Ejendomskategori | Lånegrænse | § 5, stk. |
|---|---|---|
| Ejerboliger helår, andel, alment, udlejning, ældreboliger, sociale/kulturelle | 80% | stk. 1 |
| Fritidshuse (private) | 75% | stk. 2 |
| Landbrug/skovbrug, gartnerier | 70% | stk. 3 |
| Fritidshuse (erhverv), kontor, industri, energi, datacentre | 60% | stk. 4 |
| Øvrige (ubebyggede grunde m.v.) | 40% | stk. 5 |

Lånegrænserne er ikke direkte IFRS 9-relevante, men er vigtig kontekst ved scenarieopsætning. For SDRO/SDO skal lånegrænserne overholdes LØBENDE (§ 33c/33d), ikke kun ved oprettelse.

Supplerende sikkerhed (§ 33d, stk. 1): Falder ejendomsværdien så lånegrænsen overskrides, skal instituttet stille supplerende sikkerhed i registret/serien. Disse aktiver skal IFRS 9-klassificeres.

---

## 6. Obligationstyper i dansk realkredit

| Type | Forkortelse | Lovhjemmel | Dækkende aktiver |
|---|---|---|---|
| Realkreditobligationer | RO | § 18 | Pantebreve i serien |
| Særligt dækkede realkreditobligationer | SDRO | § 33a | Pantebreve + suppl. sikkerhed |
| Særligt dækkede obligationer | SDO | § 33b | Bredere aktivtyper (art. 129 CRR) |

Alle tre typer kan designeres FVTPL under IFRS 9 (4.2.2(b)) for at matche FVTPL-udlån.

SDRO vs. RO: SDRO kræver løbende overholdelse af lånegrænser (§ 33c) og mulighed for supplerende sikkerhed (§ 33d). RO kræver kun overholdelse ved oprettelse. De fleste nye udstedelser er SDRO.

---

## 7. Matched funding-effekt på P&L

Når aktiv og passiv er i SAMME serie (specifikt balanceprincip):
- Kursregulering på aktiv og passiv er identisk (samme kurs, samme nominel)
- Al kursregulering netter til 0 i P&L
- Afdrag og udtrækning er symmetriske → netter til 0
- Indfrielse og prepayment er symmetriske → netter til 0
- **Eneste permanente P&L = kursskæring (IFRS 9 B5.1.2A)**

Balanceligning for matched funding:
```
Kasse + Udlån_FV − Obl_FV = Urealiseret + Realiseret = Total P&L
```

Da kursregulering netter:
```
Total P&L = Σ Kursskæring_i  (for alle udlån i)
```

---

## 8. Kursskæring vs. kursregulering

| Begreb | Definition | Hjemmel | P&L-type |
|---|---|---|---|
| Kursskæring | FV(mid) − Udbetalingskurs ved oprettelse | IFRS 9 B5.1.2A | Realiseret, dag 1 |
| Kursregulering | ΔFV grundet markedskursændring | IFRS 9 5.7.1 | Urealiseret (netter til 0 i matched funding) |

---

## 9. Koncernintern realkreditstruktur (§ 20, stk. 3)

Hvor to realkreditinstitutter er koncernforbundne, kan det ene udstede obligationer til finansiering af det andets udlån. Forholdet er koncerninternt (realkredit-til-realkredit) og reguleres af LBK 1541 § 20, stk. 3. Det er IKKE FIL § 16b (som kun gælder pengeinstitut-til-realkreditinstitut).

Strukturen:
- Det långivende realkreditinstitut yder realkreditlån til låntagere (§ 2).
- Det udstedende realkreditinstitut udsteder obligationer til finansiering af det långivende instituts udlån (§ 20, stk. 3).
- Obligationerne overdrages til eje (§ 20, stk. 3, nr. 2).
- Det udstedende institut sælger obligationerne til markedet til ikke-koncernforbundne aftagere (§ 20, stk. 3, nr. 1).

Bogføringsmæssigt: Begge institutter IFRS 9-bogfører hver deres side. Det långivende institut har udlånet (fx FVTPL aktiv) og en koncernintern forpligtelse. Det udstedende institut har den koncerninterne fordring og den udstedte obligation (fx FVTPL passiv). Matched funding-netting sker på koncernniveau, ikke nødvendigvis i hvert enkelt institut.
