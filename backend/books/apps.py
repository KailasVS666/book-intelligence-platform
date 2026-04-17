import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class BooksConfig(AppConfig):
    name = "books"

    def ready(self):
        """Perform professional health checks on module load."""
        if os.environ.get('RUN_MAIN') == 'true':
            self._check_ollama()

    def _check_ollama(self):
        import requests
        try:
            requests.get("http://localhost:11434/api/tags", timeout=1)
            logger.info("Intelligence Context: Ollama is reachable.")
        except Exception:
            logger.warning("Intelligence Context: Ollama is NOT reachable. AI features may fail.")
