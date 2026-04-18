---
name: ifrs-realkreditregnskab
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
  Kilderettigheder: IFRS 9/13-referencer baseret på EU 2023/1803 (EUR-Lex), tilladt i EEA.
---

# IFRS 9 Accounting — T-konti og bogføring

## Formål

Denne skill tager en beskrivelse af et finansielt flow og producerer:
1. En præcis IFRS 9-baseret bogføringsanalyse med paragrafhenvisninger
2. T-konti i HTML-format der viser posteringerne dag for dag
3. Netting-oversigter og saldiafstemning
4. Formler hvor relevant
5. En opsummering med konklusion

## Anbefalet model

Skillen kører på alle Claude-modeller. Valg efter scenarie-type:

- **Haiku 4.5** — simple standardscenarier: enkelt FVTPL-udlån, basis kursskæring, standard kursregulering, hvor klassifikation er givet. Hurtig og billig, stadig korrekt.
- **Sonnet 4.6** — default til rutine-realkreditbogføring: matched funding, koncernintern §20, derivater med klar klassifikation, balanceprincip-spørgsmål, dansk kontoramme-mapping.
- **Opus 4.7** — kun ved reel kompleksitet: hedge accounting-valg, reklassifikation, strukturerede produkter, flertrinsscenarier med usikker klassifikation, eller når skillen selv skal revideres og forbedres.

De fleste af dine scenarier ligger i Sonnet-kategorien. Skift til Opus når du mærker at klassifikationen ikke er oplagt eller scenariet har flere sammenvævede juridiske lag.

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

### 2. Hent KUN den relevante reference (on-demand)

For at holde konteksten fokuseret, læs KUN de reference-filer der matcher scenariet. Brug nedenstående lookup-tabel.

**Reference-filernes roller:**

| Fil | Indhold | Læs når |
|---|---|---|
| `references/ifrs9-key-paragraphs.md` | IFRS 9-paragraffer (klassifikation, måling, ECL, hedge, derecognition) — EU-adopteret tekst, EU 2023/1803 | Altid (grundlag) |
| `references/ifrs13-fair-value.md` | Fair value-måling, Level 1/2/3, exit price, day-one P&L — EU-adopteret tekst, EU 2023/1803 | FVTPL/FVOCI, derivater, kursskæring, mid-kurs, hierarchy-spørgsmål |
| `references/lbk1541-realkreditloven.md` | Realkreditloven (§20, matchfunding, §15, refinansiering) | Realkreditscenarier, koncernintern funding, obligationstyper |
| `references/bek1425-balanceprincip.md` | Overordnet vs. specifikt balanceprincip, risikogrænser | Når princip-valget eller netting-kvaliteten er relevant |
| `references/regnskabsbekendtgoerelsen.md` | BEK 658 kontoramme, bilag 3/4, posteringsmapping | Dansk regnskabskontekst, postnumre, indberetning |
| `scripts/generate_tkonti.py` | JSON-schema og rendering-logik | Når du skriver JSON (læs kun docstring, linje 1-80) |
| `assets/tkonti.css` | CSS-definitioner for T-konti rendering | Kun ved fallback direkte HTML (sjældent) |

**Scenarie → minimum læse-set:**

- **Simpelt FVTPL udlån/obligation uden realkredit**: `ifrs9-key` + `script` (docstring).
- **Derivat (IRS, FRA, option)**: `ifrs9-key` (sektion 4 + 9) + `ifrs13-fair-value` (sektion 1, 8) + `script`.
- **Matched funding / kursskæring**: `ifrs9-key` (sektion 3, 4, 11) + `ifrs13-fair-value` (sektion 6, 13) + `lbk1541` (sektion 1-2) + `script`.
- **Koncernintern realkreditstruktur (§20)**: Tilføj `lbk1541` (sektion 9).
- **Balanceprincip-spørgsmål**: Tilføj `bek1425`.
- **Dansk kontoramme / post-mapping**: Tilføj `regnskabsbekendtgoerelsen` (specielt sektionen om bilag 3/4).
- **Impairment / ECL**: `ifrs9-key` (sektion 7) + `script`.
- **Hedge accounting**: `ifrs9-key` (sektion 9).

**Læs kun de nødvendige sektioner.** Hver reference-fil har en indholdsfortegnelse med sektionsnumre. Når du ved hvilken sektion du skal bruge, anvend `view_range` til at læse netop den sektion i stedet for hele filen. Eksempel: hvis scenariet kun involverer ECL, læs `ifrs9-key-paragraphs.md` sektion 7 med view_range, ikke hele filen.

