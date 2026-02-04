import os
import subprocess

# Hinweis: Dieses Skript funktioniert nur auf einem macOS System mit installiertem 'dmgbuild'.
def build_dmg():
    app_name = "TransformatorPro"
    dist_path = "dist"
    app_path = os.path.join(dist_path, f"{app_name}.app")
    dmg_output = os.path.join(dist_path, f"{app_name}_Installer.dmg")

    if not os.path.exists(app_path):
        print(f"Fehler: {app_path} nicht gefunden. Bitte zuerst das App-Bundle mit PyInstaller erstellen.")
        return

    # dmgbuild configuration (simplified)
    # Für eine fortgeschrittene DMG mit Hintergrundbild müsste man eine settings.py nutzen.
    cmd = [
        "dmgbuild",
        "-s", "dmg_settings.py", # Optional: Falls vorhanden
        app_name,
        dmg_output
    ]
    
    print(f"Erstelle DMG: {dmg_output}...")
    # Da dmgbuild oft eine settings-datei braucht, hier ein vereinfachter Aufruf 
    # oder alternativ 'hdiutil' (macOS native)
    hdi_cmd = [
        "hdiutil", "create", "-volname", app_name, 
        "-srcfolder", app_path, "-ov", "-format", "UDZO", dmg_output
    ]
    
    try:
        subprocess.run(hdi_cmd, check=True)
        print("DMG erfolgreich erstellt!")
    except Exception as e:
        print(f"Fehler beim Erstellen der DMG: {e}")

if __name__ == "__main__":
    if os.name == 'posix': # macOS/Linux
        build_dmg()
    else:
        print("Dieses Skript ist für macOS gedacht.")
