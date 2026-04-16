---
name: ifrs9-accounting
description: >
  IFRS 9 og IFRS 13 regnskabsmæssig bogføring med T-konti og HTML-visualisering,
  inkl. dansk realkreditregulering (LBK 1541, BEK 1425, BEK 658). Brug denne skill
  når brugeren beskriver et finansielt flow (udlån, obligationer, kursregulering,
  afdrag, indfrielse, hedging, amortiseret kostpris, FVTPL, FVOCI, impairment, ECL,
  kursskæring, matched funding, reklassifikation, koncernintern funding,
  balanceprincippet, fair value measurement, Level 1/2/3, exit price, SDO, SDRO,
  RO) og ønsker bogføring med T-konti. Trigger også ved:
  "bogfør dette", "vis T-konti", "IFRS 9", "IFRS 13", "fair value hierarki",
  "kursregulering", "LBK 1541", "matchfunding", "balanceprincippet",
  "regnskabsbekendtgørelsen", "kontoramme", "bilag 3", "bilag 4",
  "post 8 kursreguleringer", eller ethvert scenarie med finansielle instrumenter
  og regnskab. Brug skillen selv uden eksplicit IFRS-nævnelse.
---

# IFRS 9 Accounting — T-konti og bogføring

## Formål

Denne skill tager en beskrivelse af et finansielt flow og producerer:
1. En præcis IFRS 9-baseret bogføringsanalyse med paragrafhenvisninger
2. T-konti i HTML-format der viser posteringerne dag for dag
3. Netting-oversigter og saldiafstemning
4. Formler hvor relevant
5. En opsummering med konklusion

## Arbejdsgang

### 0. Projekt-kontekst: er du i et projekt?

Skillen bruges både i almindelige chats og inden i Claude Projects (fx et realkredit-projekt med yderligere kontekst om kapitalcentre, specifikke instrumenter, eller interne konventioner). Tjek kort om du er inde i et projekt:

- Hvis der er `<project_context>`, projekt-instruktioner, eller projekt-knowledge i konteksten, så læs og respekter den før du starter scenariet. Projekt-konventioner har forrang over generiske eksempler (fx navngivning af kapitalcentre, specifik kontoramme-mapping, balanceprincip-valg per serie).
- Hvis projektet har specifikke data (fondskoder, serier, posteringsstruktur), brug dem som udgangspunkt for scenariet i stedet for illustrative tal.
- Hvis du er usikker på om du er i et projekt, men brugeren refererer til "vores obligationer", "vores serier", eller lignende ejeform, så er det et signal om projekt-kontekst.

Er du ikke i et projekt, fortsæt normalt.

### 1. Forstå flowet — og interview brugeren ved manglende data

Når brugeren beskriver et finansielt flow:
- Identificer instrumenttypen (udlån, obligation, derivat, etc.)
- Bestem IFRS 9-klassifikationen (FVTPL, FVOCI, amortiseret kostpris)
- Identificer alle hændelser i tidsrækkefølge (oprettelse, kursregulering, afdrag, indfrielse, impairment, etc.)

**Tjek om scenariet er komplet.** For at producere korrekte T-konti skal du som minimum have:
- Nominelt beløb (eller hovedstol)
- Kurs ved oprettelse (udbetalingskurs og/eller mid-kurs)
- IFRS 9-klassifikation (eller nok kontekst til at udlede den)
- Hændelser med tilhørende kurser/beløb/datoer

**Hvis noget mangler: spørg brugeren.** Antag aldrig kurser, nomineller eller klassifikation. Det er bedre at stille ét præcist spørgsmål end at producere T-konti med forkerte tal. Formuler spørgsmålet konkret, f.eks.: "Hvad er mid-kurs på dag 2?" eller "Er obligationen FVTPL-designeret eller amortiseret kostpris?"

Undtagelse: Hvis brugeren eksplicit beder om et illustrativt eksempel ("vis mig et eksempel på X"), kan du selv konstruere realistiske tal — men marker tydeligt i outputtet at tallene er illustrative.

### 2. Hent IFRS 9-grundlaget og reguleringsgrundlaget

Før du skriver output, læs den relevante IFRS 9-reference:

```
view /path/to/skill/references/ifrs9-key-paragraphs.md
```

Brug altid præcise paragrafhenvisninger (f.eks. B5.1.2A, 5.7.1, 4.1.2, 5.5.1). Gæt aldrig — slå op.

**IFRS 13-lag (fair value measurement):** Når scenariet involverer fair value-måling — dvs. altid ved FVTPL/FVOCI, alle derivater, kursskæring, og spørgsmål om Level 1/2/3, mid-kurs, bid-ask, exit price, principal market, eller CVA/DVA — læs IFRS 13-referencen:

