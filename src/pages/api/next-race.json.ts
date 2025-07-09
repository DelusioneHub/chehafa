import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = async () => {
  try {
    const dataPath = join(process.cwd(), 'public/data/next-race.json');
    const data = JSON.parse(readFileSync(dataPath, 'utf-8'));
    
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300'
      }
    });
  } catch (error) {
    const fallbackData = {
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
    
    return new Response(JSON.stringify(fallbackData), {
      status: 202,
      headers: { 
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60'
      }
    });
  }
};