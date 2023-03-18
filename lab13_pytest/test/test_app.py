import pytest
from app import hello, extractc_sentiment, contain_word


def test_hello():
    got = hello("Aleksandra")
    want = "Hello Aleksandra"

    assert got == want


testdata = ["I think today will be a great day",
            "I do not think this will turn out good"
            ]


@pytest.mark.parametrize('sample', testdata)
def test_extractc_sentiment(sample):
    sentiment: int = extractc_sentiment(sample)

    assert sentiment > 0


testdata2 = [
    "I think this is terrible and stupid idea",
    "I have a really bad feeling about this"
]


@pytest.mark.parametrize('sample', testdata2)
def test_extractc_sentiment2(sample):
    sentiment: int = extractc_sentiment(sample)

    assert sentiment < 0


testdata3 = [
    ('There is a duck in this text', 'duck', True),
    ('There is nothing here', 'duck', False)
]


@pytest.mark.parametrize('text, word, expected_output', testdata3)
def test_contain_word(text, word, expected_output):
    assert contain_word(word, text) == expected_output
