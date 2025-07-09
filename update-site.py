#!/usr/bin/env python3
"""
UNICO SCRIPT PER AGGIORNARE IL SITO
Aggiorna tutti i dati necessari per il sito in un solo comando
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Aggiorna tutti i dati del sito"""
    print("🏁 AGGIORNAMENTO SITO FERRARI")
    print("=" * 50)
    
    # Verifica ambiente virtuale
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Attiva ambiente virtuale se esiste
    venv_path = script_dir / 'venv'
    if venv_path.exists():
        if os.name == 'nt':  # Windows
            python_exe = venv_path / 'Scripts' / 'python.exe'
        else:  # Linux/Mac
            python_exe = venv_path / 'bin' / 'python'
    else:
        python_exe = sys.executable
    
    success = True
    
    # 1. Aggiorna i dati dell'ultima sessione
    print("\n1️⃣ Aggiornamento ultima sessione...")
    try:
        result = subprocess.run([
            str(python_exe), 
            'scripts/update-data-optimized.py'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Dati ultima sessione aggiornati")
        else:
            print("❌ Errore aggiornamento sessione:")
            print(result.stderr)
            success = False
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout aggiornamento sessione")
        success = False
    except Exception as e:
        print(f"❌ Errore: {e}")
        success = False
    
    # 2. Aggiorna classifiche complete
    print("\n2️⃣ Aggiornamento classifiche complete...")
    try:
        result = subprocess.run([
            str(python_exe),
            'scripts/calculate-standings.py'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Classifiche piloti e costruttori aggiornate")
        else:
            print("❌ Errore classifiche:")
            print(result.stderr)
            success = False
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout classifiche")
        success = False
    except Exception as e:
        print(f"❌ Errore: {e}")
        success = False
    
    # 3. Pulizia cache vecchia
    print("\n3️⃣ Pulizia cache...")
    try:
        result = subprocess.run([
            str(python_exe),
            'scripts/cleanup-cache.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Cache pulita")
        else:
            print("⚠️ Warning pulizia cache")
    except:
        print("⚠️ Pulizia cache non riuscita (non critico)")
    
    # Risultato finale
    print("\n" + "=" * 50)
    if success:
        print("🎉 AGGIORNAMENTO COMPLETATO CON SUCCESSO!")
        print("Il sito è ora aggiornato con gli ultimi dati F1")
    else:
        print("❌ AGGIORNAMENTO FALLITO")
        print("Controlla i log per i dettagli")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)