```
view /path/to/skill/references/ifrs13-fair-value.md
```

IFRS 13 er det metodiske grundlag for *hvordan* fair value måles, hvor IFRS 9 definerer *hvornår* fair value skal anvendes. Angiv IFRS 13-paragrafreferencer (fx 9, 57, 70, 72, 93) når fair value-målingens metode er relevant for bogføringen — fx ved kursskæring (IFRS 13 par. 59-60 + B5.1.2A), mid-kurs-konvention (par. 71), eller fair value hierarchy-klassifikation.

**LBK 1541-lag:** For realkreditscenarier (matched funding, koncernintern funding, obligationsudstedelse, refinansiering, lånegrænser) læs det reguleringsmæssige grundlag:

```
view /path/to/skill/references/lbk1541-realkreditloven.md
```

Angiv altid LBK 1541 § X i principle-boxen når et realkreditregulatorisk princip er relevant for bogføringen.

**BEK 1425-lag:** For scenarier der involverer balanceprincippet, risikogrænser, konverteringsret, forhåndsemission, blokemission, eller hvor kvaliteten af matched funding-nettingen er relevant, læs også:

```
view /path/to/skill/references/bek1425-balanceprincip.md
```

BEK 1425 ("Obligationsbekendtgørelsen") definerer det specifikke og det overordnede balanceprincip. Valget af princip bestemmer, hvor tæt kursregulering netter: under det specifikke princip (kap. 3) netter det perfekt, under det overordnede princip (kap. 2) kan der være residuale betalingsforskelle. Spørg brugeren om princip-valget hvis det påvirker scenariet.

**Regnskabsbekendtgørelsen (BEK 658):** Når brugeren spørger om kontoramme, indberetning til Finanstilsynet, hvilken resultat-/balancepost en IFRS 9-postering lander i, eller mapping mellem IFRS 9 og danske regnskabskrav, læs:

```
view /path/to/skill/references/regnskabsbekendtgoerelsen.md
```

Filen indeholder bilag 3 (balance) og bilag 4 (resultatopgørelse) samt en komplet mapping-tabel fra IFRS 9-hændelser til regnskabsbekendtgørelsens poster. Brug den til at annotere T-konti-output med de korrekte postnumre (f.eks. "Post 8 — Kursreguleringer") når brugeren arbejder i dansk regnskabskontekst.

### 3. Definér principper

Start outputtet med en **principle-box** der opsummerer de 4-7 vigtigste regnskabsprincipper for det konkrete flow. Hvert princip skal:
- Være nummereret
- Referere specifik IFRS 9-paragraf i parentes
- Forklare den regnskabsmæssige konsekvens præcist

### 4. Sæt scenariet op

Definer et klart scenarie med:
- Navngivne instrumenter (A, B, C…) med farvekodede tags
- Konkrete nominelle beløb, kurser, datoer
- Alle hændelser i kronologisk orden

### 5. Byg T-konti dag for dag

**UFRAVIGELIG REGEL: Debet = Kredit i HVER postering.**
Før du skriver en journalpostering, verificer at Σ Dr = Σ Cr. Hvis de ikke balancerer, er der en fejl i din analyse — gå tilbage og find den. Skriv aldrig en ubalanceret postering til output. Dette er dobbelt bogholderi; der er ingen undtagelser.

Verifikationsrutine for hver dag/hændelse:
1. Skriv journalposteringen (Dr/Cr med beløb)
2. Summér alle debetbeløb og alle kreditbeløb
3. Bekræft at Σ Dr = Σ Cr
4. Bekræft at saldi-baren balancerer: Kasse + Aktiver − Passiver = P&L
5. Først herefter, producér HTML-outputtet for den dag

For hver dag/hændelse:
1. **Callout-boks** med journalpostering i komprimeret form (Dr/Cr)
2. **Netting-bokse** der viser symmetriske effekter (grøn = gevinst, rød = tab, grå = netto)
3. **T-konti** for alle berørte konti med:
   - Primosaldo
   - Bevægelser med forklarende noter
   - Kursreguleringer markeret med delta-farver (grøn op, rød ned)
   - Ultimosaldo med kontrolnote
4. **Saldi-bar** med afstemning: aktiver, passiver, kasse, urealiseret, realiseret, P&L, og balancetjek (✓)

### 6. Formler

Angiv formler der driver beregningerne. Brug denne notation i callouts og principle-boxes:

**Fair value ved oprettelse (B5.1.2A):**
```
Kursskæring = FV(mid) − Udbetalingskurs
```

**Kursregulering (5.7.1):**
```
ΔFV = Nominel × (Kurs_ny − Kurs_gammel) / 100
```

