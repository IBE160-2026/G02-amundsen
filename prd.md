# PRD: Career Transition Assistant

## 1. Product Overview

Career Transition Assistant er en KI-basert jobbsøknadsassistent for studenter i avsluttende fase av et bachelor- eller masterstudium som søker sin første faste jobb og har begrenset relevant arbeidserfaring.

Brukeren limer inn CV og en konkret stillingsannonse som tekst. Applikasjonen analyserer hvordan brukerens erfaring og kompetanse samsvarer med kravene i stillingen, identifiserer relevante styrker og kompetansegap, foreslår tilpasninger i CV-en og genererer et førsteutkast til et tilpasset søknadsbrev.

Løsningen skal hjelpe brukeren med å presentere egen kompetanse mer målrettet, samtidig som forslagene skal være sporbare tilbake til informasjon i CV-en og stillingsannonsen. Applikasjonen skal ikke finne på kvalifikasjoner eller erfaringer som ikke finnes i brukerens input.

Første versjon skal kunne brukes uten innlogging og uten lagring av personopplysninger. Den skal også ha en demomodus slik at hovedfunksjonaliteten kan testes uten egen API-nøkkel.

## 2. Product Goals

Målet med første versjon er å:

- gjøre det enklere for brukeren å koble egen erfaring og kompetanse til kravene i en konkret stillingsannonse
- identifisere relevante styrker og kompetansegap på en tydelig og strukturert måte
- foreslå konkrete og etterprøvbare tilpasninger i CV-en
- generere et førsteutkast til søknadsbrev basert på brukerens faktiske input
- sikre at forslag kan spores tilbake til informasjon i CV og stillingsannonse
- redusere risikoen for at KI finner på kvalifikasjoner eller erfaringer
- tilby en enkel demomodus slik at løsningen kan testes uten egen API-nøkkel
- holde første versjon liten nok til å kunne utvikles, testes og kvalitetssikres innenfor prosjektperioden

## 3. Non-Goals / Out of Scope

Første versjon skal ikke inkludere:

- opplasting eller lesing av CV i PDF- eller Word-format
- støttedokumentasjon som attester eller vurderinger
- innlogging eller brukerprofiler
- lagring av CV, stillingsannonser, analyser eller søknadsutkast
- automatisk henting av stillingsannonser fra Finn.no, LinkedIn eller andre eksterne tjenester
- automatisk innsending av jobbsøknader
- avansert ATS-optimalisering
- sammenligning av mange stillinger samtidig
- full karriereplanlegging eller forslag til utdanning og kurs
- avansert historikk eller dashboard for tidligere søknader
- integrasjon mot e-post, LinkedIn eller eksterne rekrutteringssystemer

## 4. User Flow

Hovedflyten i applikasjonen skal være:

1. Brukeren åpner applikasjonen.
2. Brukeren velger enten normal modus eller demomodus.
3. I normal modus limer brukeren inn CV som tekst.
4. Brukeren limer inn en konkret stillingsannonse som tekst.
5. Brukeren starter analysen.
6. Applikasjonen analyserer CV og stillingsannonse og identifiserer:
   - relevante styrker
   - kompetansegap
   - relevante krav i stillingsannonsen
7. Applikasjonen viser konkrete forslag til hvordan CV-en kan tilpasses.
8. For de viktigste forslagene vises hvilken del av CV-en og stillingsannonsen forslaget bygger på.
9. Applikasjonen genererer et førsteutkast til søknadsbrev basert på brukerens input.
10. Brukeren kan lese og redigere søknadsutkastet videre.
11. Når økten avsluttes, lagres ikke CV, stillingsannonse, analyse eller søknadsutkast.

I demomodus brukes ferdige eksempeldata og eksempelresultater slik at hovedflyten kan testes uten egen API-nøkkel.

## 5. Functional Requirements

### FR1 – Input av CV
Brukeren skal kunne lime inn CV som tekst i et eget felt.

### FR2 – Input av stillingsannonse
Brukeren skal kunne lime inn en konkret stillingsannonse som tekst i et eget felt.

### FR3 – Analyse av samsvar
Applikasjonen skal analysere CV og stillingsannonse og identifisere hvordan brukerens erfaring og kompetanse samsvarer med kravene i stillingen.

### FR4 – Identifisering av styrker
Applikasjonen skal identifisere relevante styrker som kan spores tilbake til informasjon i brukerens CV.

