# file: test_text_processor.py
import pytest
from main import count_words_and_sentences

# Фікстура для створення тимчасового файлу
@pytest.fixture
def create_temp_file(tmp_path):
    def _create_temp_file(content):
        # Створюємо тимчасовий файл у тимчасовій директорії
        file_path = tmp_path / "test_file.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    return _create_temp_file