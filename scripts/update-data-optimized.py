#!/usr/bin/env python3
"""
Optimized F1 Data Updater - FastF1 only for latest session
Standings from reliable sources, session data from FastF1
"""

import fastf1
import json
import os
import logging
from datetime import datetime, timedelta, timezone
import pandas as pd
from pathlib import Path
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_update_optimized.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Enable minimal FastF1 cache for latest session only
cache_dir = Path('.cache')
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

# Data directory setup
public_data_dir = Path('public/data')
public_data_dir.mkdir(exist_ok=True)

def normalize_datetime(dt):
    """Normalize datetime to timezone-aware UTC"""
    if dt is None:
        return None
    if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        return dt.astimezone(timezone.utc)
    return dt

def format_f1_time(time_obj):
    """Format time object to F1 style (e.g., '1:26.296')"""
    if pd.isna(time_obj) or time_obj is None:
        return None
    
    try:
        # Convert to string and parse timedelta format
        time_str = str(time_obj)
        if '0 days' in time_str:
            time_str = time_str.replace('0 days ', '')
        
        # Extract minutes, seconds, and milliseconds
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) >= 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds_ms = float(parts[2])
                
                total_minutes = hours * 60 + minutes
                seconds = int(seconds_ms)
                milliseconds = int((seconds_ms - seconds) * 1000)
                
                return f"{total_minutes}:{seconds:02d}.{milliseconds:03d}"
        
        return time_str
    except:
        return None

def fetch_latest_session():
    """Fetch only the latest session data using FastF1"""
    try:
        logger.info("🏁 Fetching latest session with FastF1...")
        
        # Get current year and try to find the latest completed session
        current_year = datetime.now().year
        schedule = fastf1.get_event_schedule(current_year)
        
        now = datetime.now(timezone.utc)
        latest_session = None
        
        # Find the most recent completed session
        for _, event in schedule.iterrows():
            event_date = normalize_datetime(event['Session5Date'])
            if event_date and event_date < now:
                # Check if this is more recent than our current latest
                if latest_session is None or event_date > latest_session['date']:
                    latest_session = {
                        'event': event,
                        'date': event_date
                    }
        
        if not latest_session:
            logger.warning("No completed sessions found")
            return None
            
        event = latest_session['event']
        logger.info(f"Latest session: {event['EventName']} - {event['Location']}")
        
        # Try to load race session first, then qualifying
        session_types = ['R', 'Q']  # Race, Qualifying
        session_data = None
        
        for session_type in session_types:
            try:
                logger.info(f"Attempting to load {session_type} session for {event['EventName']}")
                session = fastf1.get_session(current_year, event['RoundNumber'], session_type)
                session.load()
                
                if session.results is not None and len(session.results) > 0:
                    session_data = session
                    break
                    
            except Exception as e:
                logger.warning(f"Could not load {session_type} session: {e}")
                continue
        
        if not session_data:
            logger.error("No session data available")
            return None
            
        # Filter for Ferrari drivers only
        ferrari_results = session_data.results[session_data.results['TeamName'] == 'Ferrari']
        
        if ferrari_results.empty:
            logger.warning("No Ferrari results found in latest session")
            return None
        
        # Format results
        results = []
        for _, driver in ferrari_results.iterrows():
            # Handle NaN values properly
            driver_number = int(driver['DriverNumber']) if pd.notna(driver['DriverNumber']) else 0
            position = int(driver['Position']) if pd.notna(driver['Position']) else None
            points = int(driver['Points']) if pd.notna(driver['Points']) else 0
            
            result = {
                'driver_number': driver_number,
                'name': str(driver['FullName']) if pd.notna(driver['FullName']) else 'Unknown',
                'position': position,
                'time': format_f1_time(driver.get('Time', None)),
                'status': str(driver.get('Status', '')) if pd.notna(driver.get('Status', '')) else '',
                'points': points,
            }
            
            # Add qualifying times if available
            if hasattr(driver, 'Q1') and pd.notna(driver['Q1']):
                result['q1'] = format_f1_time(driver['Q1'])
            if hasattr(driver, 'Q2') and pd.notna(driver['Q2']):
                result['q2'] = format_f1_time(driver['Q2'])
            if hasattr(driver, 'Q3') and pd.notna(driver['Q3']):
                result['q3'] = format_f1_time(driver['Q3'])
            
            results.append(result)
        
        # Prepare session data
        session_info = {
            'event': event['EventName'],
            'location': event['Location'],
            'country': event['Country'],
            'round': int(event['RoundNumber']),
            'session_type': 'Qualifying' if session_data.session_info['Type'] == 'Qualifying' else 'Race',
            'date': session_data.session_info['StartDate'].isoformat(),
            'results': results,
            'total_drivers': len(session_data.results)
        }
        
        logger.info(f"✅ Successfully fetched latest session: {session_info['event']} - {session_info['session_type']}")
        return session_info
        
    except Exception as e:
        logger.error(f"Error fetching latest session: {e}")
        return None

