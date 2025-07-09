import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = async () => {
  try {
    const dataPath = join(process.cwd(), 'public/data/latest-session.json');
    
    try {
      const data = JSON.parse(readFileSync(dataPath, 'utf-8'));
      
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300' // 5 minutes cache
        }
      });
      
    } catch (fileError) {
      console.log('Latest session file not found, returning fallback data');
      const fallbackData = {
        message: 'Dati ultima sessione non ancora disponibili',
        event: null,
        location: null,
        country: null,
        round: null,
        session_type: null,
        date: null,
        results: [],
        total_drivers: 0
      };
      
      return new Response(JSON.stringify(fallbackData), {
        status: 202,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=60'
        }
      });
    }
  } catch (error) {
    console.error('Error in latest session API:', error);
    return new Response(JSON.stringify({ 
      error: 'Errore interno del server',
      message: 'Impossibile recuperare i dati dell\'ultima sessione'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};