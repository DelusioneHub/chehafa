# 🏎️ Sistema FastF1 - Ferrari F1 Website

Sistema completamente dinamico basato su **DATI REALI** FastF1. Zero dati fittizi.

## ✅ SISTEMA IMPLEMENTATO

### **STRUTTURA DATI REALI**
```
public/data/
├── current-season.json      # Classifica attuale 2025
├── latest-session.json      # Ultima gara/qualifiche
├── next-race.json          # Prossima gara
├── drivers/
│   ├── driver_16.json      # Charles Leclerc
│   └── driver_44.json      # Lewis Hamilton
├── races/
│   └── race_01_*.json      # Risultati gare 2025
└── archive/
    └── 2024.json           # Archivio stagione passata
```

### **SCRIPT PYTHON**
- `scripts/update-data.py` - Script principale FastF1
- `scripts/cache_manager.py` - Sistema di cache intelligente
- Gestione errori completa
- Logging dettagliato
- Retry automatico

### **API ENDPOINTS**
- `/api/f1-data?type=current-season` - Classifiche 2025
- `/api/f1-data?type=latest-session` - Ultima sessione
- `/api/f1-data?type=next-race` - Prossima gara
- `/api/f1-data?type=driver&driver_id=16` - Profilo pilota
- `/api/f1-data?type=archive&year=2024` - Archivio

### **PAGINE DINAMICHE**
- ✅ Homepage: mostra "Dati non ancora disponibili" se FastF1 non ha dati
- ✅ Statistiche: tutto da API reali
- ✅ Piloti: profili con dati live FastF1
- ✅ Zero fallback fittizi

## 🚀 COMANDI DISPONIBILI

```bash
# Aggiorna dati manualmente
npm run update-data

# Sviluppo con dati aggiornati
npm run dev-with-data

# Build con dati aggiornati
npm run build-with-data

# Solo sviluppo
npm run dev
```

## ⚡ AUTOMAZIONE

### **GitHub Actions**
- Aggiorna dati ogni ora nei weekend di gara
- Ogni 6 ore negli altri giorni
- Build automatico quando i dati cambiano
- Deploy automatico su Netlify

### **Cache Intelligente**
- Schedule F1: aggiornato 1 volta al giorno
- Sessioni: ogni 5 min nei weekend, ogni ora altrimenti
- Classifiche: ogni 30 min nei weekend, ogni 2 ore altrimenti
- Pulizia automatica cache vecchia

### **Gestione Errori**
- Retry automatico con backoff
- Fallback graceful se FastF1 non disponibile
- Log dettagliati per debug
- Stato HTTP 202 per "dati non ancora disponibili"

## 📊 COMPORTAMENTO REALE

### **Quando FastF1 ha dati:**
- Homepage mostra risultati reali
- Classifiche aggiornate
- Countdown per prossima gara
- Risultati delle sessioni

### **Quando FastF1 NON ha dati:**
- "Dati non ancora disponibili"
- "Nessuna sessione completata disponibile"
- "Classifiche non ancora disponibili"
- **MAI numeri inventati**

## 🔧 CONFIGURAZIONE

### **Variabili Ambiente**
```bash
NETLIFY_AUTH_TOKEN=your_token    # Per deploy automatico
NETLIFY_SITE_ID=your_site_id     # ID sito Netlify
```

### **Dipendenze Python**
```bash
pip install fastf1 pandas
```

## 📈 MONITORAGGIO

### **Log Files**
- `logs/data_update.log` - Log aggiornamenti
- Cache stats nei log
- Errori tracciati completamente

### **Cache Stats**
- Numero file cache
- Dimensione cache
- Ultimo aggiornamento per tipo di dato
- Statistiche performance

## 🎯 CARATTERISTICHE CHIAVE

1. **100% Dati Reali**: Solo FastF1, zero inventati
2. **Gestione Mancanza Dati**: Messaggi chiari quando non disponibili
3. **Cache Ottimizzata**: Riduce chiamate API FastF1
4. **Automazione Completa**: GitHub Actions + deploy automatico
5. **Error Resilience**: Sistema continua a funzionare anche con problemi
6. **Performance**: Cache intelligente per velocità
7. **Logging**: Tracciamento completo per debug

## 🚨 IMPORTANTE

- Il sito mostra **SOLO** dati reali da FastF1
- Se una sessione non è ancora disponibile: "Dati non ancora disponibili"
- Se FastF1 è down: il sito continua con gli ultimi dati cached
- **Zero numeri fittizi** in qualsiasi circostanza

Il sistema è progettato per essere completamente trasparente: se non ci sono dati reali, lo dice chiaramente.