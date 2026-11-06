# Produksjonstest av normalmodus med ekte OpenAI

## 2026-11-06 kl. 11:17 — Sondre Tveit Amundsen

### Oppgave
Dokumentere en allerede gjennomført, kontrollert produksjonstest av normalmodus med ekte OpenAI på `https://g02-amundsen.vercel.app/` (06.11.2026). Brukeren hadde: redusert OpenAI sin månedlige forbruksgrense fra $100 til $3 og aktivert "Enforce a hard limit" før testen (saldo $4,98, auto-påfyll av); lagt `OPENAI_API_KEY` inn i Vercel som Secret kun for Production; publisert og testet normalmodus med en fiktiv kandidat (Emma Hansen, Fjord Analyse AS, Junior analytiker); deretter slettet `OPENAI_API_KEY` fra Vercel igjen og publisert på nytt uten nøkkelen (status Ready/Current). Den opprinnelige nøkkelen er IKKE tilbakekalt hos OpenAI – brukeren ba eksplisitt om at dette dokumenteres som en kjent, åpen sikkerhetsrisiko (eldre Vercel-deployments kan i prinsippet fortsatt ha tilgang til den). Oppgaven var ren dokumentasjon: oppdatere `process-log.md` (hendelsen, resultatene, sikkerhetstiltakene, kritisk refleksjon), `README.md` (korrekt produksjonsstatus for demo-/normalmodus), og `issues.md` (markere fullført produksjonstest, føre sikkerhetsrisikoen og de to kvalitetsbegrensningene som nye, åpne punkter) – ingen kodeendringer, ingen API-kall, ingen nye deployments.

### Plan
- Leste gjeldende `README.md`, slutten av `process-log.md` og `issues.md` for å vite nøyaktig hva som var utdatert etter denne hendelsen.
- Skrev en ny, detaljert seksjon i `process-log.md`: OpenAI-forberedelsene (saldo, forbruksgrense, hard limit), Vercel-gjennomføringen (nøkkel lagt inn → testet → nøkkel fjernet → ny publisering), et eget, tydelig avsnitt om sikkerhetsrisikoen (nøkkelen ikke tilbakekalt), det fulle testresultatet (6 krav/5 styrker/5 gap/4 forslag/søknadsutkast) og kvalitetskontrollen (inkl. de to mindre begrensningene: en språklig feil og et generelt søknadsutkast), samt en kritisk refleksjon om at det å fjerne en miljøvariabel i Vercel ikke er det samme som å trekke tilbake tilgangen til en nøkkel hos leverandøren.
- Oppdaterte `README.md` sin "Status i produksjon"-seksjon fra "normalmodus er ikke aktivert" til den mer presise, faktiske historien: normalmodus BLE testet og bekreftet fungerende i produksjon, men er bevisst deaktivert igjen etterpå – med sikkerhetsrisikoen synlig nevnt der også. Oppdaterte den tilhørende Vercel-sjekklisten til å starte med å tilbakekalle/rotere den gamle nøkkelen før en eventuell ny aktivering.
- Oppdaterte `issues.md`: markerte det tidligere åpne punktet om manglende produksjonstest av normalmodus som løst, og la til fire nye, konkrete åpne punkter (sikkerhetsrisiko, språklig feil, generelt søknadsutkast, og den utestående beslutningen om permanent aktivering).

### Resultat
Endrede filer (kun dokumentasjon):
- `process-log.md` – ny seksjon «Kontrollert produksjonstest av normalmodus med ekte OpenAI».
- `README.md` – oppdatert "Status i produksjon" og Vercel-sjekklisten.
- `.logs/sondre-tveit-amundsen/issues.md` – se Åpne punkter under.

Ingen applikasjonskode er endret. Ingen API-kall ble gjort av Claude Code. Ingen API-nøkkel er lagt inn eller eksponert av Claude Code. Ingen nye Vercel-deployments ble gjort av Claude Code. Ingen git-commit/push av `README.md`/`process-log.md` er gjort (på brukerens eksplisitte instruks – dette gjør brukeren selv) – kun denne loggfilen og `issues.md` committes av `sesjonslogg`-skillen.

### Åpne punkter
- **Sikkerhetsrisiko:** den OpenAI API-nøkkelen som ble brukt i produksjonstesten er ikke tilbakekalt/rotert hos OpenAI. Nøkkelen er fjernet fra Vercel sin nåværende konfigurasjon, men eldre Vercel-deployments kan i prinsippet fortsatt ha tilgang til den.
- Mindre kvalitetsbegrensning: en språklig feil i resultatet ("språkendelig seksjon") ble observert i denne produksjonstesten.
- Søknadsutkastet var igjen ganske generelt formulert – samme kjente begrensning som 05.11.2026, nå bekreftet også i produksjon.
- Beslutning utestående: om/når normalmodus skal aktiveres permanent i produksjon (krever at nøkkelen fra testen først tilbakekalles/roteres hos OpenAI).
- Øvrige, tidligere åpne punkter er uendret, se `issues.md`.
