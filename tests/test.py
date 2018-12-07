from invars.invars import analyze_code


def test_fail_two_assign_same_name():
    code = (
        "one = 1\n"
        "two = 2\n"
        "two = one + two\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_aug_assign():
    code = (
        "one = 1\n"
        "two = 2\n"
        "two += one\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_increment_variable():
    code = (
        "a = 1\n"
        "a += 1\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_two_assign_method():
    code = (
        "class A(object):\n"
        ""
        "    def test(self):\n"
        "        one = 1\n"
        "        one = 2\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_two_assign_inside_block():
    code = (
        "if True:\n"
        "    a = 1\n"
        "    a = 2\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_two_assign_outer_scope():
    code = (
        "if True:\n"
        "    a = 1\n"
        "a = 2\n"  # invalid
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_reassign_index_for_loop():
    code = (
        "i = 0\n"
        "for i in range(10):\n"  # invalid
        "    pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_reassign_tuple_for_loop():
    code = (
        "v = 0\n"
        "for _, v in dict().items():\n"  # invalid
        "    pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_assign_inside_for_loop():
    code = (
        "l = [[1, 2, 3], [4, 5, 6]]\n"
        "for sublist in l:\n"
        "    total = sum(i)\n"  # invalid
    )
    # Cannot define a variable inside a for loop
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_nested_for_loop():
    code = (
        "for i in range(10):\n"
        "    for i in range(10):\n"
        "        pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_nested_with_block():
    code = (
        "with open() as f:\n"
        "   with open() as f:\n"
        "       pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 1


def test_fail_nested_with_block_tuple():
    code = (
        "with open() as (a, b):\n"
        "   with open() as (a, b):\n"
        "       pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 2


# def test_nofail_reassign_uninitialized_var():
#     code = (
#         "a = None\n"
#         "if True:\n"
#         "    a = True\n"
#         "else:\n"
#         "    a = False"
#     )
#     # Underscore variable can be assigned more than once
#     violations = analyze_code(code)
#     assert len(violations) == 0


def test_nofail_two_assign_underscore_var():
    code = (
        "_ = 1\n"
        "_ = 2\n"
    )
    # Underscore variable can be assigned more than once
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_same_var_diff_funcs():
    code = (
        "def f1():\n"
        "    one = 1\n"
        ""
        "def f2():\n"
        "    one = 2\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_subscript_dict():
    code = (
        "d = {}\n"
        "d[1] = 'a'\n"
        "d[2] = 'b'\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_assign_var_in_func():
    code = (
        "one = 1\n"
        ""
        "def f2():\n"
        "    one = 2\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_assign_inside_if():
    code = (
        "if b == 0:\n"
        "    a = 1\n"
        "else:\n"
        "    a = 2\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_for_loop():
    code = (
        "for i in range(1):\n"
        "    pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_nested_for_loop():
    code = (
        "for i in range(1):\n"
        "    for j in range(1):\n"
        "        pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0


def test_nofail_with_inside_for_loop():
    code = (
        "for i in range(10):\n"
        "    for j in range(10):\n"
        "        with open(f'doc.{i}.{j}', 'r') as f:\n"
        "            pass\n"
    )
    violations = analyze_code(code)
    assert len(violations) == 0
