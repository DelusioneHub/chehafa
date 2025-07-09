import type { APIRoute } from 'astro';
import { readFileSync } from 'fs';
import { join } from 'path';

export const GET: APIRoute = async () => {
  try {
    const dataPath = join(process.cwd(), 'public/data/next-race.json');
    const data = JSON.parse(readFileSync(dataPath, 'utf-8'));
    
    // Function to get next session
    function getNextSession(raceData: any) {
      const now = new Date();
      const sessionTypes = [
        { key: 'fp1', name: 'FP1', fullName: 'Prove Libere 1' },
        { key: 'fp2', name: 'FP2', fullName: 'Prove Libere 2' },
        { key: 'fp3', name: 'FP3', fullName: 'Prove Libere 3' },
        { key: 'qualifying', name: 'Qualifiche', fullName: 'Qualifiche' },
        { key: 'race', name: 'Gara', fullName: 'Gara' }
      ];
      
      // Check if race has sessions data
      if (!raceData.sessions) {
        return null;
      }
      
      // Find next session
      for (const sessionType of sessionTypes) {
        const sessionDate = raceData.sessions[sessionType.key];
        if (sessionDate) {
          const sessionTime = new Date(sessionDate);
          if (sessionTime > now) {
            return {
              type: sessionType.key,
              name: sessionType.name,
              fullName: sessionType.fullName,
              date: sessionDate,
              event: raceData.name,
              location: raceData.location,
              country: raceData.country,
              circuit: raceData.circuit,
              round: raceData.round
            };
          }
        }
      }
      
      return null;
    }
    
    const nextSession = getNextSession(data);
    
    if (nextSession) {
      return new Response(JSON.stringify(nextSession), {
        status: 200,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300'
        }
      });
    } else {
      // No upcoming session found
      return new Response(JSON.stringify({
        message: 'Nessuna sessione programmata',
        event: null,
        type: null,
        name: null,
        date: null
      }), {
        status: 202,
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=60'
        }
      });
    }
    
  } catch (error) {
    console.error('Error loading next session:', error);
    
    // Fallback data for Belgian GP
    const fallbackSession = {
      type: 'fp1',
      name: 'FP1',
      fullName: 'Prove Libere 1',
      date: '2025-07-25T12:30:00+02:00',
      event: 'Belgian Grand Prix',
      location: 'Spa-Francorchamps',
      country: 'Belgium',
      circuit: 'Circuit de Spa-Francorchamps',
      round: 13
    };
    
    return new Response(JSON.stringify(fallbackSession), {
      status: 202,
      headers: { 
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60'
      }
    });
  }
};