**Paragrafpræcision:** Brug altid præcise henvisninger (fx IFRS 9 B5.1.2A, 5.7.1, 4.1.2, 5.5.1; IFRS 13 par. 9, 71, 72; LBK 1541 § 20, stk. 3). Gæt aldrig — slå op.

**Forrang ved konflikt:** Hvis projekt-kontekst fra trin 0 konflikter med reference-filerne (fx specifik intern praksis vs. generel anbefaling), følg projekt-konteksten og noter diskrepansen kort.

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

### 8. Juridisk ramme (OBLIGATORISK sidst i HTML)

Hver output **skal** afslutte med en "Juridisk ramme"-sektion der lister præcis hvilke regler og paragraffer der er anvendt i bogføringen. Dette gør det muligt for brugeren at efterprøve grundlaget og genfinde kilderne ved revision eller dialog med revisor.

Sektionen er struktureret som kilde → paragraffer. Typiske kilder:

- **IFRS 9** — klassifikation, måling, impairment, hedge, derecognition (EU 2023/1803)
- **IFRS 13** — fair value-måling, hierarki, day-one P&L (EU 2023/1803)
- **LBK 1541** — Realkreditloven (matchfunding, § 20, refinansiering)
- **BEK 1425** — Balanceprincippet (specifikt vs. overordnet)
- **BEK 658** — Regnskabsbekendtgørelsen (dansk kontoramme, bilag 3/4)
- **CRR / CRD** — når kapitaldækning eller risikovægte er relevant
- **FIL** — Lov om finansiel virksomhed (sjældent relevant for ren realkredit-bogføring)

Hver post indeholder:
- `source`: Kortnavn på regelsættet (fx "IFRS 9", "LBK 1541")
- `full_name`: Fuldt navn (fx "IFRS 9 Financial Instruments (EU 2023/1803)")
- `paragraphs`: Liste af anvendte paragraffer med kort forklaring — hver som `{"ref": "B5.1.2A", "note": "Day-one P&L ved Level 1-instrument"}`

Yderligere, efter hovedlisten, tilføj (når relevant):
- **Fortolkningsvalg:** Korte noter om hvor scenariet har haft flere mulige behandlinger og hvad der blev valgt. Kan være tom liste hvis ikke relevant.
- **Ikke anvendt:** Regler der kunne have været relevante i beslægtede scenarier men IKKE er anvendt her. Hjælper med at afgrænse scopet.

**Sprogregel:** Paragrafhenvisninger skal være præcise (fx "IFRS 9 B5.1.2A", ikke "IFRS 9 kap. 5"). Gæt aldrig — slå op hvis usikker.

**Placeringsregel:** Den juridiske ramme står **altid sidst** i HTML'en, efter konklusionen. Dette er fast layout.

## Output-format

Output er ALTID en `.html`-fil. Aldrig markdown. Aldrig ren tekst.

### Metode: JSON → validator → script → HTML

Byg output i tre trin:

**Trin A:** Konstruér en JSON-datastruktur der beskriver hele scenariet. Se det fulde schema i docstringen øverst i scriptet (læs kun linje 1-100 med view_range):

```
view /path/to/skill/scripts/generate_tkonti.py (view_range [1, 100])
```

**JSON-schema v2 (stramt typed format):**

Top-level: `title` (required), `subtitle`, `principles` (array), `scenario` (str), `days` (array, required), `summary_cards`, `netting_table`, `conclusion`, `legal_framework` (required, se trin 8).

Hver `day` har: `title` (required), `callouts`, `netting`, `accounts` (required), `saldi`.

**`legal_framework` (obligatorisk):**

```json
{
  "sources": [
    {
      "source": "IFRS 9",
      "full_name": "IFRS 9 Financial Instruments (EU 2023/1803)",
      "paragraphs": [
        {"ref": "B5.1.2A", "note": "Day-one P&L ved Level 1-instrument"},
        {"ref": "5.7.1", "note": "FVTPL: alle kursændringer i P&L"}
      ]
    },
    {
      "source": "LBK 1541",
      "full_name": "Realkreditloven (konsolideret)",
      "paragraphs": [
        {"ref": "§ 1a, nr. 1", "note": "Matchfunding-definition"}
      ]
    }
  ],
  "interpretive_choices": [
    "FKA bogført on-balance som FVTPL-aktiv, ikke off-balance tilsagn."
  ],
  "not_applied": [
    {"source": "FIL § 16b", "note": "Gælder kun pengeinstitut→realkreditinstitut; ikke relevant her."}
  ]
}
```

`interpretive_choices` og `not_applied` er valgfri men anbefales hvor det skærper scopet.

**Rows i accounts har præcis tre former — vælg én:**

