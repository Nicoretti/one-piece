# Modify the Rust extension to get the test below to pass
# Do NOT modify the test itself!
from konfy import hello_from_konfy


def test_smoke_test():
    expected = "Hello from Konfy"
    actual = hello_from_konfy()
    assert expected == actual

