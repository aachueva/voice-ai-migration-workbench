from src.evaluation import critical_term_recall, word_error_rate


def test_identical_transcript_has_zero_wer():
    assert word_error_rate("hello world", "hello world") == 0.0


def test_word_error_rate_detects_substitution():
    assert word_error_rate("hello world", "hello there") == 0.5


def test_critical_term_recall():
    reference = "Route ZX-204 to the SAML support queue"
    hypothesis = "Route ZX-204 to the support queue"
    assert critical_term_recall(reference, hypothesis, ("ZX-204", "SAML")) == 0.5
