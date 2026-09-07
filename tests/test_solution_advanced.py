from solution_advanced import subtract, multiply, divide

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(1, 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass