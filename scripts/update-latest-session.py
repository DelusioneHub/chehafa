#!/usr/bin/env python3
"""
Quick Latest Session Updater
Fast script to update only the latest F1 session data
"""

import os
import sys
from pathlib import Path

def main():
    """Run the optimized update script"""
    script_dir = Path(__file__).parent
    optimized_script = script_dir / 'update-data-optimized.py'
    
    if not optimized_script.exists():
        print("❌ Optimized update script not found")
        return False
    
    print("🚀 Running optimized F1 data update...")
    
    # Run the optimized script
    import subprocess
    result = subprocess.run([sys.executable, str(optimized_script)], 
                          capture_output=False, text=True)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Latest session update completed")
    else:
        print("❌ Update failed")
        sys.exit(1)