```json
{"text": "Oprettelse", "debet": 994000}        // Posting: debet
{"text": "Udbetaling", "kredit": 989000}       // Posting: kredit
{"total": true, "saldo": 994000, "side": "debet"}   // Total-row (saldo på debet- eller kredit-side)
```

**Vigtigt: beløb er ALTID tal, aldrig strings.** Skriv `994000`, ikke `"994.000"` eller `"Oprettelse 994.000"`. Scriptet formaterer selv til dansk tusindtalsseparator (`994.000`), typografisk minus (`−21.500`), og farver negative tal røde, positive grønne.

En posting-row har præcis én af `debet` eller `kredit`, aldrig begge. Text er valgfri men anbefalet (fx "Oprettelse", "Afdrag", "Kursregulering").

**Netting-items har to former:**

```json
{"label": "ΔFV udlån", "amount": -21500}      // Typed: farve fra fortegn
{"color": "green", "html": "<strong>Text</strong>"}    // Free-form: tekst uden tal
```

**Saldi-bar:** `{"label": "Udlån", "value": 994000}` for tal (formateres + farves), eller `{"label": "Bal", "value": "✓"}` for strings.

**Summary_cards og netting_table:** tal-celler formateres og farves automatisk; strings bruges uændret (fx `""` for tomme celler).

**Markup-tokens i strings:** `<tag-a>X</tag-a>` (blå låne-tag), `<tag-b>X</tag-b>` (lilla), `<strong>X</strong>` (fed), `<note>X</note>` (lille grå). Brug IKKE `<delta>` eller `<delta-neg>` længere — farver afledes af tal-fortegn automatisk.

**Trin B:** Validér JSON'en FØR du genererer HTML. Validatoren checker balance-ligning eksakt (Σ debet − Σ kredit = deklareret saldo × retning), typer, og alle tokens:

```bash
python /path/to/skill/scripts/validate_scenario.py input.json
```

Exit 0 = OK. Exit 1 = fejl der skal rettes. Balance-fejl på konti er altid blokerende (modsat v1 hvor de var advarsler), fordi vi nu har eksakte tal. Ret alle fejl før du fortsætter.

**Trin C:** Kør scriptet:

```bash
python /path/to/skill/scripts/generate_tkonti.py input.json /mnt/user-data/outputs/output.html
```

Scriptet genererer komplet HTML med dark mode, alle CSS-klasser, korrekt layout, og alle beløb formateret dansk.

### Designprincipper (håndhævet af scriptet)

- Dark mode support via `prefers-color-scheme: dark` — automatisk
- Alle farver via CSS custom properties
- Fontstørrelser: h1=20px, day-title=16px, brødtekst=13px, T-konti=12px, noter=11px
- T-konti: Debet venstre, Kredit højre, total-row med border-top
- Saldi-bar: Pipe-separeret, grøn for positive tal, grå for nul
- Max-width 1300px, padding 24px
- Alle beløb formateres med punktum som tusindtalsseparator (dansk: 994.000, ikke 994,000)

### Fallback: direkte HTML

Hvis scenariet kræver layout der ikke dækkes af scriptet (specialtabeller, custom diagrammer), kan du skrive HTML direkte. Indlejr `assets/tkonti.css` inline i `<style>`-tagget for at bevare konsistent styling:

```
view /path/to/skill/assets/tkonti.css
```

CSS'en er den samme som scriptet bruger, så output'et vil være visuelt konsistent med de scriptgenererede T-konti.

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

## Kilderettigheder

IFRS 9- og IFRS 13-referencerne i denne skill er baseret på **Commission Regulation (EU) 2023/1803** (konsolideret tekst, gældende fra 16. oktober 2023), som er offentligt tilgængelig EU-forordningstekst fra EUR-Lex. Reproduktion er tilladt inden for EEA. Kilden er ikke IASB-originalteksten fra ifrs.org.

De danske referencefiler (BEK 658, BEK 1425, LBK 1541) er hentet fra retsinformation.dk og er fri dansk lovgivning.

## Licens

Denne skill er udgivet under **PolyForm Noncommercial License 1.0.0**. Fri brug til ikke-kommercielle formål, herunder personlig brug, forskning, undervisning, og brug af nonprofitorganisationer, uddannelsesinstitutioner, offentlige forskningsorganisationer og myndigheder. Se `LICENSE` for de fulde vilkår.

Kommerciel brug kræver separat licens. Kontakt forfatteren for kommerciel licensering.

Copyright 2026 Asbjørn (https://linkedin.com/in/asbjorn)
Skill: ifrs-realkreditregnskab (tidligere: ifrs9-accounting)

