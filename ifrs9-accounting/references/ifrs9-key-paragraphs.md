# IFRS 9 — Nøgleparagraffer til bogføring

Reference: IFRS 9 Financial Instruments (2014, senest konsolideret 2021)
Kilde: https://www.ifrs.org/content/dam/ifrs/publications/pdf-standards/english/2021/issued/part-a/ifrs-9-financial-instruments.pdf

## Indholdsfortegnelse

1. [Klassifikation af finansielle aktiver](#1-klassifikation)
2. [Klassifikation af finansielle forpligtelser](#2-forpligtelser)
3. [Initial recognition og måling](#3-initial-recognition)
4. [Efterfølgende måling — FVTPL](#4-fvtpl)
5. [Efterfølgende måling — FVOCI](#5-fvoci)
6. [Amortiseret kostpris og effektiv rente](#6-amortiseret-kostpris)
7. [Impairment / ECL](#7-impairment)
8. [Derecognition](#8-derecognition)
9. [Hedge accounting](#9-hedge-accounting)
10. [Reklassifikation](#10-reklassifikation)
11. [Matched funding og realkreditspecifik](#11-matched-funding)

---

## 1. Klassifikation af finansielle aktiver

### 4.1.1 — Forretningsmodel og cash flow-karakteristik
Et finansielt aktiv klassificeres baseret på:
(a) virksomhedens forretningsmodel for styring af de finansielle aktiver, og
(b) cash flow-karakteristikken (SPPI-test: solely payments of principal and interest).

### 4.1.2 — Amortiseret kostpris
Et aktiv måles til amortiseret kostpris hvis begge betingelser er opfyldt:
(a) hold-to-collect forretningsmodel, og
(b) SPPI er opfyldt.

### 4.1.2A — FVOCI (gæld)
Måles til FVOCI hvis:
(a) hold-to-collect-and-sell forretningsmodel, og
(b) SPPI er opfyldt.

### 4.1.4 — FVTPL (residual)
Alle aktiver der ikke opfylder 4.1.2 eller 4.1.2A måles til FVTPL.
Virksomheden kan også vælge FVTPL-designation (fair value option) ved initial recognition for at eliminere accounting mismatch (4.1.5).

---

## 2. Klassifikation af finansielle forpligtelser

### 4.2.1 — Hovedregel: Amortiseret kostpris
Alle finansielle forpligtelser måles til amortiseret kostpris, medmindre:

### 4.2.2 — FVTPL-forpligtelser
(a) Held for trading, eller
(b) Designated til FVTPL ved initial recognition (fair value option).

Realkreditobligationer kan designeres FVTPL under 4.2.2(b) for at matche FVTPL-udlån og eliminere accounting mismatch.

---

## 3. Initial recognition og måling

### 5.1.1 — Initial recognition
Et finansielt aktiv eller forpligtelse indregnes når virksomheden bliver part i instrumentets kontraktlige vilkår.

### 5.1.1A — Køb eller salg af et finansielt aktiv
Regular way purchase/sale: indregnes på trade date eller settlement date (konsistent valg).

### 5.1.1 + B5.1.1 — Måling ved initial recognition
Til fair value. For aktiver/forpligtelser der ikke er FVTPL: plus/minus transaktionsomkostninger.
For FVTPL: transaktionsomkostninger i P&L.

### B5.1.2A — Day-one profit or loss (kursskæring)
Hvis transaktionsprisen afviger fra FV ved initial recognition, OG FV er baseret på:
- En observerbar pris i et aktivt marked for et identisk aktiv (Level 1), eller
- En værdiansættelse der kun bruger observerbare markedsdata (Level 2):

**Forskellen indregnes som day-one gain/loss i P&L.**

Formel:
```
Kursskæring = FV(mid) − Transaktionspris(udbetalingskurs)
```

For realkreditinstitutter: Mid-kurs på udstedelsesdagen minus udbetalingskurs til låntager = kursskæring, indregnet som realiseret P&L dag 1.

Hvis FV IKKE er Level 1/2, udskydes forskellen og amortiseres (B5.1.2A(b)).

---

## 4. Efterfølgende måling — FVTPL

### 5.7.1 — Gevinster og tab
For FVTPL-aktiver og -forpligtelser (undtagen 5.7.7):
**Alle gevinster og tab indregnes i P&L.**

Formel for kursregulering:
```
ΔFV_aktiv  = Nominel × (Kurs_ny − Kurs_gammel) / 100
ΔFV_passiv = Nominel × (Kurs_ny − Kurs_gammel) / 100

P&L_aktiv:  ΔFV > 0 → gevinst, ΔFV < 0 → tab
P&L_passiv: ΔFV > 0 → tab (forpligtelsen stiger), ΔFV < 0 → gevinst (forpligtelsen falder)
```

Bogføring:
- Aktiv stiger: Dr Aktiv / Cr Urealiseret (P&L)
- Aktiv falder: Dr Urealiseret (P&L) / Cr Aktiv
- Passiv stiger: Dr Urealiseret (P&L) / Cr Passiv
- Passiv falder: Dr Passiv / Cr Urealiseret (P&L)

### 5.7.7 — FVTPL-forpligtelser designated: own credit risk
For forpligtelser designated til FVTPL under 4.2.2(b):
- Ændringer i FV relateret til **own credit risk** → OCI
- Resterende FV-ændringer → P&L

Realkreditobligationer: typisk ingen own credit risk-separation, da obligationerne er pass-through og SDO/RO-sikrede. Hele kursreguleringen er markedsrisiko → P&L.

---

## 5. Efterfølgende måling — FVOCI

### 5.7.10-5.7.11 — FVOCI (gældsinstrumenter)
- FV-ændringer i OCI
- Effektiv rente-indtægt, ECL-impairment og valutakurseffekter i P&L
- Ved derecognition: kumulativ OCI reklassificeres til P&L

### 5.7.5 — FVOCI (egenkapitalinstrumenter, uigenkaldeligt valg)
- FV-ændringer i OCI
- Udbytte i P&L
- Ingen reklassificering til P&L — aldrig

---

## 6. Amortiseret kostpris og effektiv rente

### 5.4.1 — Effektiv rente-metode
Renteindtægt/-omkostning beregnes ved at applicere den effektive rente på bruttobeløbet (Stage 1/2) eller nettobogført beløb (Stage 3).

### 5.4.2 — Effektiv rente
Den rente der diskonterer forventede fremtidige cash flows til bogført værdi ved initial recognition.

Formel:
```
Renteindtægt = Effektiv rente × Bruttobeløb (Stage 1/2)
Renteindtægt = Effektiv rente × Nettobeløb  (Stage 3)
```

---

## 7. Impairment / ECL

### 5.5.1 — Grundprincip
En virksomhed skal indregne en hensættelse (loss allowance) for expected credit losses (ECL) på finansielle aktiver målt til amortiseret kostpris eller FVOCI.

### 5.5.3 — Stage 1: 12-måneders ECL
Ved initial recognition (og hvis kreditrisikoen ikke er steget signifikant): 12-måneders ECL.

```
ECL_12m = PD_12m × LGD × EAD
```

### 5.5.3 — Stage 2: Lifetime ECL
Hvis kreditrisikoen er steget signifikant siden initial recognition: lifetime ECL.

```
ECL_lifetime = Σ(PD_marginal_t × LGD_t × EAD_t × DF_t)  for t = 1..n
```

### 5.5.5 — Stage 3: Credit-impaired
Aktiver der er credit-impaired (default, >90 dage overdue, restruktureret):
- Lifetime ECL
- Rente beregnes på nettobeløb (5.4.1(a)(ii))

### 5.5.17 — Forenklinger
For trade receivables, contract assets og lease receivables: virksomheden KAN (og i visse tilfælde SKAL) bruge den forenklede tilgang (altid lifetime ECL, ingen Stage 1).

Bogføring af ECL-hensættelse:
```
Dr Impairment loss (P&L) / Cr Loss allowance (contra-aktiv)
```

Bogføring af ECL-tilbageførsel:
```
Dr Loss allowance / Cr Impairment loss (P&L)
```

**NB: FVTPL-aktiver er IKKE underlagt ECL-impairment.** Kreditrisiko er implicit i fair value.

---

## 8. Derecognition

### 3.2.3 — Derecognition af finansielle aktiver
Et finansielt aktiv derecogniseres når:
(a) de kontraktlige rettigheder til cash flows udløber, eller
(b) aktivet overdrages og overdragelsen opfylder kriterierne i 3.2.6.

### 3.3.1 — Derecognition af finansielle forpligtelser
En forpligtelse derecogniseres når den er indfriet, annulleret eller udløbet.

### 3.3.3 — Forskel ved derecognition af forpligtelse
Forskellen mellem bogført værdi og det betalte beløb indregnes i P&L.

Formel:
```
Realiseret_aktiv  = Modtaget beløb − Bogført FV
Realiseret_passiv = Bogført FV − Betalt beløb
```

Ved afdrag (delvis derecognition):
```
FV_fjernet = (Afdrag_nominel / Total_nominel) × FV_bogført
Realiseret = Afdrag_modtaget − FV_fjernet   (aktiv)
Realiseret = FV_fjernet − Afdrag_betalt     (passiv)
```

---

## 9. Hedge accounting

### 6.1.1 — Formål
Hedge accounting repræsenterer effekten af risikostyringsaktiviteter i regnskabet.

### 6.4.1 — Kvalificeringskriterier
(a) Kun eligible hedging instruments og hedged items
(b) Formel designation og dokumentation ved inception
(c) Hedgeforholdet opfylder effectiveness-kravene

### 6.5.2 — Fair value hedge
- Gain/loss på hedging instrument: P&L (eller OCI for FVOCI equity)
- Hedged item: justér bogført værdi for den hedgede risiko, i P&L

### 6.5.11 — Cash flow hedge
- Effektiv del af hedging instrument: OCI (cash flow hedge reserve)
- Ineffektiv del: P&L
- Reklassificeres fra OCI til P&L når hedged item påvirker P&L

---

## 10. Reklassifikation

### 4.4.1 — Reklassifikation af aktiver
Kun ved ændring i forretningsmodel (sjældent). Prospektiv effekt.

### 5.6.1-5.6.7 — Reklassifikationseffekter
- Amortiseret kostpris → FVTPL: FV-justering i P&L
- FVTPL → Amortiseret kostpris: FV på reklassifikationsdagen = ny bogført værdi
- FVOCI → FVTPL: Kumulativ OCI reklassificeres til P&L
- FVOCI → Amortiseret kostpris: OCI fjernes mod bogført værdi

---

## 11. Matched funding og realkreditspecifik

Se separate reference-filer:
- `references/lbk1541-realkreditloven.md` — LBK 1541 (matchfunding-def., § 20 koncernintern funding, balanceprincip, refinansiering, lånegrænser, obligationstyper, koncernintern realkreditstruktur, kursskæring vs. kursregulering)
- `references/bek1425-balanceprincip.md` — BEK 1425 (overordnet vs. specifikt balanceprincip, risikogrænser, konverteringsret, forhåndsemission)

Nøgleregel for bogføring: Under matched funding (specifikt balanceprincip, BEK 1425 kap. 3) netter al kursregulering til 0 i P&L. Eneste permanente P&L = kursskæring (B5.1.2A). Under overordnet balanceprincip (BEK 1425 kap. 2) kan residuale betalingsforskelle give P&L-volatilitet.

Koncerninternt forhold mellem to realkreditinstitutter reguleres af LBK 1541 § 20, stk. 3 — ALDRIG FIL § 16b.
