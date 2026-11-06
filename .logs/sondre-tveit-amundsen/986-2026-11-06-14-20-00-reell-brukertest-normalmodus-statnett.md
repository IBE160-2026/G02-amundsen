# Reell brukertest i lokal normalmodus (anonymisert CV, Statnett-annonse)

## 2026-11-06 kl. 14:20 — Sondre Tveit Amundsen

### Oppgave
Brukeren gjennomførte en reell test av Career Transition Assistant i lokal normalmodus, med en anonymisert, ekte CV og en ekte stillingsannonse fra Statnett (rådgiver/seniorrådgiver økonomi og kostnadsoptimalisering). Søknadsutkastet inneholdt ingen tydelig oppdiktet erfaring, men tre kvalitetsproblemer ble rapportert: (1) en styrke om generell arbeidskapasitet/evne til å håndtere flere oppgaver og tidsfrister ble koblet til et spesifikt, urelatert fagkrav om IT-økonomistyring og analyse av store datamengder; (2) et sammensatt krav (IT-kostnadsmodeller, lisensforvaltning, analyse av store datamengder) ble ikke tydelig fanget opp som manglende dokumentasjon; (3) et mastergrad-krav ble presentert som et absolutt kompetansegap, selv om annonsen selv åpnet for at relevant erfaring kunne kompensere for dette. Oppgaven: undersøk årsakene, gjennomfør kun målrettede, begrunnede forbedringer, legg til regresjonstester (særlig for svake koblinger mellom generelle personlige egenskaper og spesifikke fagkrav), bevar eksisterende funksjonalitet/sporbarhet, kjør alle relevante tester, og dokumenter testen/funnene/endringene/gjenværende begrensninger ærlig i `process-log.md`. Ingen ekte CV/personopplysninger i repoet, ingen nye API-kall, ingen endring av `.env`/API-nøkler/Vercel-konfig.

### Plan
- Leste `backend/app/grounding.py`, `backend/app/prompts.py`, `backend/app/models.py` og eksisterende `backend/tests/test_grounding.py` for å forstå nåværende logikk og testkonvensjoner før noe ble endret.
- Funn 1: vurderte om feilen kunne forklares av den eksisterende, deterministiske nøkkelord-heuristikken i `grounding.py` (samme feilfamilie som tidligere rettet). Siden rå-modellsvar ikke logges (NFR3), kan ikke det eksakte delte ordet bekreftes 100 % – men koden viser at flere brede, generiske ord om kapasitet/mengde ("stor"/"store", "håndtere", "tidsfrister" m.fl.) fortsatt telles som et gyldig tematisk treff. Dette er en tilstrekkelig, demonstrerbar forklaring, i tråd med tidligere rettinger i samme modul.
- Funn 2 og 3 kan IKKE rettes i `grounding.py` (den luker bare bort feil i et allerede mottatt svar – den kan ikke få modellen til å nevne noe utelatt eller beholde en tapt nyanse). Disse er derfor adressert som nye, målrettede regler i systemprompten (`prompts.py`).
- Utvidet `_GENERIC_WORDS` i `grounding.py` med kapasitets-/mengdeord, og la til to nye, syntetiske (ikke ekte) regresjonstester i `test_grounding.py` som gjenskaper funn 1.
- Verifiserte fail-before/pass-after manuelt: fjernet den nye ordlisteutvidelsen temporært, bekreftet at den nye testen feiler (koblingen besto feilaktig), la fiksen tilbake, bekreftet at testen består.
- Kjørte full backend- og frontend-testsuite.
- Dokumenterte testen, årsaksanalysen, endringene og den ærlige, uverifiserte statusen til promptendringene i `process-log.md`.

