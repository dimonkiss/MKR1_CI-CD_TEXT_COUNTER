import pytest
import os
from main import count_words_and_sentences

# Fixture for creating and cleaning up test files
@pytest.fixture
def temp_text_file(tmp_path):
    def create_file(content):
        file_path = tmp_path / "test_file.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    return create_file

# Test cases for word counting
@pytest.mark.parametrize("content,expected_words", [
    ("", 0),  # Empty file
    ("   ", 0),  # Whitespace only
    ("Hello world", 2),  # Simple case
    ("Hello, world!", 2),  # With punctuation
    ("This is a test.", 4),  # With sentence ending
    ("One  two   three    four", 4),  # Multiple spaces
    ("Word", 1),  # Single word
    ("Hello...world", 2),  # Ellipsis between words
    ("Привіт світ", 2),  # Unicode characters
    ("Multiple\nlines\ntest", 3),  # Newline separated words
    ("Comma,separated,words", 3),  # Comma separated words
    ("  Leading and trailing spaces  ", 4),  # Leading/trailing spaces
])
def test_word_counting(temp_text_file, content, expected_words):
    file_path = temp_text_file(content)
    word_count, _ = count_words_and_sentences(file_path)
    assert word_count == expected_words

# Test cases for sentence counting
@pytest.mark.parametrize("content,expected_sentences", [
    ("", 0),  # Empty file
    ("   ", 0),  # Whitespace only
    ("Hello world", 1),  # No punctuation
    ("Hello. World!", 2),  # Multiple sentences
    ("Is this a test? Yes it is!", 2),  # Question and exclamation
    ("This is a test... with ellipsis.", 1),  # Ellipsis
    ("One. Two. Three.", 3),  # Multiple dots
    ("Hello...world", 1),  # Ellipsis doesn't end sentence
    ("End with ellipsis...", 1),  # Ellipsis at end
    ("First!\nSecond?\nThird.", 3),  # Newline separated sentences
    ("  .  ", 0),  # Just a period with spaces
])
def test_sentence_counting(temp_text_file, content, expected_sentences):
    file_path = temp_text_file(content)
    _, sentence_count = count_words_and_sentences(file_path)
    assert sentence_count == expected_sentences

# Test error handling
def test_nonexistent_file():
    word_count, sentence_count = count_words_and_sentences("nonexistent_file.txt")
    assert word_count == 0
    assert sentence_count == 0

# Test combined word and sentence counting
@pytest.mark.parametrize("content,expected", [
    ("First sentence. Second sentence!", (4, 2)),
    ("Word1, word2. Word3? Word4!", (4, 3)),
    ("Testing... one two three.", (4, 1)),
])
def test_combined_counting(temp_text_file, content, expected):
    file_path = temp_text_file(content)
    result = count_words_and_sentences(file_path)
    assert result == expected

