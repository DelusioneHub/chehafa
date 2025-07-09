#!/usr/bin/env python3
"""
Cache Management for FastF1 Data
Implements intelligent caching to reduce API calls and improve performance
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class F1DataCache:
    def __init__(self, cache_dir='../cache', data_dir='../data'):
        self.cache_dir = Path(cache_dir)
        self.data_dir = Path(data_dir)
        self.cache_metadata_file = self.cache_dir / 'cache_metadata.json'
        
        # Create directories
        self.cache_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Load cache metadata
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """Load cache metadata"""
        if self.cache_metadata_file.exists():
            try:
                with open(self.cache_metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load cache metadata: {e}")
        
        return {
            'last_schedule_fetch': None,
            'last_session_update': None,
            'last_standings_update': None,
            'cached_files': {},
            'session_cache': {}
        }
    
    def _save_metadata(self):
        """Save cache metadata"""
        try:
            with open(self.cache_metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Could not save cache metadata: {e}")
    
    def should_update_schedule(self):
        """Check if schedule should be updated (once per day)"""
        last_fetch = self.metadata.get('last_schedule_fetch')
        if not last_fetch:
            return True
        
        last_fetch_time = datetime.fromisoformat(last_fetch)
        return datetime.now() - last_fetch_time > timedelta(days=1)
    
    def should_update_session_data(self, event_name, session_type):
        """Check if session data should be updated"""
        cache_key = f"{event_name}_{session_type}"
        last_update = self.metadata.get('session_cache', {}).get(cache_key)
        
        if not last_update:
            return True
        
        last_update_time = datetime.fromisoformat(last_update)
        
        # Update session data every 5 minutes during active sessions
        # Every hour otherwise
        active_threshold = timedelta(minutes=5)
        inactive_threshold = timedelta(hours=1)
        
        time_since_update = datetime.now() - last_update_time
        
        # Check if we're in an active session window (Friday-Sunday)
        now = datetime.now()
        is_race_weekend = now.weekday() >= 4  # Friday = 4, Saturday = 5, Sunday = 6
        
        threshold = active_threshold if is_race_weekend else inactive_threshold
        return time_since_update > threshold
    
    def should_update_standings(self):
        """Check if standings should be updated (every 30 minutes during race weekends)"""
        last_update = self.metadata.get('last_standings_update')
        if not last_update:
            return True
        
        last_update_time = datetime.fromisoformat(last_update)
        now = datetime.now()
        
        # More frequent updates during race weekends
        is_race_weekend = now.weekday() >= 4
        threshold = timedelta(minutes=30) if is_race_weekend else timedelta(hours=2)
        
        return now - last_update_time > threshold
    
    def mark_schedule_updated(self):
        """Mark schedule as updated"""
        self.metadata['last_schedule_fetch'] = datetime.now().isoformat()
        self._save_metadata()
    
    def mark_session_updated(self, event_name, session_type):
        """Mark session data as updated"""
        cache_key = f"{event_name}_{session_type}"
        if 'session_cache' not in self.metadata:
            self.metadata['session_cache'] = {}
        
        self.metadata['session_cache'][cache_key] = datetime.now().isoformat()
        self._save_metadata()
    
    def mark_standings_updated(self):
        """Mark standings as updated"""
        self.metadata['last_standings_update'] = datetime.now().isoformat()
        self._save_metadata()
    
    def get_cached_file_age(self, filename):
        """Get age of cached file in minutes"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return float('inf')
        
        file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
        age = datetime.now() - file_time
        return age.total_seconds() / 60  # Return age in minutes
    
    def is_file_fresh(self, filename, max_age_minutes=60):
        """Check if file is fresh enough"""
        age = self.get_cached_file_age(filename)
        return age < max_age_minutes
    
    def cleanup_old_cache(self, max_age_days=7):
        """Clean up old cache files"""
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age_days)
            
            for filepath in self.cache_dir.rglob('*'):
                if filepath.is_file():
                    file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if file_time < cutoff_time:
                        try:
                            filepath.unlink()
                            logger.info(f"Cleaned up old cache file: {filepath.name}")
                        except Exception as e:
                            logger.warning(f"Could not delete {filepath}: {e}")
        
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
    
    def get_cache_stats(self):
        """Get cache statistics"""
        try:
            cache_files = list(self.cache_dir.rglob('*'))
            cache_size = sum(f.stat().st_size for f in cache_files if f.is_file())
            
            data_files = list(self.data_dir.rglob('*.json'))
            data_size = sum(f.stat().st_size for f in data_files if f.is_file())
            
            return {
                'cache_files': len([f for f in cache_files if f.is_file()]),
                'cache_size_mb': cache_size / (1024 * 1024),
                'data_files': len(data_files),
                'data_size_mb': data_size / (1024 * 1024),
                'last_schedule_update': self.metadata.get('last_schedule_fetch'),
                'last_standings_update': self.metadata.get('last_standings_update')
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}

# Error handling utilities
class F1DataError(Exception):
    """Custom exception for F1 data errors"""
    pass

class APITimeoutError(F1DataError):
    """Raised when API calls timeout"""
    pass

class DataNotAvailableError(F1DataError):
    """Raised when requested data is not available"""
    pass

def with_retry(max_retries=3, delay=2, backoff=2):
    """Decorator for retrying failed operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Failed after {max_retries} retries: {e}")
                        raise
                    
                    logger.warning(f"Attempt {retries} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

def safe_file_operation(operation):
    """Safely perform file operations with error handling"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PermissionError:
                logger.error(f"Permission denied during {operation}")
                return False
            except OSError as e:
                logger.error(f"OS error during {operation}: {e}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error during {operation}: {e}")
                return False
        return wrapper
    return decorator