### Resultat
- **`backend/app/grounding.py`** (endret): `_GENERIC_WORDS` utvidet med "stor", "store", "flere", "håndtere", "håndtering", "håndterer", "kapasitet", "tidsfrist", "tidsfrister", "mengde", "mengder", "samtidig". Docstring utvidet med funn 1 og begrunnelsen.
- **`backend/app/prompts.py`** (endret): to nye regler (9 og 10) i `SYSTEM_PROMPT` – regel 9 krever at hver spesifikke, udokumenterte del av et sammensatt krav presenteres som eget kompetansegap; regel 10 krever at en "kan kompenseres av relevant erfaring"-nyanse fra annonsen tas med i kravets/gapets beskrivelse. Docstring utvidet med funn 2 og 3, og en eksplisitt merknad om at disse IKKE er verifisert mot et ekte API-kall denne økten.
- **`backend/tests/test_grounding.py`** (endret): lagt til to nye fiktive CV-/annonselinjer i `CV_TEXT`/`JOB_AD_TEXT`, samt to nye tester (`test_strength_real_user_test_case_generic_capacity_is_not_linked_to_specific_requirement` og `test_shares_relevant_keyword_false_for_generic_capacity_words_alone`) som gjenskaper funn 1 med syntetisk tekst. Bekreftet manuelt at den første feiler uten fiksen og består med den.
- **`process-log.md`** (endret): ny seksjon "06.11.2026 – Reell brukertest i lokal normalmodus (anonymisert CV, Statnett-annonse)" med gjennomføring, årsak, endringer, testing og en egen "Kritisk vurdering"-del som eksplisitt skiller mellom det som er bevist (grounding-fiksen) og det som IKKE kan garanteres uten en ny, reell KI-test (de to nye promptreglene).
- Testresultat: `uv run pytest` → **83/83 bestått** (opp fra 81). `npm test` (frontend) → **23/23 bestått** (uendret, ingen frontend-endring).
- Ingen ekte CV, personopplysninger eller stillingsannonsetekst er lagt i repoet. Ingen nye OpenAI-kall. Ingen endring av `.env`, API-nøkler eller Vercel-konfigurasjon.
- Ingen av de fire endrede filene (`grounding.py`, `prompts.py`, `test_grounding.py`, `process-log.md`) er committet av meg – kun denne sesjonsloggen og `issues.md` committes nå, per brukerens instruks («det gjør jeg selv»).

### Åpne punkter
- Promptendringene (regel 9 og 10) er ikke verifisert mot et nytt, ekte OpenAI-kall – det kan derfor ikke garanteres at språkmodellen faktisk dekker sammensatte krav bedre, eller bevarer kompensasjonsnyanser, før en ny reell test er kjørt i normalmodus.
- Nøkkelord-heuristikkens grunnleggende begrensning er uendret: den kan fortsatt i prinsippet la en annen, ikke-identifisert generisk ordoverlapp skape en svak kobling – denne rettingen dekker kun de konkret identifiserte ordene fra dette funnet, ikke alle tenkelige tilfeller.
- Øvrige, tidligere åpne punkter er uendret, se `issues.md`.

## 2026-11-06 kl. 14:45 — Sondre Tveit Amundsen

### Oppgave
Brukeren testet lokal normalmodus på nytt med SAMME anonymiserte CV og Statnett-annonse, etter forrige retting. Den tidligere feilkoblingen (generell arbeidskapasitet → IT-økonomistyring, under «Relevante styrker») var bekreftet borte. Tre nye svakheter ble funnet: (1) under «Forslag til CV-tilpasning» ble erfaring med å kombinere fulltidsjobb og studier koblet til kravet om analyse av store datamengder; (2) analysen viste fortsatt bare manglende mastergrad som kompetansegap, ikke de udokumenterte IT-controlling/lisensforvaltning/IT-kostnadsmodeller/dataanalyse-delene; (3) samme «fulltidsjobb og studier»-erfaring ble brukt som "bevis" på at relevant erfaring kunne kompensere for mastergrad-kravet. Oppgave: undersøk årsakene, utvid den målrettede grounding-kontrollen til CV-forslag der forsvarlig, undersøk hvorfor forrige promptregel (9) ikke løste funn 2 i praksis, gjennomfør bare avgrensede, begrunnede endringer, legg til regresjonstester med fiktive data, kjør alle tester, dokumenter ærlig i `process-log.md` (ikke påstå uverifisert effekt mot ekte KI).

