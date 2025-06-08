# Simple multilanguage support for English and Italian

LANGUAGES = {
    'en': {
        'app_title': 'Base',
        'success': 'SUCCESS: {msg}',
        'error': 'ERROR: {msg}',
        'file': 'File',
        'exit': 'Exit',
        'log': 'Log',
        'view_log': 'View Log',
        'help': 'Help',
        'about': 'About',
        'sponsor': 'Sponsor',
        'version': 'Version',
        'language': 'Language',
        'log_viewer_title': 'Application Log',
        'close': 'Close',
        'log_file_not_found': 'Log file not found.',
        'no_log_entries': 'No log entries for {level}',
        'usage_tab': 'Usage',
        'features_tab': 'Features',
        'sponsor_on_github': 'Sponsor on GitHub',
        'join_discord': 'Join Discord',
        'buy_me_a_coffee': 'Buy Me a Coffee',
        'join_the_patreon': 'Join the Patreon',
        'about_title': 'About',
        'about_project': 'Project',
        'about_description': 'A modern Python GUI app for demonstration and productivity.',
        'copyright': '\u00a9 2025 Nsfr750',
        'show_version': 'Show Version',
        'version_info': 'Version Information',
        'help_usage': "To start the application, run main.py from the project root.\nNavigate the menu bar for Help, About, Log Viewer, and more.\nUse the Log Viewer to see and filter application logs in real time.\nCustom log entries can be added in your code using log_info, log_warning, log_error.\nCommon troubleshooting: If you see import errors, ensure you are running from the root directory.\n",
        'help_features': "- Centralized logging system: info, warning, error, and uncaught exceptions are logged to traceback.log.\n- Log Viewer dialog with real-time filtering: view ALL, INFO, WARNING, or ERROR entries.\n- Use log_info, log_warning, log_error for custom log entries in your code.\n- Robust error handling and extensible design.\n",
    },
    'it': {
        'app_title': 'Base',
        'success': 'SUCCESSO: {msg}',
        'error': 'ERRORE: {msg}',
        'file': 'File',
        'exit': 'Esci',
        'log': 'Log',
        'view_log': 'Visualizza Log',
        'help': 'Aiuto',
        'about': 'Informazioni',
        'sponsor': 'Sostieni',
        'version': 'Versione',
        'language': 'Lingua',
        'log_viewer_title': 'Registro Applicazione',
        'close': 'Chiudi',
        'log_file_not_found': 'File di log non trovato.',
        'no_log_entries': 'Nessuna voce di log per {level}',
        'usage_tab': 'Utilizzo',
        'features_tab': 'Funzionalità',
        'sponsor_on_github': 'Sponsorizza su GitHub',
        'join_discord': 'Unisciti a Discord',
        'buy_me_a_coffee': 'Offrimi un caffè',
        'join_the_patreon': 'Unisciti a Patreon',
        'about_title': 'Informazioni',
        'about_project': 'Progetto',
        'about_description': "Un'applicazione GUI Python moderna per dimostrazione e produttività.",
        'copyright': '\u00a9 2025 Nsfr750',
        'show_version': 'Mostra Versione',
        'version_info': 'Informazioni Versione',
        'help_usage': "Per avviare l'applicazione, esegui main.py dalla cartella principale del progetto.\nNaviga nella barra dei menu per Aiuto, Informazioni, Visualizza Log e altro.\nUsa il Visualizzatore Log per vedere e filtrare i log dell'applicazione in tempo reale.\nPuoi aggiungere voci personalizzate nel log usando log_info, log_warning, log_error nel tuo codice.\nRisoluzione problemi: se visualizzi errori di importazione, assicurati di eseguire dalla cartella principale.\n",
        'help_features': "- Sistema di logging centralizzato: info, warning, error ed eccezioni non gestite vengono registrate in traceback.log.\n- Finestra Visualizza Log con filtro in tempo reale: visualizza TUTTI, INFO, WARNING o ERROR.\n- Usa log_info, log_warning, log_error per aggiungere voci personalizzate nel log dal tuo codice.\n- Gestione robusta degli errori e design estendibile.\n",
    }
}

import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def _load_lang():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('language', 'en')
    except Exception:
        return 'en'

def _save_lang(lang):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({'language': lang}, f)
    except Exception:
        pass

_current_lang = _load_lang()

def set_language(lang):
    global _current_lang
    if lang in LANGUAGES:
        _current_lang = lang
    else:
        _current_lang = 'en'
    _save_lang(_current_lang)

def get_language():
    return _current_lang

def get_available_languages():
    """
    Returns a list of available language codes.
    
    Returns:
        list: List of language codes (e.g., ['en', 'it'])
    """
    return list(LANGUAGES.keys())

def tr(key, **kwargs):
    text = LANGUAGES.get(_current_lang, LANGUAGES['en']).get(key, key)
    return text.format(**kwargs)
