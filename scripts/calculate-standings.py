#!/usr/bin/env python3
"""
Calculate 2025 F1 Championship Standings using FastF1
Generates both driver and constructor standings from race results
"""

import fastf1
import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable FastF1 cache
cache_dir = Path('cache')
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

def get_completed_races(year=2025):
    """Get list of completed races for the season"""
    try:
        schedule = fastf1.get_event_schedule(year)
        now = datetime.now(timezone.utc)
        
        completed_races = []
        for _, event in schedule.iterrows():
            # Check if race date has passed
            race_date = event.get('Session5Date')  # Session 5 is usually the race
            if race_date and pd.to_datetime(race_date, utc=True) < now:
                completed_races.append({
                    'round': event['RoundNumber'],
                    'name': event['EventName'],
                    'location': event['Location'],
                    'date': race_date
                })
        
        return completed_races
    except Exception as e:
        logger.error(f"Error getting schedule: {e}")
        return []

def get_race_results(year, round_number):
    """Get race results for a specific round"""
    try:
        # Try to get main race results
        session = fastf1.get_session(year, round_number, 'Race')
        session.load()
        
        results = []
        if session.results is not None and len(session.results) > 0:
            for _, driver in session.results.iterrows():
                results.append({
                    'driver_number': int(driver['DriverNumber']),
                    'full_name': driver['FullName'],
                    'team_name': driver['TeamName'],
                    'position': int(driver['Position']) if pd.notna(driver['Position']) else None,
                    'points': int(driver['Points']) if pd.notna(driver['Points']) else 0,
                    'status': driver.get('Status', 'Unknown')
                })
        
        return results
    except Exception as e:
        logger.error(f"Error getting race results for round {round_number}: {e}")
        return []

def get_sprint_results(year, round_number):
    """Get sprint results if available"""
    try:
        session = fastf1.get_session(year, round_number, 'Sprint')
        session.load()
        
        results = []
        if session.results is not None and len(session.results) > 0:
            for _, driver in session.results.iterrows():
                results.append({
                    'driver_number': int(driver['DriverNumber']),
                    'full_name': driver['FullName'],
                    'team_name': driver['TeamName'],
                    'position': int(driver['Position']) if pd.notna(driver['Position']) else None,
                    'points': int(driver['Points']) if pd.notna(driver['Points']) else 0,
                    'status': driver.get('Status', 'Unknown')
                })
        
        return results
    except Exception as e:
        logger.info(f"No sprint session for round {round_number}")
        return []

def calculate_driver_standings(year=2025):
    """Calculate driver championship standings"""
    logger.info(f"Calculating driver standings for {year}")
    
    completed_races = get_completed_races(year)
    logger.info(f"Found {len(completed_races)} completed races")
    
    # Initialize driver totals
    driver_totals = {}
    race_details = []
    
    for race in completed_races:
        logger.info(f"Processing {race['name']} (Round {race['round']})")
        
        # Get main race results
        race_results = get_race_results(year, race['round'])
        
        # Get sprint results if available
        sprint_results = get_sprint_results(year, race['round'])
        
        # Process race results
        for driver in race_results:
            driver_num = driver['driver_number']
            if driver_num not in driver_totals:
                driver_totals[driver_num] = {
                    'driver_number': driver_num,
                    'full_name': driver['full_name'],
                    'team_name': driver['team_name'],
                    'total_points': 0,
                    'wins': 0,
                    'podiums': 0,
                    'races_completed': 0
                }
            
            # Add race points
            driver_totals[driver_num]['total_points'] += driver['points']
            driver_totals[driver_num]['races_completed'] += 1
            
            # Count wins and podiums
            if driver['position'] == 1:
                driver_totals[driver_num]['wins'] += 1
            if driver['position'] and driver['position'] <= 3:
                driver_totals[driver_num]['podiums'] += 1
        
        # Process sprint results
        for driver in sprint_results:
            driver_num = driver['driver_number']
            if driver_num in driver_totals:
                driver_totals[driver_num]['total_points'] += driver['points']
        
        race_details.append({
            'round': race['round'],
            'name': race['name'],
            'location': race['location'],
            'date': race['date'],
            'race_results': race_results,
            'sprint_results': sprint_results
        })
    
    # Sort by points (descending), then by wins, then by podiums
    standings = sorted(
        driver_totals.values(),
        key=lambda x: (x['total_points'], x['wins'], x['podiums']),
        reverse=True
    )
    
    # Add positions
    for i, driver in enumerate(standings):
        driver['position'] = i + 1
    
    return {
        'season': year,
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'completed_races': len(completed_races),
        'standings': standings,
        'race_details': race_details
    }

def calculate_constructor_standings(driver_standings_data):
    """Calculate constructor championship standings from driver data"""
    logger.info("Calculating constructor standings")
    
    constructor_totals = {}
    
    # Aggregate points by team
    for driver in driver_standings_data['standings']:
        team_name = driver['team_name']
        if team_name not in constructor_totals:
            constructor_totals[team_name] = {
                'team_name': team_name,
                'total_points': 0,
                'wins': 0,
                'podiums': 0,
                'drivers': []
            }
        
        constructor_totals[team_name]['total_points'] += driver['total_points']
        constructor_totals[team_name]['wins'] += driver['wins']
        constructor_totals[team_name]['podiums'] += driver['podiums']
        constructor_totals[team_name]['drivers'].append({
            'driver_number': driver['driver_number'],
            'full_name': driver['full_name'],
            'points': driver['total_points']
        })
    
    # Sort by total points
    standings = sorted(
        constructor_totals.values(),
        key=lambda x: (x['total_points'], x['wins'], x['podiums']),
        reverse=True
    )
    
    # Add positions
    for i, constructor in enumerate(standings):
        constructor['position'] = i + 1
    
    return {
        'season': driver_standings_data['season'],
        'last_updated': driver_standings_data['last_updated'],
        'completed_races': driver_standings_data['completed_races'],
        'standings': standings
    }

def main():
    """Main function to calculate and display standings"""
    try:
        # Calculate driver standings
        driver_standings = calculate_driver_standings(2025)
        
        # Calculate constructor standings
        constructor_standings = calculate_constructor_standings(driver_standings)
        
        # Print results
        print("\n" + "="*60)
        print("🏆 CLASSIFICA PILOTI 2025")
        print("="*60)
        print(f"Gare completate: {driver_standings['completed_races']}")
        print(f"Ultimo aggiornamento: {driver_standings['last_updated']}")
        print("-"*60)
        
        for driver in driver_standings['standings']:
            print(f"{driver['position']:2d}. {driver['full_name']:<25} {driver['team_name']:<15} {driver['total_points']:3d} pts (W:{driver['wins']}, P:{driver['podiums']})")
        
        print("\n" + "="*60)
        print("🏆 CLASSIFICA COSTRUTTORI 2025")
        print("="*60)
        print(f"Gare completate: {constructor_standings['completed_races']}")
        print("-"*60)
        
        for constructor in constructor_standings['standings']:
            print(f"{constructor['position']:2d}. {constructor['team_name']:<25} {constructor['total_points']:3d} pts (W:{constructor['wins']}, P:{constructor['podiums']})")
        
        # Save to files
        output_dir = Path('public/data')
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / 'driver-standings-2025.json', 'w') as f:
            json.dump(driver_standings, f, indent=2, default=str)
        
        with open(output_dir / 'constructor-standings-2025.json', 'w') as f:
            json.dump(constructor_standings, f, indent=2, default=str)
        
        print(f"\n✅ Standings saved to public/data/")
        
    except Exception as e:
        logger.error(f"Error calculating standings: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)