**Realiseret ved afdrag/indfrielse:**
```
Realiseret = Modtaget/Betalt − FV_bogført
```

**Balanceligning:**
```
Kasse + Σ Aktiver_FV − Σ Passiver_FV = Urealiseret + Realiseret = Total P&L
```

**ECL (5.5.1 / 5.5.3):**
```
ECL_12m = PD_12m × LGD × EAD    (Stage 1)
ECL_life = PD_life × LGD × EAD   (Stage 2/3)
```

### 7. Opsummering

Afslut med:
- Summary-cards med nøgletal (kursskæring, total P&L, urealiseret)
- Netting-oversigtstabel der viser alle effekter og hvordan de netter
- Konklusion i en principle-box med grøn kant

## Output-format

Output er ALTID en `.html`-fil. Aldrig markdown. Aldrig ren tekst.

### Metode: JSON → script → HTML

Byg output i to trin:

**Trin A:** Konstruér en JSON-datastruktur der beskriver hele scenariet. Se docstring i scriptet for det fulde schema:

```
view /path/to/skill/scripts/generate_tkonti.py
```

JSON-strukturen har: `title`, `subtitle`, `principles` (array af strenge), `scenario` (HTML med `<tag-a>` for loan-tags), `days` (array med callouts, netting, accounts, saldi), `summary_cards`, `netting_table`, `conclusion`.

I account rows: brug `<delta>text</delta>` for grøn kursændring, `<delta-neg>text</delta-neg>` for rød, `<note>text</note>` for noter.

**Trin B:** Kør scriptet:

```bash
python /path/to/skill/scripts/generate_tkonti.py input.json /mnt/user-data/outputs/output.html
```

Scriptet genererer komplet HTML med dark mode, alle CSS-klasser, og korrekt layout.

### Designprincipper (håndhævet af scriptet)

- Dark mode support via `prefers-color-scheme: dark` — automatisk
- Alle farver via CSS custom properties
- Fontstørrelser: h1=20px, day-title=16px, brødtekst=13px, T-konti=12px, noter=11px
- T-konti: Debet venstre, Kredit højre, total-row med border-top
- Saldi-bar: Pipe-separeret, grøn for positive tal, grå for nul
- Max-width 1300px, padding 24px
- Alle beløb formateres med punktum som tusindtalsseparator (dansk: 994.000, ikke 994,000)

### Fallback: direkte HTML

Hvis scenariet kræver layout der ikke dækkes af scriptet (specialtabeller, custom diagrammer), kan du skrive HTML direkte. Brug da `assets/style-reference.html` som CSS-reference:

```
view /path/to/skill/assets/style-reference.html
```

### Sprog

Output er på **dansk** (med engelske IFRS-termer i parentes hvor det er præciserende). Brug dansk regnskabsterminologi: posteringer, konti, kursregulering, kursskæring, afdrag, indfrielse, udstedte obligationer, urealiseret, realiseret.

## Vigtige IFRS 9-regler at huske

- **FVTPL (5.7.1):** Alle kursændringer i P&L. Ingen OCI. Ingen amortisering.
- **Kursskæring (B5.1.2A):** Forskellen mellem transaktionspris og FV ved initial recognition er day-one P&L (Level 1 instrument).
- **FVOCI gæld (5.7.7):** Own credit risk i OCI, rest i P&L.
- **Amortiseret kostpris (5.4.1):** Effektiv rente-metode. Ingen FV-regulering.
- **ECL impairment (5.5.1-5.5.20):** 3-stage model. 12-måneders ECL (Stage 1), lifetime ECL (Stage 2/3).
- **Matched funding:** Når aktiv og passiv er i samme serie, netter al kursregulering til 0. Eneste P&L = kursskæring.
- **Posteringens primat:** Posteringen er den atomare enhed. Alle afledninger (saldi, afstemninger, rapporter) følger af posteringerne.

## Vigtige IFRS 13-regler at huske (fair value measurement)

