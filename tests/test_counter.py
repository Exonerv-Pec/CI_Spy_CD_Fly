from word_counter import count_words, most_common_words, average_word_length


def test_count_words_basic():
    assert count_words("hello world") == 2


def test_count_words_empty():
    assert count_words("") == 0


def test_count_words_punctuation():
    assert count_words("hello, world!") == 2


def test_most_common_words():
    text = "cat dog cat bird cat dog"
    result = most_common_words(text, top_n=2)
    assert result[0] == ("cat", 3)
    assert result[1] == ("dog", 2)


def test_average_word_length():
    assert average_word_length("cat dog") == 3.0


def test_average_word_length_empty():
    assert average_word_length("") == 0.0
