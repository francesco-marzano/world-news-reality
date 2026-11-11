# Ricerca SEO e GEO - Punto Cieco

Dati DataForSEO presi il 07/11/2026, Italia, lingua italiana. Volumi: medie mensili Google Ads. La strategia completa è la sezione 19 del `docs/architecture.md`.

## Cosa cerca la gente

| Gruppo | Ricerche e volume al mese | Difficoltà | Per noi |
|---|---|---|---|
| Notizie dal mondo | notizie dal mondo 33.100 (74.000 a marzo 2026) · ultime notizie dal mondo 8.100 · notizie dal mondo oggi 5.400 · notizie esteri 1.000 · notizie internazionali 880 | 100 | Fuori portata: Sky TG24, La Stampa, ANSA, Euronews, Tgcom24 |
| Cosa succede nel mondo | 2.900, picco 18.100 a marzo 2026 | n.d. | È la promessa della home |
| Guerre nel mondo | guerre nel mondo 3.600 · guerre nel mondo oggi 2.900 · quante guerre ci sono nel mondo 2.900 · guerre nel mondo oggi mappa 880 · mappa guerre nel mondo 2026 320 | 2-10 | Il gruppo più promettente, ma per contare le guerre serve UCDP: pagina nella v2 |
| Crisi dimenticate | guerre dimenticate 70 · crisi umanitarie nel mondo 30 · crisi dimenticate 10 | n.d. | Poche ricerche, fatte da chi poi cita (giornalisti, ONG, scuole). Pagina "Crisi dimenticate" nella v1.1 con i dati ECHO |
| Stampa estera | stampa estera 320 · giornali stranieri 170 · rassegna stampa estera 50 | n.d. | Vicine alla pagina Storia |

Nessun dato per "notizie ignorate", "mappa delle notizie", "mappa notizie mondo".

## Chi occupa le SERP (07/11)

- **"crisi dimenticate":** AI Overview presente. Caritas Verona, Osservatorio di Pavia (rapporto MSF), Corriere 2009, Linkiesta, Treccani, ACLI, PassaParola.
- **"guerre in corso nel mondo":** l'AI Overview cita Oxfam Italia, Geopop, Wikipedia (categoria conflitti in corso), Rai Cultura. Organici: Vatican News, Valori.it "Atlante delle guerre 2026", Truenumbers. Ricerche correlate: "guerre nel mondo oggi mappa", "guerre sconosciute nel mondo".

## Strategia decisa nel documento

- Google dice che per AI Overviews e AI Mode valgono le regole della SEO normale: niente file speciali. Per noi GEO vuol dire frasi e numeri facili da citare, con fonte e data.
- **Indicizzazione prudente al lancio:** solo punti ciechi confermati e pagine Giorno, Paese, Metodo, Dati; il resto `noindex` finché non regge la qualità, per evitare l'abuso di contenuti in scala.
- Dati strutturati: `Dataset` per la pagina Dati (serve a Google Dataset Search), `Organization` con `sameAs` verso GitHub e Zenodo, `BreadcrumbList`, `CollectionPage` con `ItemList`. Niente `NewsArticle` sui titoli degli altri.
- Sitemap con `lastmod` solo sui cambi sostanziali, IndexNow (Bing, che alimenta Copilot), `llms.txt` generato in build perché costa poco.
- **Bot AI:** ammessi anche quelli di addestramento (D13, raccomandato), perché l'obiettivo è essere citati e i dati sono già CC BY. Da rivedere quando arriverà la regola comune annunciata a fine ottobre 2026 (Google dal 2027).
- **Misure:** Search Console con il report sull'AI generativa, Bing Webmaster con AI Performance, DataForSEO LLM mentions su ChatGPT e Google. Al 07/11 il database LLM Mentions non ha restituito dati per le nostre parole chiave in italiano.