- **Exit price (par. 9):** Fair value er prisen ved salg af aktiv / overdragelse af forpligtelse — ikke entry price.
- **Principal market (par. 16-19):** Mål i principalmarkedet. For realkreditobligationer: dealer-til-dealer / børshandel, ikke retail.
- **Unit of account (par. 13-14):** Bestemmes af den IFRS, der kræver målingen — for finansielle instrumenter typisk det enkelte instrument.
- **Transaction costs (par. 25):** Indgår IKKE i fair value. Behandles efter IFRS 9 (ved FVTPL: omkostningsføres straks).
- **Day-one P&L (par. 59-60):** Afvigelse mellem transaktionspris og fair value ved initial recognition → P&L, medmindre anden IFRS specificerer andet. Dette er grundlaget for kursskæring som day-one P&L.
- **Mid-market tilladt (par. 71):** IFRS 13 udelukker ikke mid-kurs som praktisk konvention — dansk realkreditpraksis er konsistent med dette.
- **Fair value hierarchy (par. 72-90):** Level 1 (noteret pris, aktivt marked), Level 2 (observerbare inputs), Level 3 (ikke-observerbare). Måling klassificeres på laveste væsentlige inputniveau.
- **Non-performance risk (par. 42-43):** Fair value af forpligtelse inkluderer egen kreditrisiko. For FVTPL-designerede obligationer rammer dette P&L; for FVOCI-gæld ville egen kreditrisiko skulle i OCI jf. IFRS 9.5.7.7.
- **Offsetting exception (par. 48):** Net exposure-måling tilladt ved dokumenteret porteføljestyring af markedsrisiko eller modpartsrisiko. Relevant ved IRS-porteføljer under master netting / CSA.

## Vigtige LBK 1541-regler at huske (realkreditspecifik)

- **Matchfunding (§ 1a, nr. 1):** Lovdefineret krav om at betalingsstrømme fra låntagere forfalder FØR udbetalinger til investorer, og at modtagne beløb mindst svarer til udbetalingerne. Dette er den reguleringsmæssige forudsætning for at kursregulering netter.
- **Midlernes binding (§ 20, stk. 1):** Obligationsprovenuet kan ALENE anvendes til udlån mod pant i fast ejendom eller offentlig myndighed. Begræns scenarier til dette.
- **Koncernintern funding (§ 20, stk. 3):** Strukturen hvor ét realkreditinstitut udsteder obligationer til finansiering af et andet koncernforbundet realkreditinstituts udlån. Obligationer overdrages til eje og sælges til ikke-koncernforbundne aftagere.
- **IKKE FIL § 16b:** Koncerninternt forhold mellem to realkreditinstitutter reguleres af § 20, stk. 3 — ALDRIG FIL § 16b (som kun gælder pengeinstitut → realkreditinstitut).
- **Balanceprincippet (§ 18a):** Alle betalingsforpligtelser vedrørende RO skal dækkes af betalingskrav fra dækkende aktiver i serien. Forudsætning for netting.
- **Refinansiering (§ 6):** RTL-lån: renteloft +5pp, tvungen 12-måneders forlængelse ved manglende refinansiering. Refinansiering udløser derecognition/initial recognition under IFRS 9.
- **Obligationstyper:** RO (§ 18), SDRO (§ 33a), SDO (§ 33b). Alle kan FVTPL-designeres under IFRS 9 4.2.2(b).

## Vigtige BEK 1425-regler at huske (balanceprincip)

- **Valg af princip (§ 2):** Overordnet (kap. 2) eller specifikt (kap. 3), vælges per serie/register/kapitalcenter.
- **Specifikt princip (kap. 3):** Klassisk 1:1-match, konverterbar-til-konverterbar, ingen konverteringsrisiko tilladt (§ 20). Kursregulering netter perfekt under IFRS 9.
- **Overordnet princip (kap. 2):** Stresstestbaseret, tillader betalingsforskelle inden for risikogrænser. Kursregulering netter IKKE nødvendigvis perfekt — residual P&L mulig.
- **Risikogrænser:** Renterisiko ≤ 1% basiskapital (specifikt), fondsbeholdning ≤ 8% basiskapital (begge principper), valutakursrisiko ≤ 0,1% basiskapital.
- **Forhåndsemission/blokemission (§ 14/§ 21):** Skaber midlertidige betalingsforskelle (præemissionsmidler) der skal bogføres.

## Hvad denne skill IKKE gør

- Giver ikke juridisk eller skattemæssig rådgivning
- Dækker ikke IAS 39 (forgængeren) medmindre eksplicit bedt
- Producerer ikke regneark — kun HTML med T-konti
- LBK 1541-referencerne bruges udelukkende til at understøtte korrekt IFRS 9-bogføring i realkreditkontekst — skillen giver ikke regulatorisk rådgivning om compliance med balanceprincippet, lånegrænser eller Finanstilsynets krav

## Licens

Denne skill er udgivet under **PolyForm Noncommercial License 1.0.0**. Fri brug til ikke-kommercielle formål, herunder personlig brug, forskning, undervisning, og brug af nonprofitorganisationer, uddannelsesinstitutioner, offentlige forskningsorganisationer og myndigheder. Se `LICENSE` for de fulde vilkår.

Kommerciel brug kræver separat licens. Kontakt forfatteren for kommerciel licensering.

Copyright 2026 Asbjørn (https://linkedin.com/in/asbjorn)

