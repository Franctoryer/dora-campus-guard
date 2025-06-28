from typing import List

def get_sensitive_list() -> List[str]:
    with open('black_word.txt', 'r', encoding='utf-8') as f:
        sensitive_word_text = f.read()
    return sensitive_word_text.split(',')


def get_normal_list() -> List[str]:
    with open('white_word.txt', 'r', encoding='utf-8') as f:
        normal_word_text = f.read()
    return normal_word_text.split(',')


def is_sensitive(text: str) -> bool:
    sensitive_word_list = get_sensitive_list()
    normal_word_list = get_normal_list()
    for word1 in sensitive_word_list:
        if word1 in text:
            for word2 in normal_word_list:
                if word2 in text:
                    return False
            return True

    return False


if __name__ == '__main__':
    print(is_sensitive('我在操场跑步'))