import pytest
import re
from app import refuse_in_user_lang, REFUSAL_EN, REFUSAL_MR

# Marathi (Devanagari) text
def test_refuse_in_user_lang_marathi():
    text = "मराठा आरक्षण काय आहे?"
    assert refuse_in_user_lang(text) == REFUSAL_MR

# English text
def test_refuse_in_user_lang_english():
    text = "What is Maratha reservation?"
    assert refuse_in_user_lang(text) == REFUSAL_EN

# Mixed text
def test_refuse_in_user_lang_mixed():
    text = "मराठा reservation"
    assert refuse_in_user_lang(text) == REFUSAL_MR

# Empty string
def test_refuse_in_user_lang_empty():
    text = ""
    assert refuse_in_user_lang(text) == REFUSAL_EN
