# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G02 – G02-amundsen |
| **Product brief** | `product-brief.md` (commit `523aae2`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Problemet er godt formulert og gjenkjennelig: unge og nyutdannede som har relevant erfaring fra deltidsjobb, praksis og verv, men som ikke klarer å koble den til kravene i en konkret stillingsannonse. Dilemmaet mellom effektivitet og autentisitet gir appen en tydelig profil.
2. Scope er ryddig delt i «In for v1» og «Out for v1». Det er klokt å holde automatisk henting fra Finn.no/LinkedIn, automatisk innsending, ATS-optimalisering og sammenligning av mange stillinger utenfor første versjon.
3. Kravet om at appen ikke skal finne på kvalifikasjoner brukeren ikke har, er et godt og konkret kvalitetsprinsipp som kan bli tester.

**De viktigste endringene:**

1. Briefen sier ingenting om hvordan appen skal bruke en språkmodell, hva det koster, og hvordan sensor kan kjøre appen uten deres API-nøkkel. Det må avklares før PRD og arkitektur.
2. Flere suksesskriterier er ikke testbare slik de står («forstå hvorfor de viktigste forslagene er gitt», «redusere tiden det tar»). Gjør dem om til konkrete «brukeren kan …»-kriterier med forventet resultat.
3. Avklar hvordan CV-en kommer inn i appen (lim inn tekst eller last opp PDF/Word), og om CV-er og søknader lagres. Det avgjør om dere trenger innlogging og hvordan personopplysninger skal håndteres.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 2) AI CV- og søknadsassistent (middels). Ideen ligger svært nær dette forslaget, og v1 er avgrenset omtrent som forslaget beskriver.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Lite tradisjonell beregning, men matching mellom CV og stillingskrav, styrker og kompetansegap må gi meningsfulle resultater. Det meste av «logikken» ligger i prompts. |
| Datamodell – antall entiteter og relasjoner mellom dem | Lav | Bruker, CV/profil, stillingsannonse og analyse/søknadsutkast. Få entiteter, enkle relasjoner. |
| Brukere, roller og innlogging | Lav–middels | Én brukerrolle. Innlogging er ikke nevnt, men blir nødvendig hvis CV-er og utkast skal lagres mellom økter. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Høy | Hele kjerneflyten (matching, gap-analyse, CV-forslag, søknadsbrev og forklaringer) bygger på språkmodellkall. Kravet om ingen oppdiktede kvalifikasjoner må kontrolleres. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Middels | Én ekstern tjeneste (språkmodell-API). Andre integrasjoner er riktig plassert utenfor v1. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Ikke relevant. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Middels | «Legge inn eller laste opp CV» og støttedokumentasjon betyr PDF/Word-lesing, som ofte er upålitelig. Innliming av tekst er langt enklere. |
| Sikkerhet og personvern | Middels | CV-er og attester er personopplysninger, og innholdet sendes til en ekstern språkmodell. Briefen nevner ikke dette. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten (CV og annonse inn → analyse av styrker og gap → CV-forslag → søknadsutkast) blir ferdig og stabil før dere legger til støttedokumentasjon eller andre utvidelser. Ettersom dere ser ut til å være en liten gruppe, er det ekstra viktig å holde v1 stramt.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | OK | Sju punkter i «In for v1», men de henger sammen i én flyt. Realistisk hvis støttedokumentasjon og filopplasting holdes enkelt eller utsettes. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Problem og scope er tydelige, men det mangler avklaringer om input-format, lagring, innlogging og språkmodell. Disse hullene vil dukke opp i PRD. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | En vanlig webapp med skjemaer og et LLM-API passer godt for Claude Code. Teknologivalg tas i arkitekturen. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Dere kan vurdere om et søknadsbrev er godt, men det er vanskelig å sjekke systematisk at gap-analysen er riktig og at ingen kvalifikasjoner er diktet opp. Lag noen faste eksempel-CV-er og annonser med forventede styrker/gap som dere tester mot. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Risiko | Kjerneflyten kan testes (input → output vises), men KI-svarene varierer. Skill mellom deterministisk kode (validering, lagring, flyt) som testes automatisk, og KI-kvalitet som testes med faste eksempler og manuell vurdering. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Stor risiko | Uten plan vil appen kreve en API-nøkkel sensor ikke har. Planlegg en mock-/demomodus med ferdige svar, eller en tydelig `.env.example` og beskrivelse av hvordan sensor bruker egen nøkkel. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | Språkmodell-API koster penger per kall. Briefen sier ingenting om valg av modell, kostnad eller testmodus. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. La CV og stillingsannonse limes inn som tekst i v1. Legg PDF/Word-opplasting og støttedokumentasjon (attester og vurderinger) i et senere trinn når kjerneflyten virker.
2. Bestem om v1 skal lagre noe. En versjon uten innlogging der analysen bare vises i økten, er enklest og reduserer personvernrisikoen. Velger dere lagring, legg til enkel innlogging og beskriv hvordan CV-data beskyttes.
3. Legg inn en demomodus med faste eksempelsvar, slik at appen kan kjøres og testes uten nøkkel og uten kostnad.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Tydelig: en jobbsøknadsassistent som kobler CV mot en konkret stilling, finner styrker og gap og lager søknadsutkast. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Godt beskrevet med erfaringer fra deltidsarbeid, praksis og verv. Kunne blitt enda sterkere med ett konkret eksempel på en student og en stilling. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Juster | Beskriver hva appen gjør, men ikke hvordan brukeren opplever det. Beskriv flyten steg for steg: hva brukeren ser, hva de kan redigere, og hva de sitter igjen med. |
| What Makes This Different – er vurderingen ærlig og realistisk? | Juster | Forankring i egne erfaringer og autentisitet er en god idé, men generelle chatboter kan gjøre mye av det samme. Si konkret hva appen gjør annerledes, f.eks. at hvert forslag peker på hvilken del av CV-en det bygger på. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Studenter, nyutdannede og unge yrkesaktive er tre grupper. Velg én primærbruker, f.eks. en bachelorstudent i siste semester som søker sin første faste jobb. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | De fleste punktene er gode funksjonelle krav, men «forstå hvorfor», «forankret i faktiske erfaringer» og «redusere tiden» må gjøres målbare, f.eks. «hvert CV-forslag viser hvilken del av CV-en og annonsen det bygger på». |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | God avgrensning, men støttedokumentasjon står som «kan inkluderes». Bestem ja eller nei, og avklar input-format og lagring. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Karriereplattform, intervjuforberedelse og kompetanseprofil er tydelig plassert som fremtid og ikke del av v1. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Punktene i «In for v1» kan bli stories direkte. Repoet har så langt bare briefen; fortsett med PRD, arkitektur og stories, og lagre prompts og KI-økter underveis. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | OK | Én tydelig kjerneflyt med nok innhold. Hold støttedokumentasjon og filopplasting som utvidelser. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Endre | Lag målbare kriterier og et sett eksempel-CV-er og annonser med forventet resultat, slik at dere kan sjekke at KI-svarene ikke dikter opp erfaring. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Skisser de viktigste skjermbildene: input av CV og annonse, resultat med styrker/gap og forslag, og redigerbart søknadsutkast. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Ingen teknologivalg ennå. Velg en enkel, vanlig stakk i arkitekturen og begrunn valg av språkmodell. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Endre | Planlegg demomodus eller tydelig oppsett med egen nøkkel, slik at sensor kan kjøre appen etter README. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Bestem nå at API-nøkler ligger i `.env` (i `.gitignore`) med en `.env.example`, og at eksempel-CV-er er fiktive. Briefen ligger i rotmappen; vurder en egen mappe for planleggingsdokumenter. |

## 3. Neste steg for gruppen

1. Avklar språkmodell, kostnad og demomodus, og skriv det inn i briefen eller i et addendum, slik at det er tydelig før arkitekturen.
2. Skriv om suksesskriteriene til målbare «brukeren kan …»-krav, og lag 3–5 fiktive eksempel-CV-er og stillingsannonser med forventede styrker og gap.
3. Bestem input-format (tekst først) og om noe skal lagres, og gå deretter videre til PRD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
