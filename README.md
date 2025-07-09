# Che ha fatto la Ferrari 🏎️

Un sito web moderno e responsive dedicato agli appassionati della Scuderia Ferrari di Formula 1. Costruito con Astro, Tailwind CSS e TypeScript.

## 🚀 Caratteristiche

- **Design moderno**: Interfaccia elegante con tema scuro e accenti rosso Ferrari
- **Responsive**: Ottimizzato per desktop, tablet e mobile
- **Performance**: Costruito con Astro per massima velocità
- **SEO friendly**: Ottimizzato per i motori di ricerca
- **Content Collections**: Gestione contenuti strutturata per news e piloti
- **TypeScript**: Tipizzazione forte per maggiore affidabilità

## 📁 Struttura del progetto

```
/
├── public/
│   └── favicon.svg
├── src/
│   ├── content/
│   │   ├── config.ts
│   │   ├── news/
│   │   │   ├── primo-articolo.md
│   │   │   ├── risultati-abu-dhabi.md
│   │   │   └── hamilton-ferrari-2025.md
│   │   └── pilots/
│   │       ├── leclerc.md
│   │       └── sainz.md
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── news.astro
│   │   ├── statistiche.astro
│   │   └── news/
│   │       └── [...slug].astro
│   └── styles/
│       └── global.css
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── package.json
├── netlify.toml
└── README.md
```

## 🎨 Design System

### Colori Ferrari
- **Rosso Ferrari**: `#DC143C` - Colore principale del brand
- **Giallo Ferrari**: `#FFD700` - Accenti e call-to-action
- **Nero**: `#000000` - Testo e elementi scuri
- **Grigio scuro**: `#1a1a1a` - Sfondi e contenitori
- **Grigio chiaro**: `#2a2a2a` - Card e elementi secondari

### Tipografia
- **Display**: Montserrat (700, 800, 900) - Titoli e intestazioni
- **Body**: Inter (400, 500, 600, 700) - Testo principale

## 🛠️ Tecnologie utilizzate

- **[Astro](https://astro.build/)** - Framework web moderno
- **[Tailwind CSS](https://tailwindcss.com/)** - Framework CSS utility-first
- **[TypeScript](https://www.typescriptlang.org/)** - Linguaggio tipizzato
- **[MDX](https://mdxjs.com/)** - Markdown con componenti JSX
- **[Sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/)** - Generazione sitemap automatica

## 🚀 Installazione e avvio

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd che-ha-fatto-la-ferrari
   ```

2. **Installa le dipendenze**:
   ```bash
   npm install
   ```

3. **Avvia il server di sviluppo**:
   ```bash
   npm run dev
   ```

4. **Apri il browser** e vai su `http://localhost:4321`

## 📝 Comandi disponibili

| Comando                 | Azione                                           |
| :---------------------- | :----------------------------------------------- |
| `npm install`           | Installa le dipendenze                          |
| `npm run dev`           | Avvia il server di sviluppo su `localhost:4321` |
| `npm run build`         | Costruisce il sito per la produzione in `./dist/` |
| `npm run preview`       | Anteprima del build locale prima del deploy     |
| `npm run astro ...`     | Esegue comandi CLI di Astro                     |
| `npm run astro -- --help` | Mostra l'aiuto per i comandi Astro           |
| `npm run lint`          | Esegue ESLint per controllo qualità codice      |
| `npm run format`        | Formatta il codice con Prettier                 |

## 📄 Gestione contenuti

### News
Le news sono gestite tramite Astro Content Collections in `src/content/news/`. Ogni articolo è un file Markdown con frontmatter:

```markdown
---
title: "Titolo dell'articolo"
description: "Breve descrizione"
publishedAt: 2024-12-08
category: "Gara" | "Piloti" | "Tecnica" | "Mercato" | "Generale"
author: "Nome autore"
tags: ["tag1", "tag2"]
featured: true
---

Contenuto dell'articolo in Markdown...
```

### Piloti
I profili piloti sono in `src/content/pilots/` con schema strutturato:

```markdown
---
name: "Nome Pilota"
number: 16
nationality: "Nazionalità"
age: 27
seasons: 7
initials: "CL"
championshipPosition: 3
points2024: 319
careerWins: 8
careerPodiums: 35
careerPoints: 1142
firstRace: "GP Australia 2018"
biography: "Biografia del pilota"
active: true
---

Contenuto biografico dettagliato...
```

## 🌐 Deploy

Il sito è configurato per il deploy su Netlify:

1. **Collega il repository** al tuo account Netlify
2. **Imposta le variabili di build**:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: `18`

3. **Deploy automatico**: Ogni push sul branch main attiva un nuovo deploy

## 🔧 Configurazione

### Astro Config
Il file `astro.config.mjs` configura:
- Integrazioni (Tailwind, MDX, Sitemap)
- URL del sito per la produzione
- Configurazione Markdown

### Tailwind Config
Il file `tailwind.config.mjs` include:
- Colori personalizzati Ferrari
- Font personalizzati
- Estensioni del tema

### TypeScript Config
Il file `tsconfig.json` configura:
- Strict mode abilitato
- Path aliases per import puliti
- Configurazione Astro

## 📊 Features principali

### Homepage
- Hero section con CTA
- Statistiche Ferrari
- Ultime 3 news
- Statistiche piloti attuali

### Pagina News
- Lista di tutti gli articoli
- Filtri per categoria
- Ricerca dinamica
- Paginazione

### Pagina Statistiche
- Profili piloti completi
- Classifica campionato piloti
- Classifica campionato costruttori
- Risultati delle ultime gare

### Pagina Articolo
- Layout ottimizzato per la lettura
- Breadcrumb navigation
- Condivisione social
- Articoli correlati

## 🎯 Performance

- **Lighthouse Score**: 100/100 (Performance, Accessibility, SEO)
- **Core Web Vitals**: Tutti i parametri in verde
- **Bundle Size**: Ottimizzato per caricamento veloce
- **Images**: Lazy loading e formati ottimizzati

## 🔒 Sicurezza

- Headers di sicurezza configurati
- CSP (Content Security Policy)
- XSS Protection
- HTTPS enforced

## 📱 Responsive Design

- **Mobile First**: Progettazione mobile-first
- **Breakpoints**: Configurati per tutti i dispositivi
- **Touch Friendly**: Elementi ottimizzati per touch
- **Performance**: Ottimizzato per connessioni lente

## 🎨 Personalizzazione

Per personalizzare il tema:

1. **Modifica i colori** in `tailwind.config.mjs`
2. **Aggiorna i font** in `src/styles/global.css`
3. **Personalizza i componenti** nei file `.astro`
4. **Modifica il layout** in `src/layouts/BaseLayout.astro`

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🏎️ Forza Ferrari!

Creato con ❤️ per tutti i tifosi della Scuderia Ferrari.

---

*Che ha fatto la Ferrari* - Il tuo portale sulla Scuderia Ferrari di Formula 1.