#!/usr/bin/env python3
"""
FastF1 Cache Cleanup Script
Clears FastF1 cache to free up disk space
"""

import shutil
import os
from pathlib import Path

def cleanup_cache():
    """Clean FastF1 cache directory"""
    cache_dir = Path('.cache')
    
    if cache_dir.exists():
        # Get current size
        size_before = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
        size_before_mb = size_before / (1024 * 1024)
        
        print(f"📊 Cache size before cleanup: {size_before_mb:.1f} MB")
        
        # Remove cache contents
        for item in cache_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        
        print("🧹 FastF1 cache cleared successfully")
        print("💡 Next update will download fresh data but should still be fast")
    else:
        print("ℹ️ No cache directory found")

if __name__ == "__main__":
    cleanup_cache()