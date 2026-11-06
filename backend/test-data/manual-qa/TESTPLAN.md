# Testplan: manuell kvalitetssikring av normalmodus mot fire fiktive testsett

Dette dokumentet beskriver hvordan de fire fiktive testsettene i denne mappen skal
brukes til å kvalitetssikre normalmodus mot en ekte språkmodell (PRD §7;
`tilbakemelding-product-brief.md`, punkt 2 under «Neste steg for gruppen»).

**Forventningene i denne mappen er definert og låst 2026-11-06, FØR noe ekte
OpenAI-kall er gjort mot testsett 2–4.** Testsett 1 gjenbruker det eksisterende
demotestsettet og dets allerede eksisterende, uavhengig skrevne forventede resultat
(`demo-result.json`). Git-tidspunktet for når disse filene committes er beviset på at
forventningene ble satt før testresultatene var kjent.

## Oversikt over testsettene

| # | Mappe | Kandidat | Arketype |
|---|---|---|---|
| 1 | `testsett-1-kari-nordmann/` (viser til eksisterende demodata) | Kari Nordmann | God match mot stillingen |
| 2 | `testsett-2-markus-eide/` | Markus Eide | Tydelige kompetansegap |
| 3 | `testsett-3-sara-lund/` | Sara Lund | Overførbar erfaring fra deltidsarbeid |
| 4 | `testsett-4-thomas-berg/` | Thomas Berg | Uklare kvalifikasjoner (hallusinasjons-stresstest) |

Hvert testsett (2–4) består av `cv.txt`, `stillingsannonse.txt` og
`forventet-resultat.md`. Alle personer, bedrifter og kontaktopplysninger er fiktive.
Telefonnummer og e-postadresse er bevisst utelatt fra de nye testsettene, siden de
ikke er nødvendige for analysen.

## Grunnprinsipp: «ikke dokumentert» ≠ «mangler ferdigheten»

Gjennom alle fire testsett skilles det konsekvent mellom:
- **«Ikke dokumentert i CV-en»** – CV-en sier ingenting om dette. Vi vet ikke om
  kandidaten faktisk har ferdigheten.
- **«Kandidaten mangler ferdigheten»** – en konklusjon CV-en alene ikke gir grunnlag
  for, og som verken forventningene eller en ekte analyse bør påstå.

Et korrekt kompetansegap i et ekte svar skal være formulert som det første, ikke det
andre. Dette er en del av det som skal vurderes for hvert testsett, ikke bare om et
gap ble "funnet".

## Meningsbaserte forventninger, ikke eksakt ordlyd

Forventningene i hvert `forventet-resultat.md` beskriver hva som **bør gjenkjennes i
meningsinnhold**. Vi krever ikke:
- identisk ordlyd som i forventningsdokumentet
- et eksakt antall styrker, gap eller forslag

Vi krever at:
- hvert krav som er markert «Styrke» faktisk dekkes av noe reelt i CV-en, med et ekte
  kildesitat
- hvert krav som er markert «Gap» ikke feilaktig dukker opp som en udiskutabel styrke
- krav markert «Skjønnsvurdering» vurderes med et kort, begrunnet notat – ikke med et
  enkelt bestått/ikke bestått

## Objektivt kontrollerbart (sjekkes først, uten skjønn)

1. Ble hvert sentrale krav identifisert i `job_requirements`?
2. For hvert krav markert «Styrke» i forventningene: finnes en tilsvarende styrke i
   det ekte svaret, med et kildesitat som faktisk finnes ordrett i `cv.txt`/
   `stillingsannonse.txt`?
3. For hvert krav markert «Gap»: er det **ikke** feilaktig presentert som en bekreftet
   styrke i svaret?
4. **Forbudslisten** i hvert testsetts `forventet-resultat.md` («Må aldri påstås som
   dokumentert»): forekommer noe av dette i styrker, forslag eller søknadsutkast? Hvis
   ja, er dette en bekreftet FR10-feil, ikke en tolkningsforskjell.
5. Er alle `cv_excerpt`/`job_ad_excerpt` i svaret ekte, ordrette (eller nær-ordrette)
   sitater fra riktig kildetekst? (Kontrolleres manuelt, uavhengig av backendens egen
   `grounding.py` – vi tester systemet utenfra.)

## Krever skjønn (vurderes kvalitativt, dokumenteres som notat – ikke bestått/ikke bestått)

- Er ordlyden i styrker/gap/forslag forståelig og godt formulert?
- Er CV-forslagene genuint nyttige råd, ikke bare teknisk forankret?
- Søknadsutkastets kvalitet, tone og personlige preg.
- De eksplisitt markerte skjønns-casene i testsett 3 (CRM vs. saksbehandlingssystem)
  og testsett 4 (skriftlig formuleringsevne).
- Om `priority` (sentral/ønskelig) som modellen velger, stemmer med vår egen vurdering.

## Prosedyre for selve testkjøringen

1. Disse filene committes og er dermed tidsstemplet **før** testkjøringen starter.
2. Hvert testsett kjøres **én gang** mot ekte `POST /api/analyze`. Et nytt forsøk er
   kun akseptabelt ved en teknisk feil (f.eks. tidsavbrudd), og skal da dokumenteres
   som en teknisk retry – ikke som en ny sjanse til et "bedre" resultat.
3. Det objektive sjekkpunktene (over) fylles ut først.
4. De skjønnsbaserte punktene vurderes og noteres separat.
5. Avvik fra forventningene klassifiseres som enten:
   - **(a) en reell feil i applikasjonen** → dokumenteres i `process-log.md` og
     `issues.md`, og rettes med en egen regresjonstest (samme mønster som
     Power BI-/SQL-feilene fra 05.11.2026), eller
   - **(b) akseptabel KI-variasjon** i ordlyd/vektlegging som ikke bryter FR7/FR10 →
     dokumenteres som observasjon, ikke som feil.
6. Forventningene i denne mappen skal **ikke** redigeres etter at en testkjøring er
   sett. Endres noe senere (f.eks. fordi vi oppdager at et testsett var utformet
   feil), skal det gjøres som en ny, tydelig markert revisjon – ikke en stille
   retting – og begrunnelsen skal fremgå.

## Hvor resultatene skal dokumenteres

- Rå JSON-svar (eller minst `result`-delen) lagres sammen med det tilhørende
  testsettet, f.eks. som `testsett-N-.../resultat-2026-MM-DD.json`, ved siden av (ikke
  i stedet for) `forventet-resultat.md`.
- En kort oppsummering av funn, avvik og eventuelle fikser føres i `process-log.md`,
  på samme måte som de tre testrundene 05.11.2026.
- Avvik som krever oppfølging føres i `.logs/<bruker>/issues.md`, med lenke til
  testsettet og til en eventuell kode-fiks/regresjonstest.
- En sesjonslogg for selve testøkten lagres i `.logs/<bruker>/`, i tråd med
  prosjektets vanlige rutine.
