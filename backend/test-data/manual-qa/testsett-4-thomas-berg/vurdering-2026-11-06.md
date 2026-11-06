# Vurdering – Testsett 4 (Thomas Berg), ekte OpenAI-kall 2026-11-06

**Resultat:** `resultat-2026-11-06.json` (HTTP 200, ett ekte kall, ingen retries).

Dette var det skarpeste testsettet (hallusinasjons-stresstest), og det er her vi fant
det eneste reelle avviket av betydning i denne testrunden.

## Objektive kontrollpunkter

| Kontroll | Utfall |
|---|---|
| Alle 5 krav identifisert (JR1–JR5) | ✅ Ja |
| Jira/Trello/Excel påstått som dokumentert *i fri tekst* (styrkebeskrivelse eller søknadsutkast) | ✅ Nei – ordene "Jira", "Trello" og "Excel" forekommer ikke i noen beskrivelse eller i søknadsutkastet |
| Alle `cv_excerpt`/`job_ad_excerpt` er ekte, ordrette sitater | ✅ Ja – samtlige sitater i styrker, gap og forslag er kontrollert og stemmer ordrett med `cv.txt`/`stillingsannonse.txt` |
| JR2 (Excel) og JR3 (skriftlig formuleringsevne) som gap, ikke ubetinget styrke | ✅ Ja, begge korrekt listet som gap med `cv_excerpt: null` |
| JR4 (tverrfaglig team), JR5 (prosjektledelse) – ekte, relevante sitater | ✅ Ja |

## Bekreftet avvik: JR1 (Jira/Trello) kobles til en vag styrke via `related_requirement_ids`

Styrken `S3` har beskrivelsen **"Har erfaring med digitale verktøy i daglig arbeid"**,
med kildesitat "Liker å bruke digitale verktøy i det daglige arbeidet" (ekte sitat,
ikke oppdiktet) – men `related_requirement_ids` for denne styrken er satt til
**`["JR1"]`**, altså kravet "Erfaring med prosjektstyringsverktøy som Jira eller
Trello".

Dette betyr at grensesnittet (`TraceableItemList.jsx`) ville vist denne styrken med
en synlig kobling til nettopp Jira/Trello-kravet – selv om selve CV-en kun nevner
generiske "digitale verktøy" og ikke noe navngitt verktøy. Dette er **nøyaktig den
sammenblandingen** testsettet ble designet for å avdekke, selv om selve tekstens
ordlyd ("digitale verktøy") teknisk sett er sann og ordrett sitert.

**Dette er et bekreftet, dokumentert avvik – ikke akseptabel KI-variasjon** – fordi
koblingen skaper et misvisende inntrykk av at et sentralt krav er dekket, når CV-en
ikke gir grunnlag for det.

### Årsak (undersøkt i koden, ikke gjettet)

`grounding.py` sin `_filter_related_requirement_ids` beholder en krav-kobling hvis
kravets beskrivelse deler et "betydningsfullt" ord med funnets egen påstand OG dets
kildesitater (`cv_excerpt`/`job_ad_excerpt`) samlet. I dette tilfellet satte modellen
`job_ad_excerpt` til **nøyaktig samme tekst som selve kravbeskrivelsen** ("Erfaring
med prosjektstyringsverktøy som Jira eller Trello"). Da blir sammenligningen
selvreferensiell: kravteksten "deler ord" med seg selv, uavhengig av om
`cv_excerpt` ("digitale verktøy") faktisk har noe meningsfullt å gjøre med
"prosjektstyringsverktøy". Filteret ble derfor ikke utløst, fordi det aldri
isolert kontrollerer om **CV-sitatet spesifikt** er relevant for kravet – det
kontrollerer om *noe* i den samlede teksten (inkl. kravets eget sitat av seg selv)
overlapper.

### Et sekundært funn: intern inkonsistens

Samme krav (JR1) opptrer **både** som et bekreftet gap (`G1`, "CV-en dokumenterer
ikke erfaring med prosjektstyringsverktøy...") **og** som koblet til en styrke
(`S3`) i samme svar. Dette er en selvmotsigelse i modellens eget resultat, uavhengig
av grunnlagskontrollen.

## Et gjennomgående mønster (sett i flere testsett, ikke isolert)

I både testsett 2 (req4/req7) og dette testsettet (JR4, tverrfaglig team) ble reelt,
allerede dokumentert CV-innhold ikke konsekvent anerkjent som en bekreftet styrke –
det endte i stedet som et "forslag om å fremheve", selv når innholdet allerede var
tydelig nok. Ikke en sikkerhetsfeil, men en gjennomgående, verdt-å-følge-med-på
kvalitetssvakhet.

## Konklusjon

**Avvik funnet – ikke bestått på ett punkt.** Søknadsutkastet og styrkenes egne
beskrivelser dikter ikke opp Jira/Trello/Excel-erfaring (den strengeste, kritiske
grensen holder), men den strukturerte krav-koblingen for `S3` gir et misvisende
bilde av at Jira/Trello-kravet er dekket.

**Anbefalt tiltak (ikke utført – krever egen godkjenning og kodeendring):**
Stram inn `_filter_related_requirement_ids` i `grounding.py` slik at
kravbeskrivelsens egen tekst ikke kan "bekrefte seg selv" via et `job_ad_excerpt`
som bare gjentar kravet – sammenligningen bør i større grad vekte om `cv_excerpt`
spesifikt (ikke bare den samlede teksten) har reell, betydningsfull overlapp med
kravet. Dette bør fikses med en egen, målrettet regresjonstest som speiler nøyaktig
dette tilfellet (vag "digitale verktøy"-styrke koblet til et spesifikt, navngitt
verktøykrav), på samme måte som SQL-/Power BI-sakene fra 05.11.2026.
