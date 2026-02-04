# Transformator Pro - Build Guide

Dieses Projekt kann als ausführbare Datei für Windows (.exe) und macOS (.dmg) paketiert werden.

## 🛠️ Windows (EXE)

Wir haben ein automatisiertes Skript `build_exe.py` erstellt, das alle Abhängigkeiten (inklusive CustomTkinter-Assets) korrekt einbindet.

### Voraussetzungen
- Python 3.x
- Alle Pakete aus `requirements.txt` (installiert via `pip install -r requirements.txt`)
- PyInstaller (`pip install pyinstaller`)

### Build-Prozess
Führen Sie einfach folgenden Befehl aus:
```powershell
python build_exe.py
```
Die fertige Anwendung finden Sie anschließend im Ordner `dist/TransformatorPro/`.

---

## 🍎 macOS (DMG)

Aufgrund technischer Einschränkungen (Code-Signierung und Mach-O Format) muss der Build-Prozess für macOS zwingend **auf einem Mac** durchgeführt werden.

### Build-Prozess auf macOS:
1.  **Repository klonen** auf den Mac.
2.  **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller dmgbuild
    ```
3.  **App-Bundle erstellen**:
    ```bash
    python3 -m PyInstaller --noconfirm --onedir --windowed \
        --add-data "$(python3 -c 'import customtkinter; print(customtkinter.__path__[0])'):customtkinter" \
        --icon=icon.ico \
        --name="TransformatorPro" \
        app.py
    ```
4.  **DMG erstellen**:
    Wir haben ein Skript `build_dmg.py` vorbereitet, das auf einem Mac ausgeführt werden kann, um das `.app` Bundle in ein schönes `.dmg` zu verpacken.

---

## 🎨 Icon / Design
Das neue Logo (`icon.ico` / `icon.png`) wurde speziell für den professionellen Look von "Transformator Pro" entworfen.
