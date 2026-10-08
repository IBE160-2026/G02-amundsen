# Product Brief: Career Transition Assistant

## Executive Summary

Career Transition Assistant er en KI-basert jobbsøknadsassistent for studenter, nyutdannede og unge yrkesaktive med begrenset arbeidserfaring. Løsningen skal hjelpe brukeren med å forstå hvilke deler av egen utdanning, erfaring og kompetanse som er mest relevante for en konkret stilling, og hvordan dette kan presenteres tydeligere i CV og søknad.

Behovet oppstår fordi mange unge kandidater har relevant kompetanse, men synes det er vanskelig å koble denne til kravene i stillingsannonser og konkurrere mot søkere med lengre yrkeserfaring. Samtidig er individuell tilpasning av søknader tidkrevende, mens generelle KI-verktøy kan produsere tekster som fremstår standardiserte, generiske eller lite personlige.

Ved å analysere CV og en konkret stillingsannonse skal applikasjonen kunne identifisere relevante styrker og kompetansegap, foreslå tilpasninger i CV-en og generere et førsteutkast til søknadsbrev. Målet er å gjøre jobbsøkingen mer målrettet og effektiv uten at brukeren mister kontroll over eget innhold eller personlige uttrykk.

## The Problem

Unge og nyutdannede møter ofte et arbeidsmarked der stillingsannonser etterspør erfaring og kompetanse som kan være vanskelig å koble til det de faktisk har fra utdanning, deltidsarbeid, praksis, verv og andre erfaringer. Selv når kandidaten har relevant bakgrunn, kan det være krevende å identifisere hvilke erfaringer som er viktigst for en konkret stilling og hvordan disse bør fremheves i CV og søknad.

Samtidig er jobbsøking tidkrevende når hver søknad skal tilpasses individuelt. KI-verktøy kan effektivisere denne prosessen, men genererte tekster kan bli generiske, standardiserte eller lite personlige dersom de ikke tar utgangspunkt i brukerens faktiske erfaringer og skrivestil. Dette skaper et dilemma mellom effektivitet og autentisitet.

Konsekvensen kan være at unge kandidater bruker unødvendig mye tid på hver søknad, sender lite målrettede søknader eller underselger relevant kompetanse. For kandidater med begrenset yrkeserfaring kan dette gjøre det vanskeligere å synliggjøre den kompetansen de faktisk har.

## The Solution

Løsningen er en KI-basert jobbsøknadsassistent for studenter i avsluttende fase av bachelor- eller masterstudium som søker sin første faste jobb. Brukeren limer inn CV-en sin og en konkret stillingsannonse som tekst i applikasjonen.

Applikasjonen analyserer hvordan brukerens bakgrunn samsvarer med kravene i stillingsannonsen. Resultatet presenteres som relevante styrker, eventuelle kompetansegap og konkrete forslag til hvordan CV-en kan tilpasses stillingen. På bakgrunn av informasjonen brukeren selv har lagt inn, genererer løsningen også et førsteutkast til et tilpasset søknadsbrev som brukeren kan redigere videre.

For de viktigste forslagene skal brukeren kunne se hvilken del av CV-en og stillingsannonsen forslaget bygger på. Løsningen skal ikke finne på kvalifikasjoner eller erfaringer som ikke finnes i brukerens input.

Første versjon skal kunne brukes uten innlogging og uten at CV, stillingsannonse, analyse eller søknadsutkast lagres. Applikasjonen skal også ha en demomodus med ferdige eksempeldata slik at løsningen kan testes uten egen API-nøkkel.

Målet er å gjøre det enklere for brukeren å forstå og presentere egen kompetanse på en mer målrettet måte, samtidig som brukeren beholder kontroll over innholdet og det personlige uttrykket.

## What Makes This Different

Løsningen skiller seg fra generelle KI-verktøy ved at den er bygget rundt en fast arbeidsflyt for jobbsøking, der brukerens CV sammenlignes direkte med kravene i én konkret stillingsannonse.

I stedet for kun å generere tekst skal applikasjonen først identifisere relevante styrker og kompetansegap, og deretter bruke denne analysen til å foreslå konkrete CV-endringer og generere et tilpasset søknadsutkast.

For de viktigste forslagene skal brukeren kunne se hvilken del av CV-en og hvilken del av stillingsannonsen forslaget bygger på. Dette gjør det enklere å kontrollere at forslagene faktisk er forankret i brukerens egne erfaringer og ikke inneholder oppdiktede kvalifikasjoner.