### FR5 – Identifisering av kompetansegap
Applikasjonen skal identifisere relevante kompetansegap mellom brukerens bakgrunn og kravene i stillingsannonsen.

### FR6 – CV-forslag
Applikasjonen skal gi konkrete forslag til hvordan CV-en kan tilpasses den aktuelle stillingen.

### FR7 – Sporbarhet
For de viktigste forslagene skal applikasjonen vise hvilken del av CV-en og hvilken del av stillingsannonsen forslaget bygger på.

### FR8 – Søknadsutkast
Applikasjonen skal generere et førsteutkast til søknadsbrev basert på brukerens CV og den aktuelle stillingsannonsen.

### FR9 – Redigering
Brukeren skal kunne redigere søknadsutkastet etter at det er generert.

### FR10 – Ingen oppdiktede kvalifikasjoner
Applikasjonen skal ikke presentere kvalifikasjoner eller erfaringer som om brukeren har dem dersom de ikke finnes i brukerens input.

### FR11 – Ingen lagring
Applikasjonen skal ikke lagre CV, stillingsannonse, analyse eller søknadsutkast etter at økten avsluttes.

### FR12 – Demomodus
Applikasjonen skal ha en demomodus med ferdige eksempeldata og eksempelresultater som kan brukes uten egen API-nøkkel.

## 6. Non-Functional Requirements

### NFR1 – Brukervennlighet
Applikasjonen skal ha et enkelt og oversiktlig grensesnitt der brukeren tydelig forstår hvor CV og stillingsannonse skal legges inn, hvordan analysen startes og hvor resultatene vises.

### NFR2 – Respons og tilbakemelding
Applikasjonen skal gi tydelig tilbakemelding når en analyse pågår, er ferdig eller ikke kan gjennomføres.

### NFR3 – Personvern
CV, stillingsannonse, analyse og søknadsutkast skal ikke lagres permanent i første versjon.

### NFR4 – Sikker håndtering av API-nøkkel
API-nøkkelen skal lagres lokalt i en `.env`-fil og skal ikke pushes til GitHub.

### NFR5 – Kjørbarhet
Applikasjonen skal kunne kjøres lokalt etter instruksjoner i README.

### NFR6 – Demomodus
Sensor skal kunne teste hovedflyten i applikasjonen uten egen API-nøkkel eller betalt tilgang til en språkmodell.

### NFR7 – Feilhåndtering
Applikasjonen skal vise forståelige feilmeldinger dersom input mangler eller et språkmodellkall mislykkes.

### NFR8 – Sporbarhet
Det skal være mulig å kontrollere hvilke deler av CV og stillingsannonse de viktigste forslagene bygger på.

## 7. Acceptance Criteria and Testing

Første versjon skal testes mot et lite sett med fiktive CV-er og stillingsannonser der forventede styrker, kompetansegap og relevante krav er definert på forhånd.

Følgende kriterier skal kunne kontrolleres:

- brukeren kan lime inn både CV og stillingsannonse
- analysen kan gjennomføres uten manglende input
- relevante styrker kan spores tilbake til informasjon i CV-en
- identifiserte kompetansegap kan spores tilbake til krav i stillingsannonsen
- CV-forslagene bygger på informasjon som faktisk finnes i brukerens input
- søknadsutkastet inneholder ikke oppdiktede kvalifikasjoner eller erfaringer
- demomodus fungerer uten egen API-nøkkel
- applikasjonen viser forståelige feilmeldinger ved manglende input
- applikasjonen kan kjøres lokalt etter README-instruksjonene

Det skal lages 3–5 fiktive testsett bestående av:
- en CV
- en stillingsannonse
- forventede relevante styrker
- forventede kompetansegap
- sentrale krav som analysen bør identifisere

KI-resultater kan variere mellom kjøringer. Derfor skal deterministiske funksjoner testes automatisk der det er mulig, mens kvaliteten på KI-genererte resultater vurderes mot de faste testsettene.

## 8. Open Decisions

Følgende beslutninger tas i arkitekturfasen:

- valg av språkmodell og API
- valg av frontend- og backend-teknologi
- hvordan demomodus skal implementeres teknisk
- hvordan prompts og KI-svar skal struktureres
- hvordan testdata skal organiseres i prosjektet
- hvordan applikasjonen skal kjøres lokalt