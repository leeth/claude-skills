# claude-skills

Her deler jeg mine Claude Code skills — specialiserede kommandoer og værktøjer til brug med Claude Code CLI.

## Skills

### [ifrs-realkreditregnskab](./ifrs-realkreditregnskab/)

IFRS 9 og IFRS 13 regnskabsmæssig bogføring med T-konti og HTML-visualisering, inkl. dansk realkreditregulering (LBK 1541, BEK 1425, BEK 658).

**Hvad den gør:**
- Analyserer finansielle flows og producerer præcise IFRS 9-posteringer med paragrafhenvisninger
- Genererer T-konti som HTML-fil dag for dag med kursreguleringer, netting og saldiafstemning
- Dækker: FVTPL, FVOCI, amortiseret kostpris, matched funding, kursskæring, ECL/impairment, koncernintern funding (§ 20), balanceprincippet
- Mapper posteringer til dansk regnskabsbekendtgørelse (BEK 658), bilag 3 og 4

**Triggerord:** "bogfør dette", "vis T-konti", "IFRS 9", "IFRS 13", "fair value hierarki", "kursregulering", "matchfunding", "balanceprincippet", "kontoramme", "post 8 kursreguleringer"

**Anbefalet model:** Sonnet 4.6 til rutinescenarier — Opus 4.7 ved hedge accounting, reklassifikation eller flertrinsscenarier med usikker klassifikation.

**Indhold:**

| Fil | Beskrivelse |
|-----|-------------|
| `SKILL.md` | Skill-definition med arbejdsgang og regler |
| `scripts/generate_tkonti.py` | Genererer HTML-output fra JSON-scenariebeskrivelse |
| `scripts/validate_scenario.py` | Validerer scenarie-JSON inden HTML-generering |
| `assets/tkonti.css` | CSS-stylesheet til HTML-output |
| `references/ifrs9-key-paragraphs.md` | IFRS 9-nøgleparagraffer |
| `references/ifrs13-fair-value.md` | IFRS 13 fair value measurement |
| `references/lbk1541-realkreditloven.md` | LBK 1541 realkreditloven |
| `references/bek1425-balanceprincip.md` | BEK 1425 obligationsbekendtgørelsen |
| `references/regnskabsbekendtgoerelsen.md` | BEK 658 kontoramme og mapping |

## Licens

[PolyForm Noncommercial 1.0.0](./LICENSE) — fri til ikke-kommerciel brug.
