# Yoto-ikoner

Liten nettside som legger 16×16-ikoner på låtene i en Yoto «Make Your Own»-spilleliste via Yotos offisielle API.

- `index.html` – selve siden (logg inn med Yoto, velg spilleliste, velg ikonsett eller egne PNG/ZIP, last opp)
- `sett.json` – liste over ferdige ikonsett
- `sett/<id>/NN_navn.png` – ikonene; `NN` er låtnummeret i spillelisten

Engangsoppsett: lag en *Public* app på https://dashboard.yoto.dev/, legg sidens adresse inn som callback-URL,
huk av `user:content:manage` og `offline_access`, og lim Client ID inn på siden.
