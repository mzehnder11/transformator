\# Transformator Pro



Transformator Pro ist eine professionelle Desktop-Anwendung zur Konvertierung und Transformation verschiedenster Dateitypen. Die Anwendung bietet eine moderne grafische Benutzeroberfläche auf Basis von CustomTkinter und unterstützt die Stapelverarbeitung von Medien- und Dokumentdateien.



\---



\## Funktionen



\* Bildkonvertierung: Unterstützung für PNG, JPG, WEBP, GIF, BMP, TIFF und AVIF.

\* Videotransformation: Konvertierung zwischen MP4, MOV, AVI, MKV und GIF (inklusive automatischer Skalierung für GIFs).

\* Audiokonvertierung: Verarbeitung von MP3, WAV, OGG und FLAC.

\* Dokumentenverarbeitung: Umwandlung von Textdateien (TXT, MD) in PDF-Dokumente.

\* Stapelverarbeitung: Mehrere Dateien können gleichzeitig zur Warteschlange hinzugefügt und konvertiert werden.

\* Integriertes Setup: Automatisierte Skripte zur Einrichtung der Python-Umgebung und Installation notwendiger Systemkomponenten wie FFmpeg.



\---



\## Voraussetzungen



\* Python 3.x

\* FFmpeg (erforderlich für die Video- und Audioverarbeitung)

\* Internetverbindung für die initiale Einrichtung der Abhängigkeiten



\---



\## Installation und Start



Die Anwendung nutzt virtuelle Umgebungen, um Konflikte mit anderen Python-Installationen zu vermeiden.



\### Windows

1\. Führen Sie die Datei setup.ps1 in der PowerShell aus.

2\. Das Skript installiert Python-Abhängigkeiten und versucht, FFmpeg via winget zu installieren, falls es fehlt.



\### macOS / Linux

1\. Öffnen Sie das Terminal im Projektordner.

2\. Machen Sie das Skript ausführbar: chmod +x setup.sh

3\. Starten Sie die Installation: ./setup.sh

&#x20;  \* Auf macOS wird versucht, FFmpeg via Homebrew zu installieren.



\---



\## Erstellung ausführbarer Dateien (Build)



Das Projekt enthält Konfigurationen, um eigenständige Programme zu erstellen, die ohne installierte Python-Umgebung laufen.



\* Windows (EXE): Starten Sie python build\_exe.py, um ein Paket im Ordner dist/TransformatorPro/ zu generieren.

\* macOS (DMG): Nutzen Sie das Skript build\_dmg.py (erfordert ein macOS-System und dmgbuild).



\---



\## Benutzung



1\. Wählen Sie in der linken Seitenleiste die gewünschte Kategorie (Bilder, Videos, Text oder Audio).

2\. Fügen Sie Dateien über die Schaltfläche "Neue Dateien hinzufügen" zur Liste hinzu.

3\. Wählen Sie das Zielformat aus dem Dropdown-Menü im unteren Bereich aus.

4\. Klicken Sie auf "Konvertierung starten".

5\. Die fertigen Dateien werden automatisch im Unterordner /converted im Projektverzeichnis gespeichert.



\---



\## Projektstruktur



\* app.py: Hauptanwendung und grafische Benutzeroberfläche.

\* build\_exe.py / build\_dmg.py: Skripte zur Paketierung für Windows und macOS.

\* requirements.txt: Liste der benötigten Bibliotheken (Pillow, MoviePy, CustomTkinter, FPDF2, etc.).

\* setup.ps1 / setup.sh: Plattformspezifische Installationsskripte.

\* BUILD\_GUIDE.md: Detaillierte Anleitung für den Build-Prozess.



\---

Dokumentation für Transformator Pro.

