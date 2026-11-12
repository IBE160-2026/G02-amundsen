# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G02 – G02-amundsen |
| **PRD vurdert** | `prd.md` (status i frontmatter: ingen frontmatter, sist endret 2026-10-08, commit 1c5d9e9) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

PRD-en har en tydelig kjerne: lim inn CV og stillingsannonse, få styrker, gap, sporbare CV-forslag og et søknadsutkast, uten at KI finner på kvalifikasjoner. Scope er stramt og Non-Goals er konkrete. Risikoen er at FR-ene er korte «skal kunne»-setninger uten testbare konsekvenser, og at det ikke står hvordan KI-delen kontrolleres, hva demomodus faktisk viser og hva som skjer med CV-en når den sendes til en ekstern språkmodell. Det er akkurat det UX, arkitektur og stories trenger å hente ut.

## 2. Dette fungerer godt

- **Tydelig tese og ærlig avgrensning.** §1: «forslagene skal være sporbare tilbake til informasjon i CV-en og stillingsannonsen» og «skal ikke finne på kvalifikasjoner». Dette er det som skiller appen fra en vanlig chatbot, og FR7 og FR10 følger opp tesen.
- **Konkret scope.** §3 lister ti utelatelser (ingen PDF/Word, ingen lagring, ingen innlogging, ingen automatisk henting av annonser). Det gjør v1 realistisk for en liten gruppe og lett å forsvare.
- **Testtenkning er på plass.** §7: «3–5 fiktive testsett» med forventede styrker og gap, og skillet mellom deterministiske funksjoner (automatiske tester) og variable KI-svar (vurderes mot faste testsett). Det viser at dere har tenkt på kvalitetssikring.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | god | Tekst inn, ingen lagring og demomodus er stilt fram som valg. Hva som ble valgt bort (PDF, innlogging) og hvorfor står ikke, og modellvalg og kostnad er skjøvet til arkitektur. |
| Substans | god | Ingen persona- eller visjonsteater. NFR-ene er delvis adjektiver (NFR1 «enkelt og oversiktlig»), men NFR3–NFR6 er produktspesifikke. |
| Strategisk sammenheng | god | Funksjonene tjener tesen (sporbarhet, ingen oppdikting). Mangler måling av om tesen holder. |
| Testbarhet | svak | FR1–FR12 har ingen konsekvenser. «Relevante», «konkrete» og «de viktigste forslagene» er ikke definert. |
| Scope og avgrensning | god | Sterke Non-Goals. Ingen eksplisitt MVP-in/out-liste, ingen `[ASSUMPTION]`-merking. |
| Brukbarhet for neste fase | svak | Ingen glossar, flere duplikatkrav (FR/NFR) og uavklarte termer («økt», «normal modus»). |
| Formtilpasning | god | Enkelt verktøy med én rolle: §4 User Flow dekker behovet for brukerreiser. Overskrifter er på engelsk, innholdet på norsk. |

## 4. Viktigste forbedringer

### 4.1 FR-ene har ingen testbare konsekvenser
- **Alvorlighet:** høy
- **Hvor:** §5, f.eks. FR7: «For de viktigste forslagene skal applikasjonen vise hvilken del av CV-en og … forslaget bygger på.»
- **Problem og hvorfor det betyr noe:** Stories og tester skal bygges direkte på FR-ene. Uten konsekvenser vet ingen når FR7 er ferdig, og «de viktigste» kan tolkes som ett forslag eller alle. §7 har gode kriterier, men de er ikke knyttet til FR-ene.
- **Forslag:** Flytt kriteriene fra §7 inn under hvert FR som konsekvenser. Eksempel:
  > **FR7 – Sporbarhet.** Hvert CV-forslag har en kildehenvisning.
  > - Hvert forslag viser minst ett sitat fra CV-en og minst ett fra annonsen.
  > - Sitatet finnes ordrett i brukerens input (kan sjekkes automatisk).
  > - Forslag uten gyldig kilde vises ikke.

### 4.2 Kontroll av KI-svar og innhold i demomodus er ikke beskrevet
- **Alvorlighet:** høy
- **Hvor:** §5 FR10 «ikke presentere kvalifikasjoner … som om brukeren har dem», FR12, §7 «KI-resultater kan variere»
- **Problem og hvorfor det betyr noe:** FR10 er produktets viktigste løfte, men sier ikke hvordan det sjekkes eller hva appen gjør når den er usikker. Et gap er per definisjon noe brukeren ikke har, så brevet må skille «dette har du» fra «dette mangler du». FR12 sier ikke om demomodus viser faste svar uansett input, eller om brukeren kan lime inn egen tekst. Modell, kostnad og rate-begrensning er heller ikke nevnt.
- **Forslag:** Skriv FR10 som testbart krav: «Søknadsutkastet inneholder ingen ferdighet, rolle eller verktøy som ikke finnes i CV-en. Testsett 3 har en annonse som krever Python, mens CV-en ikke nevner Python. Utkastet nevner ikke Python som egen erfaring.» Legg til: «Når appen er usikker, markerer den påstanden som ‹må bekreftes av deg› i stedet for å formulere den som fakta.» Beskriv demomodus: «Demomodus viser alltid ferdig eksempelresultat, gjør ingen språkmodellkall og koster ingenting.» Sett en øvre grense for lengde på input og antall kall per økt.

