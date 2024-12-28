import string

def analyze_characters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        char_count = len(content)
        letter_count = sum(c.isalpha() for c in content)
        digit_count = sum(c.isdigit() for c in content)
        whitespace_count = sum(c.isspace() for c in content)
        punctuation_count = sum(c in string.punctuation for c in content)

        pattern_count = sum(1 for i in range(len(content) - 2)
                            if content[i].isalpha() and content[i + 1] == '.' and content[i + 2].isalpha())

        print(f"Total characters: {char_count}")
        print(f"Letters: {letter_count}")
        print(f"Digits: {digit_count}")
        print(f"Whitespace: {whitespace_count}")
        print(f"Punctuation: {punctuation_count}")
        print(f"Occurrences of 'letter.letter' patterns: {pattern_count}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

file_path = "CONTEXT.txt"

analyze_characters(file_path)
