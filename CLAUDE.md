# Yoto-ikoner – instruksjoner for Claude

Øystein bruker PWA-en i dette repoet (https://oysteineliassen.github.io/yoto-ikoner/) til å legge
16×16 pikselikoner på låtene i Yoto-spillelistene sine. Knappen «Bestill ikoner fra Claude» i appen
åpner en ny chat med en bestilling: spilleliste, cardId og låtnummer + tittel for låtene som mangler ikon.

## Når en bestilling kommer
Gjør alt uten å spørre underveis:
1. Få repoet inn i økten (add_repo med push-tilgang, owner `oysteineliassen`, repo `yoto-ikoner`) og klon det.
2. Finn neste ledige sett-id i `sett.json` (`sett-NN`, ett høyere enn det høyeste).
3. Tegn ett ikon per låt i en tekstfil (format: se `verktoy/lag_sett.py`). Filnavn: `NN_Tittel_med_understrek`,
   der NN er låtnummeret fra bestillingen (to sifre). Unngå æøå i filnavn (aa/oe/ae).
4. Kjør `python3 verktoy/lag_sett.py ikoner.txt --id sett-NN --navn "<spilleliste> (låt X–Y)" --cardId <cardId>`.
5. Se på forhåndsvisningen (/tmp/sett-NN.png) og rett ikoner som ikke leses tydelig.
6. Commit og push rett til `main`. Appen finner settet selv (koblet via cardId) og velger det automatisk.
7. Send forhåndsvisningen til Øystein og si kort hva hvert ikon viser. Han trykker «Last opp» i appen selv.

## Stil (samme som Yotos egne ikoner)
- 16×16, gjennomsiktig bakgrunn, flate klare farger, litt mørkere kontur/skygge i samme fargetone, emoji-aktig.
- Motivet skal fylle det meste av ruten og være lett å kjenne igjen på liten skjerm (mørk bakgrunn i Yoto).
- Bruk paletten i `lag_sett.py`. Øyne/detaljer med `k`.
- Velg et konkret, tydelig motiv fra tittelen (jul → juletre, engel → engel, lys → stearinlys, tro → kors osv.).
- Aldri kjente figurer, merkevarer eller logoer (f.eks. ikke Kaptein Sabeltann selv – lag en generisk gjenstand
  fra tittelen i stedet, som skattekiste eller smokk).
- Sett 01 og 02 i `sett/` viser stilen.
