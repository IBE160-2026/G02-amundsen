# Vercel-publisering: fase 1 (oppsett)

## 2026-11-05 kl. 16:26 — Sondre Tveit Amundsen

### Oppgave
Etter at en publiseringsplan ble lagt fram og godkjent (Vercel Services valgt som arkitektur – ett Vercel-prosjekt for frontend og backend), gjennomføre første fase av det konkrete oppsettet: opprette `vercel.json` med frontend/backend som Services, rute `/api/*` til FastAPI og resten til React/Vite, tilpasse frontend til å bruke relativ adresse i produksjon (men fortsatt fungere lokalt), gjøre nødvendig opprydding i `backend/pyproject.toml`, oppdatere `README.md`/`architecture.md`/`process-log.md`, og kjøre tester/lint/bygg – uten å opprette noe Vercel-prosjekt, uten hemmeligheter, uten ekte API-kall, og uten commit/push.

### Plan
- Hentet og verifiserte gjeldende offisiell Vercel-dokumentasjon (`/docs/services`, `/docs/services/routing`, `/docs/services/config-reference`) for det nøyaktige `vercel.json`-skjemaet for Services, i stedet for å basere konfigurasjonen på antatt/eldre kunnskap – viktig siden Services er en relativt ny (beta) funksjon.
- Opprettet `vercel.json` i repo-roten: `services.frontend.root="frontend/"`, `services.backend.root="backend/"` med `entrypoint: "app.main:app"` (matcher eksisterende `backend/app/main.py` uten restrukturering), og to rewrites (`/api/(.*)` → backend, `/(.*)` → frontend).
- Endret `frontend/src/api/analyzeApi.js` slik at backend-adressen velges automatisk via `import.meta.env.DEV` (lokalt: `http://127.0.0.1:8000`, produksjon: relativ adresse) i stedet for å kreve en manuelt satt miljøvariabel i Vercel – reduserer risikoen for en brutt produksjonsapplikasjon pga. en glemt/feilsatt innstilling.
- Fjernet den ubrukte `[project.scripts] backend = "backend:main"`-resten fra `uv init` i `backend/pyproject.toml` (lenge kjent, ubrukt teknisk skyld – se tidligere økters `issues.md`-punkt), og bekreftet med `uv sync` + full testkjøring at dette ikke påvirker noe.
- Skrev nye tester for den DEV-avhengige adresselogikken. Et første forsøk på å simulere produksjonsmodus ved å stubbe `import.meta.env.DEV`/`PROD` i Vitest fungerte IKKE som forventet (testen beholdt localhost-adressen uansett) – undersøkte årsaken i stedet for å late som testen var riktig: Vite erstatter disse flaggene statisk ved bygging, ikke dynamisk ved kjøretid, så de kan ikke stubbes meningsfullt i en vitest-kjøring. Fjernet den upålitelige testen, og verifiserte produksjonsoppførselen empirisk i stedet: bygde frontend (`vite build`) og søkte i det ferdige JS-bygget – ingen referanse til `127.0.0.1:8000` finnes, mens den relative adressen `/api/analyze/demo` gjør.
- Oppdaterte `architecture.md` (ny seksjon 10 "Deployment (Vercel)": Services-arkitektur, adressevalg, miljøvariabler, forsvar mot kredittmisbruk; `vercel.json` lagt til i filstruktur-oversikten) og `README.md` (rettet to utdaterte linjer om at normalmodus ikke var koblet til frontend – det ble gjort i en tidligere økt; ny seksjon "Publisering på Vercel" med en nummerert sjekkliste for manuelle Vercel-steg).
- Oppdaterte `process-log.md` med en ny, egen seksjon om denne fasen.

### Resultat
Nye filer:
- `vercel.json` (repo-rot).

Endrede filer:
- `frontend/src/api/analyzeApi.js` – DEV-avhengig adressevalg.
- `frontend/src/api/analyzeApi.test.js` – nye/justerte tester for adressevalget.
- `backend/pyproject.toml` – fjernet ubrukt `[project.scripts]`-oppføring.
- `architecture.md`, `README.md`, `process-log.md` – dokumentasjon av publiseringsoppsettet.

Testresultat:
- Backend: `uv run pytest -q` → **77 passed, 0 failed** (uendret).
- Frontend: `npx vitest run` → **23 passed, 0 failed** (opp fra 21).
- `npx eslint .` → ingen feil. `npx vite build` → bygget uten feil, og inspisert direkte for å bekrefte riktig adressevalg.

Ingen Vercel-prosjekt er opprettet, ingen hemmeligheter er lagt inn noe sted, og ingen ekte OpenAI-kall er gjort. Ingen git-commit/push av kodeendringene er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Manuelt i Vercel (ikke gjort av Claude Code, per instruks): opprette prosjektet, sette `OPENAI_API_KEY` for Production-miljøet, sette et forbrukstak hos OpenAI, og gjennomføre første publisering.
- `vercel.json`/entrypoint-oppsettet er verifisert mot dokumentasjonen og mot et lokalt produksjonsbygg, men er ikke testet mot en ekte Vercel-publisering ennå (kan i prinsippet avdekke noe Vercel-spesifikt som ikke fanges opp lokalt, siden Services er i beta).
- Øvrige åpne punkter er uendret, se `issues.md`.
