# README für das Video player Projekt




## Struktur des Projekts

Die Projektstruktur sieht wie folgt aus:

```
/projektverzeichnis
│
├── app
│   ├── __init__.py
│   ├── redis_utils.py         # Hilfsfunktionen für Redis-Datenbank
│   ├── routes.py              # Flask-Routen und Logik
│   ├── templates/
│   │   ├── index.html         # Übersicht der verfügbaren Songs
│   │   └── song.html          # Detailansicht eines Songs
│   ├── config.py              # Konfiguration (z.B. Redis-Verbindung)
│   └── saved_data/            # Verzeichnis für heruntergeladene Daten (Videos und JSONs)
│
├── run.py                     # Einstiegspunkt der Anwendung
└── requirements.txt           # Abhängigkeiten
```

## Installation

1. **Voraussetzungen**
   - Python 3.x
   - Redis-Server (auf einem Host wie `130.61.189.22` in diesem Projekt, standardmäßig auf Port 6379)
   
2. **Abhängigkeiten installieren**

   Erstellen Sie ein virtuelles Umfeld und installieren Sie die benötigten Pakete:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Für Linux/macOS
   venv\Scripts\activate      # Für Windows
   pip install -r requirements.txt
   ```

3. **Redis-Server**

   Der Redis-Server sollte auf dem angegebenen Host (z.B. `130.61.189.22`) laufen, und die Konfiguration ist in der `config.py` hinterlegt. Stellen Sie sicher, dass Redis korrekt konfiguriert ist und die Daten im richtigen Format gespeichert sind.

## Konfiguration

Die Konfiguration der Anwendung ist in der Datei `config.py` enthalten. Wichtige Parameter sind:

- **SECRET_KEY**: Ein geheimer Schlüssel für die Flask-Sitzungen.
- **REDIS_HOST**: Die Adresse des Redis-Servers.
- **REDIS_PORT**: Der Redis-Serverport (Standard: 6379).
- **REDIS_DB**: Die Redis-Datenbanknummer.
- **REDIS_PASSWORD**: Passwort für die Redis-Verbindung (falls erforderlich).

Beispiel:

```python
class Config:
    SECRET_KEY = "supersecretkey"
    REDIS_HOST = "130.61.189.22"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = "!/=?aml-redis-2024-projct"
```

## Anwendung starten

1. **Starten der Anwendung**

   Um die Anwendung zu starten, führen Sie den folgenden Befehl aus:

   ```bash
   python run.py
   ```

2. **Zugriff auf die Anwendung**

   Nach dem Start können Sie die Anwendung in einem Webbrowser unter `http://127.0.0.1:5000/` erreichen.

   - **Startseite (Index)**: Zeigt eine Liste aller verfügbaren Songs. Jeder Song ist mit einem Link versehen, der zu den Details des Songs führt.
   - **Song-Details**: Auf der Detailseite eines Songs können Sie Informationen zum Video sowie geplante Veröffentlichungsdaten (Scheduler-Informationen) einsehen. Zusätzlich werden alle Daten des Songs in einer JSON-Datei gespeichert und auf dem Server abgelegt.

## Funktionsweise

### 1. **Datenabruf aus Redis**

Die Anwendung nutzt Redis, um Daten zu verwalten. Es gibt mehrere Funktionen, die Daten von Redis abrufen:

- **`get_all_songs(client)`**: Holt alle verfügbaren Song-Namen aus Redis, basierend auf den zugehörigen Scheduler-Daten.
- **`get_video(client, song_name)`**: Holt die Videodaten für einen spezifischen Song.
- **`get_scheduler_data(client)`**: Holt die Scheduler-Daten, die die geplante Veröffentlichung des Songs beschreiben.

### 2. **Speichern der Daten**

Für jeden Song werden Daten wie Video-Dateien und Scheduler-Informationen aus Redis abgerufen und in einer lokalen Datei gespeichert:

- **`save_song_data(song_name, client)`**: Diese Funktion erstellt ein Verzeichnis namens `saved_data`, in dem die heruntergeladenen Video-Dateien und JSON-Daten gespeichert werden. Jede Datei erhält einen einzigartigen Namen basierend auf dem Song-Namen.

### 3. **Routen und Templates**

Die Anwendung verwendet Flask-Routen, um den Inhalt anzuzeigen:

- **`index()`**: Diese Route zeigt die Startseite mit einer Liste aller verfügbaren Songs.
- **`song_details(song_name)`**: Diese Route zeigt detaillierte Informationen zu einem spezifischen Song, einschließlich Video- und Scheduler-Daten.

Die HTML-Templates verwenden die Jinja2-Templating-Engine, um die Daten auf der Seite anzuzeigen. Die Datei `index.html` zeigt die Song-Liste, und `song.html` zeigt die Details eines einzelnen Songs.

### 4. **Fehlerbehandlung**

Falls ein Song-Video nicht gefunden werden kann, gibt es eine Fehlerbehandlung, die eine 404-Seite mit einer entsprechenden Nachricht anzeigt.

## Beispiele

- **Startseite (`index.html`)**:
   Zeigt eine Liste von Songs. Jeder Song ist als Link dargestellt, der auf die Detailseite des Songs verweist.

   ```html
   <ul>
       {% for song in songs %}
       <li>
           <a href="{{ url_for('main.song_details', song_name=song['song_name']) }}">
               {{ song['song_name'] }}
           </a>
       </li>
       {% endfor %}
   </ul>
   ```

- **Song-Detailseite (`song.html`)**:
   Zeigt die Details eines Songs, einschließlich des Video-Dateinamens und der zugehörigen Scheduler-Daten.

   ```html
   <h1>{{ song_name }}</h1>
   <h2>Video Information</h2>
   <p>Filename: {{ video_data['filename'] }}</p>
   <h2>Scheduler Information</h2>
   <p>{{ song_scheduler_info }}</p>
   ```

## Weitere Hinweise

- Alle heruntergeladenen Daten (Videos und JSON-Dateien) werden im Verzeichnis `saved_data` gespeichert.
- Die Anwendung speichert auch eine JSON-Datei für jedes Song, die alle relevanten Informationen enthält.
- Die Redis-Datenbank muss korrekt mit den erforderlichen Datenstrukturen konfiguriert sein, um ordnungsgemäß zu funktionieren.

## Weiter Info

Dieses Projekt wurde von  team 4 erstellt.