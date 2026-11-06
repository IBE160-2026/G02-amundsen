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

## 2026-11-06 kl. 12:51 — Sondre Tveit Amundsen

### Oppgave
Gjennomføre selve testkjøringen fra forrige seksjon: kjøre normalmodus mot testsett 2, 3 og 4 (ikke 1, som gjenbruker eksisterende, allerede validerte demodata) med ekte OpenAI-kall gjennom den lokale backenden (`backend/.env`), sammenligne resultatene mot de låste forventningene i `forventet-resultat.md`, og dokumentere avvik ærlig – inkludert akseptabel KI-variasjon. Maks tre betalte kall uten ny godkjenning; ingen kodeendring under selve testingen.

### Plan
- Bekreftet at `backend/.env` har en konfigurert `OPENAI_API_KEY` uten å vise verdien, og at `uv run pytest` fortsatt var grønt (78/78) før noe ekte kall.
- Startet backenden lokalt på en egen port, og kjørte nøyaktig tre ekte `POST /api/analyze`-kall (ett per testsett 2–4) via et lite Python-skript som leser `cv.txt`/`stillingsannonse.txt` direkte og bygger JSON-payloaden korrekt (unngår skall-escaping-problemer med flerlinjetekst). Alle tre kall ga HTTP 200 på første forsøk – ingen retries var nødvendig.
- Lagret rå JSON-svar som `resultat-2026-11-06.json` i hvert testsetts mappe.
- Gjennomgikk hvert svar manuelt mot `forventet-resultat.md`: kontrollerte at alle krav ble identifisert, at ingen punkt på «må aldri påstås»-listen forekom i fri tekst, og at **hvert enkelt** `cv_excerpt`/`job_ad_excerpt` faktisk er et ordrett sitat fra kildetekstene (kontrollert manuelt, ikke bare stolt på backendens egen `grounding.py`).
- Skrev en kort, konkret `vurdering-2026-11-06.md` per testsett.
- Fant et konkret, bekreftet avvik i testsett 4: en vag styrke ("digitale verktøy") ble koblet via `related_requirement_ids` til det spesifikke Jira/Trello-kravet. Undersøkte årsaken i `grounding.py` sin kildekode (ikke gjettet): modellen satte `job_ad_excerpt` til nøyaktig kravets egen beskrivelsestekst, noe som gjør nøkkelord-overlapp-kontrollen i `_filter_related_requirement_ids` selvreferensiell og dermed virkningsløs for dette konkrete tilfellet.
- Oppdaterte `process-log.md` med en samlet, ærlig oppsummering av alle tre testsettene, inkludert det bekreftede avviket og et gjennomgående mønster (reelt CV-innhold som ikke alltid anerkjennes som en bekreftet styrke, sett i to av tre testsett).
- Stoppet den lokale backend-serveren igjen. Kjørte `uv run pytest` og `git diff --stat` på `backend/app`/`frontend/src`/`vercel.json` for å bekrefte at ingen applikasjonskode ble endret under testingen.

### Resultat
Nye filer (ukommittert av meg, per instruks):
- `backend/test-data/manual-qa/testsett-2-markus-eide/{resultat-2026-11-06.json, vurdering-2026-11-06.md}`
- `backend/test-data/manual-qa/testsett-3-sara-lund/{resultat-2026-11-06.json, vurdering-2026-11-06.md}`
- `backend/test-data/manual-qa/testsett-4-thomas-berg/{resultat-2026-11-06.json, vurdering-2026-11-06.md}`

Endret fil: `process-log.md` (ny seksjon, ukommittert av meg).

**Utfall:** testsett 2 – bestått med mindre avvik; testsett 3 – bestått, uten avvik av betydning; testsett 4 – avvik funnet (se over). Ingen av de tre svarene brøt noen «må aldri påstås»-liste i fri tekst; alle kildesitater i alle tre svar ble bekreftet ekte og ordrette.

Nøyaktig 3 ekte, betalte API-kall ble gjort (grensen uten ny godkjenning). Ingen applikasjonskode, modell, prompt eller forventede resultater ble endret under testingen (bekreftet med `git diff --stat`). Ingen Vercel-endring. API-nøkkelen ble ikke vist, kopiert eller logget noe sted. Ingen av testresultat-/dokumentasjonsfilene eller `process-log.md` er committet av meg (på brukerens eksplisitte instruks) – kun denne loggfilen og `issues.md` committes av `sesjonslogg`-skillen.

### Åpne punkter
- **Anbefalt kodefiks, ikke implementert:** stram inn `_filter_related_requirement_ids` i `grounding.py` slik at kravets egen `job_ad_excerpt` ikke kan "bekrefte" en krav-kobling uten at `cv_excerpt` spesifikt er relevant for kravet. Bør dekkes av en ny, målrettet regresjonstest som speiler akkurat testsett 4-tilfellet.
- Mønsteret med at reelt CV-innhold noen ganger ikke anerkjennes som en bekreftet styrke (sett i testsett 2 og 4) bør følges med på ved videre testing, men er ikke nødvendigvis en feil som skal rettes isolert.
- Testsett 1 er ikke kjørt denne runden (gjenbruker eksisterende, validert demodata – ingen ny kjøring nødvendig).
- Øvrige, tidligere åpne punkter er uendret, se `issues.md`.