def get_verified_standings():
    """Get standings from verified manual sources (already corrected)"""
    try:
        # Read the manually verified current season data
        standings_file = public_data_dir / 'current-season.json'
        if standings_file.exists():
            with open(standings_file, 'r') as f:
                data = json.load(f)
                logger.info("✅ Using verified standings data")
                return data
        else:
            logger.warning("No verified standings file found")
            return None
            
    except Exception as e:
        logger.error(f"Error reading verified standings: {e}")
        return None

def get_next_race():
    """Get next race from schedule (from verified data)"""
    try:
        # Read the manually verified next race data
        next_race_file = public_data_dir / 'next-race.json'
        if next_race_file.exists():
            with open(next_race_file, 'r') as f:
                data = json.load(f)
                logger.info("✅ Using verified next race data")
                return data
        else:
            logger.warning("No verified next race file found")
            return None
            
    except Exception as e:
        logger.error(f"Error reading verified next race: {e}")
        return None

def update_latest_session():
    """Update latest session data only"""
    try:
        logger.info("🔄 Updating latest session data...")
        
        session_data = fetch_latest_session()
        if session_data:
            # Save to public/data/latest-session.json
            output_file = public_data_dir / 'latest-session.json'
            with open(output_file, 'w') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Latest session data saved to {output_file}")
            return True
        else:
            logger.warning("❌ No latest session data to update")
            return False
            
    except Exception as e:
        logger.error(f"Error updating latest session: {e}")
        return False

def main():
    """Main optimized update function"""
    logger.info("🚀 Starting OPTIMIZED F1 data update...")
    logger.info("📋 Strategy: FastF1 for latest session only, verified data for standings")
    
    start_time = time.time()
    success_count = 0
    total_tasks = 3
    
    # Task 1: Update latest session with FastF1
    logger.info("📊 Task 1/3: Updating latest session data with FastF1...")
    if update_latest_session():
        success_count += 1
        logger.info("✅ Latest session update completed")
    else:
        logger.warning("⚠️ Latest session update failed")
    
    # Task 2: Verify standings data exists
    logger.info("📈 Task 2/3: Checking verified standings data...")
    standings_data = get_verified_standings()
    if standings_data:
        success_count += 1
        logger.info("✅ Verified standings data available")
    else:
        logger.warning("⚠️ No verified standings data found")
    
    # Task 3: Verify next race data exists  
    logger.info("🏁 Task 3/3: Checking verified next race data...")
    next_race_data = get_next_race()
    if next_race_data:
        success_count += 1
        logger.info("✅ Verified next race data available")
    else:
        logger.warning("⚠️ No verified next race data found")
    
    # Summary
    elapsed_time = time.time() - start_time
    logger.info(f"🏆 Update completed in {elapsed_time:.2f} seconds")
    logger.info(f"📊 Success rate: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        logger.info("🎉 All data sources are ready!")
        return True
    else:
        logger.warning(f"⚠️ {total_tasks - success_count} tasks failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            logger.info("✅ Optimized update script completed successfully")
        else:
            logger.error("❌ Optimized update script completed with errors")
    except KeyboardInterrupt:
        logger.info("🛑 Update cancelled by user")
    except Exception as e:
        logger.error(f"💥 Critical error in update script: {e}")