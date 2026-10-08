# Process and AI Log

Denne loggen dokumenterer utviklingsprosessen for Career Transition Assistant, inkludert viktige beslutninger, bruk av KI-verktøy, iterasjoner, problemer og kvalitetssikring.

## 10.09.2026 – Oppstart og Product Brief

### Arbeid utført
- Valgte prosjektidéen Career Transition Assistant.
- Avgrenset første versjon til en KI-basert jobbsøknadsassistent.
- Utarbeidet og pushet `product-brief.md` til GitHub.
- Installerte og verifiserte nødvendig verktøykjede:
  - VS Code
  - Git og GitHub
  - Node.js og NPM
  - Python 3.12 via uv
  - Docker Desktop og WSL 2
  - Claude Code

### KI-bruk
ChatGPT ble brukt til idéutvikling, avgrensning av scope, formulering av Product Brief og veiledning i teknisk oppsett. Claude Code ble installert og testet med en enkel prøvefil.

### Viktige beslutninger
- Prosjektet skal være realistisk for én student.
- Første versjon skal fokusere på én konkret stillingsannonse om gangen.
- Automatisk jobbsøk, automatisk innsending og avansert ATS ble plassert utenfor v1.
- Appen skal ikke finne på kvalifikasjoner eller erfaringer.

## 08.10.2026 – Revisjon etter tilbakemelding og PRD

### Arbeid utført
- Reviderte `product-brief.md` etter faglig tilbakemelding.
- Snevrerte inn primærbrukeren til studenter i avsluttende fase av bachelor- eller masterstudium som søker sin første faste jobb.
- Endret v1 slik at CV og stillingsannonse limes inn som tekst.
- Flyttet PDF/Word-opplasting og støttedokumentasjon ut av v1.
- Bestemte at v1 ikke skal ha innlogging eller permanent lagring.
- La til demomodus slik at sensor kan teste løsningen uten egen API-nøkkel.
- La til `Technical Assumptions`.
- Opprettet og pushet `prd.md` med:
  - product overview
  - product goals
  - out of scope
  - user flow
  - functional requirements
  - non-functional requirements
  - acceptance criteria og testing
  - open decisions

### KI-bruk
ChatGPT ble brukt som sparringspartner til å tolke tilbakemeldingen, foreslå konkrete endringer og formulere PRD-krav. Forslagene ble gjennomgått og justert før de ble lagt inn i repoet.

### Viktige beslutninger
- Demomodus skal være del av v1.
- API-nøkkel skal lagres lokalt i `.env` og aldri pushes til GitHub.
- Endelig valg av språkmodell/API tas i arkitekturfasen.
- KI-kvalitet skal vurderes mot faste, fiktive testsett.
- Prosessen skal dokumenteres løpende med små commits, prompts og beslutninger.