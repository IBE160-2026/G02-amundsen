# Vercel-publisering: dokumentasjon av fullført publisering

## 2026-11-05 kl. 16:52 — Sondre Tveit Amundsen

### Oppgave
Avslutte dagens IBE160-arbeid med å dokumentere den vellykkede publiseringen av Career Transition Assistant på `https://g02-amundsen.vercel.app/` (siste applikasjonscommit `c10c0f7`). Brukeren har manuelt bekreftet at demomodus fungerer i produksjon (demodata-feilen fra forrige fase er dermed bekreftet rettet i produksjon, ikke bare lokalt). `OPENAI_API_KEY` er bevisst IKKE lagt inn i Vercel – normalmodus er derfor ikke aktivert i produksjon, for å beskytte forhåndsbetalte OpenAI-kreditter mot en offentlig, uinnlogget side. Oppgaven var rent dokumentasjon: oppdatere `README.md` (publisert adresse, status på demo-/normalmodus, korrigere utdatert status), oppdatere `process-log.md` (publiseringen, demodata-feilen, den manuelle bekreftelsen, kredittbeskyttelsen, og en kort kritisk refleksjon om lokal testing vs. produksjon), gjennomgå `architecture.md` for feil/utdatert innhold, og rydde opp i `issues.md` – ingen kodeendringer, ingen ekte API-kall, ingen ny Vercel-opprettelse.

### Plan
- Leste `README.md`, `architecture.md` (avsnitt 10) og slutten av `process-log.md`/`issues.md` for å finne nøyaktig hva som var utdatert.
- `README.md`: la til den publiserte adressen tydelig i innledningen, skrev om "Publisering på Vercel"-seksjonen fra "foreløpig kun forberedt, ikke publisert" til faktisk status (publisert, demomodus fungerer, normalmodus bevisst ikke aktivert), og endret den nummererte Vercel-sjekklisten til å reflektere at prosjektet allerede finnes (kun nøkkel/forbrukstak gjenstår).
- `architecture.md`: gjennomgikk avsnitt 10 grundig. Fant ingen faktiske feil eller utdaterte påstander – innholdet er skrevet beskrivende ("slik er det satt opp"), ikke som en statusrapport, og stemte fortsatt med den faktiske løsningen. Gjorde bevisst ingen endring der, i tråd med "rett bare eventuelle feil".
- `process-log.md`: la til en ny seksjon med publiseringsstatus, den manuelle bekreftelsen, en oppsummering av demodata-feilen (med lenke/sammenheng til forrige økts seksjon), en tydelig forklaring på hvorfor nøkkelen bevisst ikke er lagt inn, og en kort kritisk refleksjon om forskjellen mellom lokal testing (hele repoet tilgjengelig) og en isolert, bundlet serverless-funksjon i produksjon.
- `issues.md`: markerte Vercel-prosjekt-opprettelse og produksjonstest av demomodus som fullført (løst), og la til ett nytt, fortsatt åpent punkt: normalmodus er bevisst ikke aktivert i produksjon (forbrukstak + nøkkel gjenstår).

### Resultat
Endrede filer (kun dokumentasjon):
- `README.md` – publisert adresse, oppdatert publiseringsseksjon og -sjekkliste.
- `process-log.md` – ny seksjon om fullført publisering, demodata-feil-oppsummering, kredittbeskyttelse, og kritisk refleksjon.
- `architecture.md` – **ingen endring** (gjennomgått, funnet korrekt).

Ingen applikasjonskode er endret. Ingen ekte OpenAI-kall. Ingen API-nøkkel lagt inn eller eksponert. Ingen nytt Vercel-prosjekt opprettet. Ingen git-commit/push av applikasjons-/dokumentasjonsfilene er gjort (på brukerens eksplisitte instruks – dette gjør brukeren selv) – kun denne loggfilen committes av `sesjonslogg`-skillen.

`git status` ved avslutning: `README.md` og `process-log.md` endret (ukommittert av meg); `.logs/sondre-tveit-amundsen/issues.md` og denne loggfilen committes separat av skillen.

### Åpne punkter
- Normalmodus er bevisst ikke aktivert i produksjon – gjenstår: sette forbrukstak hos OpenAI, legge `OPENAI_API_KEY` inn på Production-miljøet i Vercel, og gjøre én bevisst ekte testforespørsel i produksjon etterpå.
- Øvrige åpne punkter er uendret, se `issues.md`.
