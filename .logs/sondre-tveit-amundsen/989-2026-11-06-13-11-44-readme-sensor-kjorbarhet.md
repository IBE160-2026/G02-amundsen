# README: sensor-kjørbarhet og dokumentasjonsoversikt

## 2026-11-06 kl. 13:11 — Sondre Tveit Amundsen

### Oppgave
Oppfølging av IBE160-sluttkontrollen (muntlig/chat-audit, ingen filer endret den gangen): forbedre `README.md` slik at en sensor kan klone repoet og kjøre applikasjonen på en ren maskin. Konkret: dokumentere forutsetninger (Python 3.12, uv, Node.js/npm), bekrefte korrekte install-/oppstartskommandoer, tydeliggjøre demomodus (ingen nøkkel/kostnad) og normalmodus (egen nøkkel) lokalt, dokumentere testkommandoer, bekrefte at Vercel-lenke/produksjonsstatus er korrekt, rette `issues.md`-referansen til riktig sti under `.logs/`, og sørge for at README peker til Product Brief, PRD, arkitektur, epics/stories, prosesslogg og den manuelle KI-testdokumentasjonen. Kun nødvendige endringer i README; ingen kodeendring.

### Plan
- Leste gjeldende `README.md` i full og identifiserte konkrete mangler fra sluttkontrollen: ingen forutsetninger nevnt, `issues.md` referert uten sti, `product-brief.md`/`process-log.md`/manuell-QA-mappen ikke lenket.
- Sjekket faktiske versjonskrav i stedet for å gjette: `backend/.python-version`/`pyproject.toml` (`>=3.12`), `npm view vite@8.3.0 engines` (`^20.19.0 || >=22.12.0`), ingen `engines`-felt i `frontend/package.json`, ingen pinnet uv-versjon. Noterte de faktisk installerte versjonene i dette miljøet (Python 3.12, uv 0.12.7, Node v26.7.0, npm 11.19.0) som en "testet med"-referanse.
- Bekreftet at `git remote -v` faktisk peker til `https://github.com/IBE160-2026/G02-amundsen.git` før jeg la inn en `git clone`-kommando i README.
- Skrev om README: ny "Dokumentasjon"-tabell (lenker til alle plandokumenter, prosesslogg, `backend/test-data/manual-qa/` og riktig `.logs/sondre-tveit-amundsen/issues.md`-sti), ny "Forutsetninger"-seksjon, et eksplisitt `git clone`-steg, og delte det gamle punkt 3 ("demo- eller normalmodus") i to tydelige, separate punkter (3: demomodus uten nøkkel, 4: normalmodus med egen nøkkel) for å gjøre NFR6-kravet synlig. Vercel-seksjonen er i hovedsak uendret (allerede korrekt fra forrige økt), men `issues.md`-referansen der er også rettet til full sti.
- Verifiserte at ALLE filer/mapper README nå lenker til faktisk eksisterer (`test -e` på hver av dem).
- Gjorde en reell smoke-test av de dokumenterte kommandoene (ikke bare lest dem): `uv sync` + `uv run uvicorn ...` → `GET /` og `GET /api/analyze/demo` ga begge 200; `uv run pytest` → 81/81; `npm test` → 23/23. Ingen ekte OpenAI-kall.
- Kontrollerte med `git status` at kun `README.md` ble endret.

### Resultat
Endret fil: `README.md` (ny «Dokumentasjon»-tabell og «Forutsetninger»-seksjon, utvidet/korrigert «Kjøre applikasjonen lokalt», rettet `issues.md`-sti i Vercel-seksjonen). Ingen annen fil er rørt.

Alle dokumenterte kommandoer er faktisk kjørt og bekreftet å fungere i denne økten (ikke bare antatt korrekte fra tidligere økter): backend-oppstart + demomodus (200/200), `uv run pytest` (81/81), `npm test` (23/23).

Ingen applikasjonskode, API-nøkler eller Vercel-konfigurasjon er endret. Ingen ekte eller betalte API-kall. Ingen git-commit/push av `README.md` er gjort av meg (på brukerens eksplisitte instruks – dette gjør brukeren selv) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Jeg har IKKE kjørt `npm install`/`npm run dev` på nytt denne økten (frontend-oppsettet er uendret og allerede verifisert fungerende i tidligere økter) – dersom frontend-avhengigheter endres senere, bør dette re-verifiseres.
- Jeg har ikke testet README-instruksjonene på en faktisk "ren" maskin uten Python/uv/Node forhåndsinstallert – kun bekreftet at versjonskravene i README stemmer med det som faktisk kreves av prosjektfilene (`pyproject.toml`, Vite sitt `engines`-felt).
- Øvrige, tidligere åpne punkter (sikkerhetsrisikoen med den ikke-tilbakekalte OpenAI-nøkkelen, de mindre KI-kvalitetsfunnene fra manuell-QA-runden, m.m.) er uendret, se `issues.md`.