### Plan
- Leste oppdatert `backend/app/grounding.py` (inkl. forrige økts fiks) og identifiserte at `_filter_related_requirement_ids` fortsatt inkluderte CV-forslagets EGEN fritekst (`suggestion`-feltet) i sammenligningsgrunnlaget mot kravteksten – samme grunnleggende svakhet som tidligere ble fjernet for `job_ad_excerpt`, nå i et nytt felt, og spesifikt for CV-forslag (ikke styrker, der ingen tilsvarende feil er rapportert).
- Endret `_filter_related_requirement_ids` til å bruke KUN `cv_excerpt` (ikke forslagsteksten) som grunnlag for CV-forslagets krav-koblinger. Styrker/kompetansegap er uendret (minst mulig, avgrenset endring).
- La til to nye fiktive linjer i `CV_TEXT`/`JOB_AD_TEXT` i `test_grounding.py`, og to nye tester: én som gjenskaper funn 1 (feiler uten fiksen, består med), én som bekrefter at en legitim CV-forslag-kobling (via et presist fagord i `cv_excerpt`) fortsatt fungerer.
- Verifiserte fail-before/pass-after manuelt (fjernet fiksen temporært, bekreftet feil, la den tilbake, bekreftet bestått).
- For funn 2: resonnerte (uten å kunne bekrefte mot rå-modelldata, som ikke logges) at den mest nærliggende forklaringen er at det feilkoblede CV-forslaget fra funn 1 «dekket» samme krav i modellens svar, og at forrige regel 9 ikke sa eksplisitt at dette ikke fritar fra kompetansegap-plikten. Skrev om regel 9 (bryt sammensatt krav ned i navngitte deler, vurder hver for seg) og la til ny regel 11 (svak kobling fritar aldri fra regel 9).
- For funn 3: la til ny regel 12 (en generell, udokumentert egenskap kan ikke i seg selv utgjøre «kompenserende relevant erfaring» for et fagspesifikt krav).
- Kjørte full backend- og frontend-testsuite.
- Dokumenterte gjennomføring, årsaksanalyse, endringer og en eksplisitt «hva er bevist vs. hva er kun begrunnet»-vurdering i `process-log.md`.

### Resultat
- **`backend/app/grounding.py`** (endret): `_filter_related_requirement_ids` bruker nå kun `cv_excerpt` som grunnlag for CV-forslagets krav-koblinger (ikke lenger forslagets egen fritekst). Docstring (modul- og funksjonsnivå) utvidet med funn 1 og begrunnelsen.
- **`backend/app/prompts.py`** (endret): regel 9 omskrevet til å kreve nedbrytning av sammensatte krav i navngitte deler; ny regel 11 (svak kobling fritar ikke fra regel 9); ny regel 12 (kompenserende erfaring må være fagrelevant, ikke generell). Docstring utvidet med funn 2/3 og en eksplisitt, uendret forbehold: IKKE verifisert mot et ekte API-kall.
- **`backend/tests/test_grounding.py`** (endret): to nye fiktive CV-/annonselinjer, og to nye tester (`test_suggestion_own_text_cannot_self_confirm_requirement_link`, `test_suggestion_related_requirement_link_survives_via_relevant_cv_excerpt`). Fail-before/pass-after bekreftet manuelt for den første.
- **`process-log.md`** (endret): ny seksjon «06.11.2026 – Oppfølgende reell brukertest» med gjennomføring, årsak, endringer, testing og en «Kritisk vurdering»-del som eksplisitt skiller bevist (grounding-fiksen) fra kun begrunnet/uverifisert (promptreglene).
- Testresultat: `uv run pytest` → **85/85 bestått** (opp fra 83). `npm test` (frontend) → **23/23 bestått** (uendret).
- Ingen ekte CV, personopplysninger eller stillingsannonsetekst i repoet. Ingen nye OpenAI-kall. Ingen endring av `.env`, API-nøkler eller Vercel-konfigurasjon.
- Ingen av de fire endrede filene er committet av meg – kun denne sesjonsloggen og `issues.md` committes nå, per brukerens instruks.

### Åpne punkter
- De tre nye/omskrevne promptreglene (9 omskrevet, 11, 12 nye) er IKKE verifisert mot et ekte OpenAI-kall. Erfaringen fra forrige runde (regel 9 sin opprinnelige versjon beviselig ikke løste funn 2) viser konkret at promptjusteringer ikke kan garanteres å virke før de er testet mot et reelt svar – dette gjelder også denne rundens endringer.
- Nøkkelord-/fritekst-heuristikkens grunnleggende begrensning er uendret: denne rettingen dekker de konkret identifiserte feilkanalene (generiske ord for styrker, forslagstekst for CV-forslag), ikke alle tenkelige varianter.
- Øvrige, tidligere åpne punkter er uendret, se `issues.md`.
