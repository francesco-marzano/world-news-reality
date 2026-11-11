# World News Reality

[![ci](https://github.com/francesco-marzano/world-news-reality/actions/workflows/ci.yml/badge.svg)](https://github.com/francesco-marzano/world-news-reality/actions/workflows/ci.yml)

**Italiano** · [English](#english)

Un sito gratuito e open source che misura quali storie racconta il mondo e quali mancano
nei media italiani.

Ogni 30 minuti una pipeline legge i titoli di circa 100 testate in 30 paesi, raggruppa gli
articoli che parlano dello stesso fatto anche se sono in lingue diverse, e conta quanti
paesi ne parlano. Una storia è un «punto cieco» quando molti paesi la raccontano e in Italia
quasi nessuna testata. Formule, parametri e dati sono pubblici: chiunque può rifare il conto
e citarlo.

## Stato

Il progetto è all'inizio. Oggi nel repository ci sono:

- il progetto completo: [brief](PROJECT_BRIEF.md) e [documento tecnico](docs/architecture.md);
- l'impalcatura del codice, con controlli automatici e test;
- le [decisioni prese finora](docs/decisions/).

Il sito non pubblica ancora dati. Il piano è diviso in 13 passi, da M0 a M12, descritti nel
brief. Il passo in corso è scritto in [TASKS.md](TASKS.md).

## Provarlo

Servono [uv](https://docs.astral.sh/uv/), Node.js 22 o più recente con
[pnpm](https://pnpm.io/), e [just](https://just.systems/).

```sh
just setup     # installa le dipendenze
just check     # lint, tipi e test, senza rete
just verify    # check, più la build del sito
```

## Come è fatto

| Cartella | Cosa contiene |
|---|---|
| `pipeline/` | Il pacchetto Python `world_news_reality` e il comando `wnr` |
| `web/` | Il sito, fatto con Astro e TypeScript |
| `config/` | I parametri del metodo, in chiaro |
| `schemas/` | Gli schemi dei dati, generati dai modelli |
| `docs/` | Documento tecnico, ricerche e decisioni |

## Sviluppo con assistenti AI

Il progetto si sviluppa insieme ad assistenti AI di coding. Le regole che seguono sono in
[AGENTS.md](AGENTS.md): cosa possono fare da soli, cosa richiede un'approvazione e quale
comando dimostra che un lavoro è finito. Ogni pull request riceve un livello di rischio
calcolato dai file che tocca.

## Licenze

Il codice è sotto [Apache-2.0](LICENSE). I dati pubblicati dal progetto sono sotto
[CC BY 4.0](DATA_LICENSE). Per citare il progetto usa [CITATION.cff](CITATION.cff).

---

## English

A free, open-source website that measures which stories the world's media cover and which
ones Italian media leave out.

Every 30 minutes a pipeline reads headlines from about 100 outlets in 30 countries, groups
articles about the same event across languages, and counts how many countries cover each
story. A story is a "blind spot" when many countries report it and almost no Italian outlet
does. Formulas, parameters and data are public, so anyone can redo the count and cite it.

### Status

Early. The repository holds the full design ([brief](PROJECT_BRIEF.md),
[technical design](docs/architecture.md) in Italian), the code scaffold with automated
checks and tests, and the [decisions taken so far](docs/decisions/). The site does not
publish data yet. The plan has 13 steps, M0 to M12, described in the brief. The current
step is in [TASKS.md](TASKS.md).

### Try it

You need [uv](https://docs.astral.sh/uv/), Node.js 22 or newer with
[pnpm](https://pnpm.io/), and [just](https://just.systems/).

```sh
just setup     # install dependencies
just check     # lint, types and tests, no network
just verify    # check, plus the site build
```

### Working with AI assistants

The project is built together with AI coding assistants. Their rules are in
[AGENTS.md](AGENTS.md): what they may do alone, what needs approval, and which command
proves a change is done. Every pull request gets a risk level computed from the files it
touches.

### Licences

Code is under [Apache-2.0](LICENSE). Data published by the project is under
[CC BY 4.0](DATA_LICENSE). To cite the project, use [CITATION.cff](CITATION.cff).
