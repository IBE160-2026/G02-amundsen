# Fire fiktive testsett for manuell kvalitetssikring

## 2026-11-06 kl. 12:37 — Sondre Tveit Amundsen

### Oppgave
Som oppfølging av sluttkontrollen (som fant at PRD §7 og faglærers tilbakemelding krever 3–5 fiktive testsett med forhåndsdefinerte forventninger, mens kun ett fantes): lage fire fiktive testsett (CV + stillingsannonse + forhåndsdefinert forventet resultat) som dekker god match, tydelige kompetansegap, overførbar deltidserfaring og uklare kvalifikasjoner. Brukeren godkjente et forslag presentert i en tidligere, fil-fri runde, med fire presiseringer: (1) utvid Sara Lund-CV-en og gjør den lengre/mer realistisk, (2) skill konsekvent mellom «ikke dokumentert» og «mangler ferdigheten», (3) fjern telefonnummer/kontaktopplysninger fra de nye testdataene, (4) bruk meningsbaserte forventninger (ikke eksakt ordlyd/antall). Oppgaven nå var å faktisk opprette filene, uten å gjøre noe ekte API-kall, uten å endre applikasjonskode/Vercel, og uten selv å committe testdata-/dokumentasjonsfilene.

### Plan
- Leste PRD §7, `product-brief.md`, eksisterende `backend/test-data/` og `test_grounding.py`/`test_demo_data.py` på nytt for å sikre at forslaget var tro mot kravene og ikke overlappet eksisterende tester.
- La til en dedikert mappe `backend/test-data/manual-qa/` med én undermappe per testsett, og en felles `TESTPLAN.md`.
- **Testsett 1 (Kari Nordmann, god match):** gjenbrukte eksisterende `demo-cv.txt`/`demo-job-ad.txt`/`demo-result.json` uendret, og la kun til en `README.md` i `testsett-1-kari-nordmann/` som forklarer at `demo-result.json` allerede er en gyldig, uavhengig skrevet forventning, pluss en meningsbasert sjekkliste.
- **Testsett 2 (Markus Eide, tydelige kompetansegap):** ny kandidat med bachelor i markedsføring som søker en dataanalytiker-stilling (SQL/Python/Power BI/statistikk helt fraværende i CV-en) – ingen telefon/e-post i CV-en.
- **Testsett 3 (Sara Lund, overførbar deltidserfaring):** utvidet CV-en vesentlig fra forslaget (lagt til en tredje rolle – sommerpraktikant på et fiktivt kommunalt servicekontor med et saksbehandlingssystem) for å gjøre den lengre og mer realistisk, og for å skape en bevisst, dokumentert skjønnsgråsone (saksbehandlingssystem vs. CRM-system) i stedet for et rent svart/hvitt-gap.
- **Testsett 4 (Thomas Berg, uklare kvalifikasjoner):** bevisst vag CV («digitale verktøy», ingen navngitte verktøy) mot en stillingsannonse som krever Jira/Trello/Excel – den skarpeste FR10-stresstesten av de fire.
- I alle tre nye `forventet-resultat.md`-filer: brukte konsekvent formuleringen «ikke dokumentert i CV-en» for gap (aldri «mangler ferdigheten»), skrev forventningene som meningsbaserte sjekklister (ingen krav til eksakt ordlyd/antall), og la inn en egen, tydelig markert «Må aldri påstås»-liste per testsett som er en hard grense (ikke skjønn).
- Skrev `TESTPLAN.md` med: prinsippet om at forventningene er låst 2026-11-06 før noe ekte kall, skillet «ikke dokumentert» vs. «mangler ferdigheten», meningsbaserte kriterier, en klar objektiv/skjønnsbasert todeling av hva som sjekkes, prosedyre for selve testkjøringen (inkl. at et nytt forsøk kun er akseptabelt ved teknisk feil, ikke for å få et «bedre» resultat), og hvor resultater/avvik skal dokumenteres (`process-log.md`, `issues.md`, råsvar lagret ved siden av forventningene).
- Kontrollerte med `git status`/`git diff --stat` at de tre eksisterende demo-filene er helt uendret, og at ingen applikasjonskode er rørt.

### Resultat
Nye filer (alle usporet, ikke committet av meg):
- `backend/test-data/manual-qa/TESTPLAN.md`
- `backend/test-data/manual-qa/testsett-1-kari-nordmann/README.md`
- `backend/test-data/manual-qa/testsett-2-markus-eide/{cv.txt, stillingsannonse.txt, forventet-resultat.md}`
- `backend/test-data/manual-qa/testsett-3-sara-lund/{cv.txt, stillingsannonse.txt, forventet-resultat.md}`
- `backend/test-data/manual-qa/testsett-4-thomas-berg/{cv.txt, stillingsannonse.txt, forventet-resultat.md}`

`git status --porcelain` viser kun én ny, usporet mappe (`backend/test-data/manual-qa/`); `git diff --stat` på de tre eksisterende demo-filene er tom (bekreftet uendret). Ingen applikasjonskode, Vercel- eller API-konfigurasjon er rørt. Ingen ekte eller mockede OpenAI-kall er gjort. Ingen av testdata-/dokumentasjonsfilene er committet (på brukerens eksplisitte instruks – dette gjør brukeren selv) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- De fire testsettene er ikke kjørt mot ekte OpenAI ennå – det er neste steg, og skal gjøres av brukeren (eller av meg på eksplisitt oppfordring senere), én gang per sett, med resultatene dokumentert ved siden av de nå låste forventningene.
- Øvrige åpne punkter fra sluttkontrollen (manglende forutsetninger i README, ødelagt kodeblokk i `architecture.md`, manglende wireframe, m.m.) er uendret og ikke del av denne økten.
