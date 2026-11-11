# Ricerca concorrenti - Punto Cieco

Ricerca del 07/11/2026. 

## Il verdetto in quattro punti

- **Il campo è affollato.** Almeno 20 prodotti confrontano già le notizie per paese, quasi tutti nati nel 2025-2026 con l'AI. Anche il globo 3D esiste (World Monitor, Terra-Orb, news-globe): da solo non ci distingue.
- **Nessuno misura cosa manca all'Italia.** L'unico precedente diretto è Unfiltered.News di Google Jigsaw (2016-2020), chiuso. PRYSM ha un'edizione italiana e Terra-Orb un'interfaccia in italiano, ma nessuno misura i punti ciechi italiani con una regola pubblica.
- **Gli utenti premiano la fiducia:** chi copre cosa, prima i fatti, un'edizione che finisce, fonti a un clic. Se ne vanno per paywall, errori dell'AI senza fonti, contenuti tutti americani, interfacce lente.
- **Nessuno è citabile:** nessun concorrente trovato con DOI o pulsante "Cita". È la leva più economica per l'obiettivo delle citazioni.

## I concorrenti che contano

| Prodotto | Cosa fa | Cosa prendiamo |
|---|---|---|
| The Refract | Confronta decine di paesi, indice di divergenza 0-100, punti ciechi per paese. Solo EN/FR, Premium €4,99 | Cifre paese per paese con estratto, sezione "cosa resta provvisorio", soglia minima di paesi |
| Unfiltered.News (chiuso) | Temi poco coperti in ogni paese, 40 lingue | È il precedente: lo rifacciamo per storie, senza sport, con metodo pubblico e appuntamento quotidiano |
| Terra-Orb | Globo, quanti paesi parlano di una storia, cosa tralasciano gli altri. Gestore non dichiarato, quasi tutto a pagamento | Segnalare chi tace, gratis e con l'Italia al centro |
| Ground News | Barre sinistra/centro/destra e Blindspot con formula pubblica. iOS 4,7 su 49mila voti | Formula pubblica del punto cieco, conteggi veri, "chi l'ha data per primo" |
| Kagi News | Un'edizione al giorno che finisce, fonti citate, dati aperti. Esce alle 12 UTC | Edizione unica ma alle 7 italiane, registro delle correzioni |
| World Monitor | Globo 3D con 59 livelli, 90mila stelle GitHub, AGPL dal 02/2026 | Solo le idee (il codice AGPL ci vincolerebbe). Prestazioni e mobile dal primo giorno |
| news-globe | Globo react-globe.gl, 175 paesi, file statici, MIT | Architettura statica, codice riusabile citando l'autore |
| Internazionale | Riferimento italiano fatto da persone, "Visti dagli altri" | Formato breve quotidiano; possibile partner |

## Le cinque kill feature

1. **K1 I punti ciechi italiani** (v1): storie coperte da almeno N paesi con quota italiana sotto soglia, sport escluso, ordinate per rilevanza per l'Italia.
2. **K2 Il globo con gli occhi italiani** (v1): si accendono i paesi che parlano della storia, l'Italia spenta mostra il punto cieco.
3. **K3 Il prisma** (v1 titoli affiancati e tradotti, v2 nucleo comune dei fatti e racconti per paese).
4. **K4 Attenzione e realtà** (v2): copertura italiana confrontata con vittime, sfollati, disastri, legami con l'Italia. Nessun concorrente lo fa in modo continuo.
5. **K5 L'edizione delle 7** (v1): 5 minuti, finisce, su sito e Telegram, senza account.

Fondamenta v1: classifica con le copie d'agenzia contate una volta, pagina Metodo, scheda testata, ora dell'ultimo aggiornamento, link permanenti, pulsante "Cita" e `CITATION.cff`, niente account né pubblicità.

## Cosa lasciamo fuori

Punteggi destra/sinistra americani, pesi per paese messi a mano, decine di livelli, account e paywall, citazioni o foto generate dall'AI, funzioni social e serie di giorni, Reddit come fonte, tradurre tutto, il codice AGPL di World Monitor.

## Dati per incrociare

GDELT (copertura online per paese), UCDP (vittime dei conflitti, token in 3-5 giorni), UNHCR, GDACS, ReliefWeb, ISTAT e AIRE (legami con l'Italia), ECHO Forgotten Crisis Assessment, INFORM Severity, Wikipedia pageviews. Esclusi ACLED (licenza restrittiva) ed Europe Media Monitor (dati non scaricabili). Dettaglio nella sezione 4 del `docs/architecture.md`.
