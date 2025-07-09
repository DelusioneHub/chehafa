import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = async ({ url }) => {
  try {
    const searchParams = new URLSearchParams(url.search);
    const type = searchParams.get('type') || 'latest-session';
    
    // Debug: force next-race if we detect it in URL
    if (url.toString().includes('type=next-race')) {
      console.log('🚀 FORCING next-race type');
      const dataPath = join(process.cwd(), 'public/data/next-race.json');
      try {
        const data = JSON.parse(readFileSync(dataPath, 'utf-8'));
        return new Response(JSON.stringify(data), {
          status: 200,
          headers: { 
            'Content-Type': 'application/json',
            'Cache-Control': 'public, max-age=300'
          }
        });
      } catch (error) {
        console.error('Error reading next-race.json:', error);
      }
    }
    const driverId = searchParams.get('driver_id');
    const raceId = searchParams.get('race_id');
    
    let dataPath: string;
    let fallbackData: any;
    
    switch (type) {
      case 'latest-session':
        dataPath = join(process.cwd(), 'public/data/latest-session.json');
        fallbackData = {
          message: 'Dati non ancora disponibili',
          event: null,
          results: []
        };
        break;
        
      case 'next-race':
        dataPath = join(process.cwd(), 'public/data/next-race.json');
        fallbackData = {
          name: "Belgian Grand Prix",
          location: "Spa-Francorchamps",
          country: "Belgium", 
          date: "2025-07-27T15:00:00+02:00",
          circuit: "Circuit de Spa-Francorchamps",
          round: 13,
          sessions: {
            fp1: "2025-07-25T12:30:00+02:00",
            fp2: "2025-07-25T16:30:00+02:00", 
            fp3: "2025-07-26T12:00:00+02:00",
            qualifying: "2025-07-26T16:00:00+02:00",
            race: "2025-07-27T15:00:00+02:00"
          }
        };
        break;
        
      case 'current-season':
        dataPath = join(process.cwd(), 'public/data/current-season.json');
        fallbackData = {
          season: new Date().getFullYear(),
          message: 'Classifiche non ancora disponibili',
          drivers: [],
          constructor: {
            team: 'Ferrari',
            points: 0,
            position: null
          }
        };
        break;
        
      case 'driver':
        if (!driverId) {
          return new Response(JSON.stringify({ error: 'Driver ID richiesto' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        dataPath = join(process.cwd(), `public/data/drivers/driver_${driverId}.json`);
        fallbackData = {
          message: 'Dati pilota non ancora disponibili',
          driver_number: parseInt(driverId),
          name: driverId === '16' ? 'Charles Leclerc' : 'Lewis Hamilton',
          current_season: {
            points: 0,
            position: null,
            wins: 0,
            podiums: 0
          }
        };
        break;
        
      case 'race':
        if (!raceId) {
          return new Response(JSON.stringify({ error: 'Race ID richiesto' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        dataPath = join(process.cwd(), `public/data/races/${raceId}.json`);
        fallbackData = {
          message: 'Risultati gara non ancora disponibili',
          event: null,
          results: []
        };
        break;
        
      case 'archive':
        const year = searchParams.get('year') || '2024';
        dataPath = join(process.cwd(), `public/data/archive/${year}.json`);
        fallbackData = {
          season: parseInt(year),
          message: 'Archivio non ancora disponibile',
          final_standings: {
            drivers: [],
            constructor: null
          }
        };
        break;
        
      default:
        return new Response(JSON.stringify({ error: 'Tipo di dati non valido' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
    }
    
    try {
      const data = JSON.parse(readFileSync(dataPath, 'utf-8'));
      
      // Check if data has an error message and return appropriate status
      if (data.message && data.message.includes('non disponibile')) {
        return new Response(JSON.stringify(data), {
          status: 202, // Accepted but not complete
          headers: { 
            'Content-Type': 'application/json',
            'Cache-Control': 'public, max-age=60' // Short cache for unavailable data
          }
        });
      }
      
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300' // 5 minutes cache
        }
      });
      
    } catch (fileError) {
      console.log(`File not found for ${type}, returning fallback data`);
      return new Response(JSON.stringify(fallbackData), {
        status: 202, // Accepted but data not available yet
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=60'
        }
      });
    }
  } catch (error) {
    console.error('Error in F1 data API:', error);
    return new Response(JSON.stringify({ 
      error: 'Errore interno del server',
      message: 'Impossibile recuperare i dati al momento'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};