Målet er dermed ikke bare å generere en søknad, men å gi brukeren en mer strukturert og etterprøvbar prosess for å forstå og presentere egen kompetanse.

## Who This Serves

Primærbrukeren er en student i avsluttende fase av et bachelor- eller masterstudium som søker sin første faste jobb og har begrenset relevant arbeidserfaring.. Brukeren kan ha erfaring fra deltidsarbeid, praksis, verv, prosjektarbeid eller andre aktiviteter, men være usikker på hvilke deler av denne bakgrunnen som er mest relevante for en konkret stilling og hvordan de bør presenteres.

Denne brukeren kan ha relevant bakgrunn, men være usikker på hvilke deler som bør fremheves, hvordan de bør formulere seg, og hvordan de kan konkurrere mot kandidater med lengre yrkeserfaring. For brukeren betyr suksess at det blir enklere å identifisere relevant kompetanse, lage mer målrettede søknader og presentere seg på en måte som oppleves både profesjonell og personlig.

Sekundære brukere kan være nyutdannede og personer tidlig i karrieren som ønsker å bytte retning og trenger hjelp til å oversette eksisterende kompetanse til nye typer stillinger.

## Success Criteria

Første versjon regnes som vellykket dersom brukeren kan:

- lime inn CV og en konkret stillingsannonse som tekst
- få identifisert relevante styrker som faktisk kan spores tilbake til CV-en
- få identifisert tydelige kompetansegap opp mot krav i stillingsannonsen
- få konkrete forslag til hvordan CV-en kan tilpasses stillingen
- få et førsteutkast til et tilpasset søknadsbrev
- se hvilken del av CV-en og stillingsannonsen de viktigste forslagene bygger på
- få resultater som ikke inneholder kvalifikasjoner eller erfaringer som ikke finnes i brukerens input
- gjennomføre hele arbeidsflyten uten innlogging eller lagring av personopplysninger
- bruke en demomodus med ferdige eksempeldata uten egen API-nøkkel

## Scope

### In for v1

Første versjon skal gjøre det mulig for brukeren å:

- lime inn CV som tekst
- lime inn en konkret stillingsannonse som tekst
- få en analyse av hvordan egen bakgrunn matcher kravene i stillingen
- få fremhevet relevante styrker og eventuelle kompetansegap
- få konkrete forslag til hvordan CV-en kan tilpasses stillingen
- få et førsteutkast til et tilpasset søknadsbrev
- se hvilken del av CV-en og stillingsannonsen de viktigste forslagene bygger på
- bruke løsningen uten innlogging eller lagring av personopplysninger
- bruke en demomodus med ferdige eksempeldata uten egen API-nøkkel

### Out for v1

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

## Technical Assumptions

Første versjon skal bruke én ekstern språkmodell gjennom et API for analyse av CV og stillingsannonse, samt generering av forslag og søknadsutkast.

API-nøkkelen skal lagres lokalt i en `.env`-fil og skal ikke pushes til GitHub. En `.env.example`-fil skal vise hvilke variabler som kreves.

Siden språkmodellkall kan koste penger, skal løsningen også ha en demomodus med ferdige eksempeldata og eksempelresultater slik at sensor kan teste hovedflyten uten egen API-nøkkel eller kostnad.

Endelig valg av språkmodell og API bestemmes i arkitekturfasen.

## Vision

På sikt kan løsningen utvikles fra en jobbsøknadsassistent til en bredere karriereplattform for studenter, nyutdannede og personer tidlig i karrieren. Plattformen kan bygge en mer helhetlig kompetanseprofil over tid basert på utdanning, arbeidserfaring, attester, vurderinger og tidligere søknader.

Løsningen kan videre hjelpe brukeren med å sammenligne ulike stillinger, identifisere hvilke ferdigheter som går igjen i jobbmarkedet og foreslå hvilke kompetanser som kan være nyttige å utvikle videre. Den kan også gi støtte gjennom flere deler av jobbsøkingsprosessen, som intervjuforberedelser, oppfølging av søknader og langsiktig karriereplanlegging.

Målet er at produktet over tid skal bli et personlig karriereverktøy som hjelper brukeren med å forstå, utvikle og kommunisere egen kompetanse gjennom ulike faser av studier og arbeidsliv.