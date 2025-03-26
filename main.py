import re


def count_words_and_sentences(file_path):
    try:
        # Зчитуємо вміст файлу
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Якщо файл порожній, повертаємо 0 слів і 0 речень
            if not content.strip():
                return 0, 0

            # Крок 1: Підрахунок речень
            # Символи, що закінчують речення: ".", "!", "?", "..."
            # Використаємо регулярний вираз для розділення тексту на речення
            # Замінюємо "..." на унікальний символ, щоб обробити його окремо
            content_for_sentences = content.replace("...", "<ELLIPSIS>")
            # Розділяємо текст за символами . ! ? (але не за <ELLIPSIS>)
            sentence_endings = r'(?<!<ELLIPSIS>)([.!?])'
            sentences = [s.strip() for s in re.split(sentence_endings, content_for_sentences) if
                         s.strip() and s not in ".!?"]
            # Підраховуємо кількість речень (кожне розділення додає 1 речення)
            sentence_count = len(sentences)

            return sentence_count

    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        return 0, 0
    except Exception as e:
        print(f"Виникла помилка: {e}")
        return 0, 0


# Приклад використання
file_path = "input.txt"  # Замініть на шлях до вашого файлу
word_count, sentence_count = count_words_and_sentences(file_path)

print(f"Кількість слів у файлі: {word_count}")
print(f"Кількість речень у файлі: {sentence_count}")