### 4.3 Personvern gjelder mer enn lagring
- **Alvorlighet:** medium
- **Hvor:** §1 «uten lagring av personopplysninger», FR11, NFR3
- **Problem og hvorfor det betyr noe:** CV-en inneholder personopplysninger og sendes til en ekstern språkmodell. «Ikke lagret hos oss» er ikke det samme som «ikke delt». Brukeren bør få vite det før de limer inn, og det påvirker arkitekturen (logger, feilsøking, tredjepart).
- **Forslag:** Legg til: «Før analysen starter, vises en tekst om at CV og annonse sendes til [leverandør]. Applikasjonen skriver ikke CV-innhold til serverlogg.» Slå sammen FR11 og NFR3 til ett krav med testbar konsekvens («etter at siden lastes på nytt er alle felt tomme»).

### 4.4 Ingen måling av om tesen holder
- **Alvorlighet:** medium
- **Hvor:** PRD-en som helhet (ingen suksessmål), §2 «redusere risikoen for at KI finner på …»
- **Problem og hvorfor det betyr noe:** Målene i §2 kan ikke avgjøres. Uten et mål vet dere ikke når v1 er «bra nok», og demo og testing mangler et felles utgangspunkt.
- **Forslag:** Legg til to-tre mål knyttet til testsettene i §7, f.eks. «SM-1: På alle testsett finner analysen minst 80 % av de forventede styrkene og gapene», «SM-2: 0 oppdiktede kvalifikasjoner i søknadsutkastene på alle testsett». Legg også til et motmål, f.eks. at appen ikke skal bli så forsiktig at den ikke foreslår noe.

### 4.5 Termer og duplikatkrav må ryddes
- **Alvorlighet:** lav
- **Hvor:** §5/§6: FR7 og NFR8, FR11 og NFR3, FR12 og NFR6; §4 «økten», «normal modus»
- **Problem og hvorfor det betyr noe:** Samme krav to steder gir to stories og to tester for én ting, og ved endring blir de ulike. Uten glossar kan «styrke», «kompetansegap», «krav» og «økt» brukes ulikt i UX, kode og tester.
- **Forslag:** Lag et kort glossar (6–8 termer, f.eks. Styrke, Kompetansegap, Krav, Forslag, Kildehenvisning, Økt, Demomodus). La NFR-ene bare referere til FR-ene, eller fjern dem.

## 5. Mekaniske funn

- Ingen frontmatter (tittel, dato, status), så versjon og status kan ikke leses ut av filen.
- Ingen glossar, ingen UJ-/SM-ID-er, ingen `[ASSUMPTION]`-tagger og ingen Assumptions Index. For dette produktet er det akseptabelt at §4 User Flow erstatter UJ-er, men det bør stå eksplisitt i et avsnitt om dokumentets formål.
- FR1–FR12 og NFR1–NFR8 er sammenhengende uten hull eller dubletter. Ingen krysshenvisninger mellom FR, NFR og §7, så sporbarhet fra krav til test må gjøres for hånd.
- §8 «hvordan applikasjonen skal kjøres lokalt» er listet som åpen, mens NFR5 allerede krever det. Avklar hva som faktisk er åpent.

## 6. Før dere går videre

**Må avklares før UX, arkitektur og epics:**
- Testbare konsekvenser per FR (4.1), spesielt FR7 og FR10.
- Hva demomodus er og ikke er (4.2), og hva som skal vises når KI er usikker.
- Hva som sendes til språkmodellen, og hva brukeren får vite om det (4.3).

**Kan vente:**
- Suksessmål og motmål (4.4), så lenge testsettene lages først.
- Glossar og opprydding av dubletter (4.5), men gjør det før stories skrives.
- Valg av modell og teknologi, slik §8 allerede sier.

**Oppfølging av tilbakemeldingen på product brief:** delvis. Tekstinput, ingen lagring/innlogging, demomodus, `.env` for nøkkel og 3–5 fiktive testsett er fulgt opp. Modellvalg og kostnad er skjøvet til arkitektur, og suksesskriteriene i §7 er ikke blitt målbare «brukeren kan …»-krav med forventet resultat.

## 7. Refleksjonsspørsmål

1. FR10 er appens viktigste løfte. Hvordan ville dere oppdaget at KI-en hadde diktet opp en ferdighet i et utkast, og hvilken av testsettene i §7 ville avslørt det?
2. Hvilke deler av PRD-en skrev KI-en, og hvilke krav la dere til eller strammet inn selv etter å ha lest dem kritisk? Hva ville dere ha endret hvis dere skulle skrevet FR7 på nytt uten KI?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
