# Vercel-publisering: demodata-feil etter publisering

## 2026-11-05 kl. 16:44 — Sondre Tveit Amundsen

### Oppgave
Etter en vellykket publisering på `https://g02-amundsen.vercel.app/` (frontend lastet riktig), ga «Kjør demoanalyse» feilmeldingen "Kunne ikke laste demodata. Kontroller at test-data-filene finnes." Demomodus fungerte lokalt. Oppgaven var å undersøke hvordan backenden finner/leser demodatafilene, fastslå den konkrete årsaken (uten å gjette) før noe ble endret, rette feilen med minst mulig endring, sørge for at både lokal utvikling og Vercel fungerer, legge til tester som forebygger samme feilklasse, kjøre alle relevante tester/lint/bygg, og oppdatere `process-log.md` – uten ekte API-kall, hemmeligheter, nytt Vercel-prosjekt, eller commit/push.

### Plan
- Leste `backend/app/demo_data.py`: `TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test-data"` pekte på en `test-data/`-mappe på repo-roten, UTENFOR `backend/`.
- Bekreftet årsaken mot gjeldende Vercel-dokumentasjon (hentet via WebFetch, ikke gjettet): en Vercel Service bunter kun filer som ligger inne i tjenestens egen `root` (`backend/`, jf. `vercel.json` fra forrige fase). Sibling-mapper utenfor roten følger ikke med i produksjonsbygget og finnes ikke i funksjonens filsystem ved kjøretid.
- Vurderte alternativer (kopieringsscript i byggetrinn vs. flytte datafilene) og valgte den minste, mest direkte løsningen: flytte selve datamappen inn i `backend/`.
- Flyttet `test-data/` → `backend/test-data/` med `git mv` (bevarer filhistorikk), og endret `TEST_DATA_DIR` i `demo_data.py` til `parents[1] / "test-data"`.
- Oppdaterte `architecture.md` (prosjektstruktur-tre + en forklarende merknad i publiseringsseksjonen) og `README.md` (lenken til demodata) til den nye plasseringen.
- La til en ny, målrettet regresjonstest (`test_test_data_dir_is_inside_backend_service_root`) som kontrollerer at demodata-mappen faktisk ligger inne i `backend/` – denne ville fanget opp nøyaktig denne feilen før publisering, i motsetning til de eksisterende testene (som alltid kjører lokalt).
- Kjørte backend- og frontend-tester, ESLint, produksjonsbygg, og en lokal smoke-test av `GET /api/analyze/demo` for å bekrefte at demomodus fortsatt fungerer lokalt etter flyttingen.
- Oppdaterte `process-log.md` med feilen, årsaken, løsningen og testresultatene.

### Resultat
Endrede/flyttede filer:
- `test-data/*.txt`/`.json` → `backend/test-data/*` (flyttet med `git mv`).
- `backend/app/demo_data.py` – `TEST_DATA_DIR` peker nå på `backend/test-data/`.
- `backend/tests/test_demo_data.py` – ny regresjonstest.
- `architecture.md`, `README.md`, `process-log.md` – oppdatert til ny plassering, med begrunnelse.

Testresultat:
- Backend: `uv run pytest -q` → **78 passed, 0 failed** (opp fra 77).
- Frontend: `npx vitest run` → **23 passed, 0 failed** (uendret).
- `npx eslint .` → ingen feil. `npx vite build` → bygget uten feil.
- Manuell lokal smoke-test: `GET /api/analyze/demo` svarte korrekt med den fiktive CV-en fra den nye plasseringen.

Ingen ekte OpenAI-kall, ingen hemmeligheter, ingen nytt Vercel-prosjekt. Ingen git-commit/push av kodeendringene er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Fiksen er verifisert lokalt, men ikke mot en ny, ekte publisering på Vercel ennå – brukeren må publisere denne endringen til det eksisterende prosjektet og bekrefte at demomodus fungerer i produksjon.
- Øvrige åpne punkter er uendret, se `issues.md`.
