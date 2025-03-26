# file: main.py
import re


def count_words_and_sentences(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            if not content.strip():
                return 0, 0

            # Підрахунок речень
            content_for_sentences = content.replace("...", "<ELLIPSIS>")
            sentence_endings = r'(?<!<ELLIPSIS>)([.!?])'
            sentences = [s.strip() for s in re.split(sentence_endings, content_for_sentences) if
                         s.strip() and s not in ".!?"]
            sentence_count = len(sentences)

            # Підрахунок слів
            content_for_words = content.replace("...", " ")
            word_separators = r'[,\s.]+'
            words = [word for word in re.split(word_separators, content_for_words) if word]
            word_count = len(words)

            return word_count, sentence_count  # Повертаємо кортеж із двох значень

    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        return 0, 0
    except Exception as e:
        print(f"Виникла помилка: {e}")
        return 0, 0


# Приклад використання
if __name__ == "__main__":
    file_path = "input.txt"  # Замініть на шлях до вашого файлу
    word_count, sentence_count = count_words_and_sentences(file_path)
    print(f"Кількість слів у файлі: {word_count}")
    print(f"Кількість речень у файлі: {sentence_count}")