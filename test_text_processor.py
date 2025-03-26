# file: test_text_processor.py
import pytest
import os
from text_processor import count_words_and_sentences


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


# Тестування з параметризацією
@pytest.mark.parametrize("content, expected_words, expected_sentences", [
    # Тест 1: Порожній файл
    ("", 0, 0),

    # Тест 2: Одне речення без розділювачів
    ("Привіт", 1, 1),

    # Тест 3: Одне речення з комами і пробілами
    ("Привіт, як справи?", 3, 1),

    # Тест 4: Кілька речень із різними закінченнями
    ("Я добре... Ти як? Дуже добре!", 5, 3),

    # Тест 5: Текст із кількома розділювачами поспіль
    ("Слово,,інше. Ще одне...", 4, 2),

    # Тест 6: Текст із пробілами та без закінчень речень
    ("Слово інше ще", 3, 1),

    # Тест 7: Текст із лише розділювачами
    (",,, ... .", 0, 0),
])
def test_count_words_and_sentences(create_temp_file, content, expected_words, expected_sentences):
    # Створюємо тимчасовий файл із заданим вмістом
    file_path = create_temp_file(content)

    # Викликаємо функцію
    word_count, sentence_count = count_words_and_sentences(file_path)

    # Перевіряємо результати
    assert word_count == expected_words, f"Очікувалось {expected_words} слів, отримано {word_count}"
    assert sentence_count == expected_sentences, f"Очікувалось {expected_sentences} речень, отримано {sentence_count}"


# Тест для перевірки випадку, коли файл не існує
def test_file_not_found():
    word_count, sentence_count = count_words_and_sentences("non_existent_file.txt")
    assert word_count == 0
    assert sentence_count == 0


# Тест для перевірки обробки помилок (наприклад, файл без прав доступу)
@pytest.mark.skipif(os.name == 'nt', reason="Тестування прав доступу складне на Windows")
def test_file_permission_error(tmp_path):
    file_path = tmp_path / "test_file.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("Тестовий текст.")

    # Змінюємо права доступу (тільки для Unix-подібних систем)
    os.chmod(file_path, 0o000)  # Забороняємо доступ

    try:
        word_count, sentence_count = count_words_and_sentences(file_path)
        assert word_count == 0
        assert sentence_count == 0
    finally:
        # Відновлюємо права доступу, щоб уникнути проблем із видаленням
        os.chmod(file_path, 0o666)