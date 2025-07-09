import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = async () => {
  try {
    const driverStandingsPath = join(process.cwd(), 'public/data/driver-standings-2025.json');
    const constructorStandingsPath = join(process.cwd(), 'public/data/constructor-standings-2025.json');
    
    try {
      const driverData = JSON.parse(readFileSync(driverStandingsPath, 'utf-8'));
      const constructorData = JSON.parse(readFileSync(constructorStandingsPath, 'utf-8'));
      
      const combinedData = {
        season: driverData.season,
        last_updated: driverData.last_updated,
        completed_races: driverData.completed_races,
        drivers: driverData.standings,
        constructors: constructorData.standings
      };
      
      return new Response(JSON.stringify(combinedData), {
        status: 200,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=1800' // 30 minutes cache
        }
      });
      
    } catch (fileError) {
      console.log('Standings files not found, returning fallback data');
      const fallbackData = {
        message: 'Dati classifiche non ancora disponibili',
        season: 2025,
        last_updated: new Date().toISOString(),
        completed_races: 0,
        drivers: [],
        constructors: []
      };
      
      return new Response(JSON.stringify(fallbackData), {
        status: 202,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300'
        }
      });
    }
  } catch (error) {
    console.error('Error in standings API:', error);
    return new Response(JSON.stringify({ 
      error: 'Errore interno del server',
      message: 'Impossibile recuperare i dati delle classifiche'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};