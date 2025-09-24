from ast import arg
from unittest import result
import pytest
from task1 import check_age


def test_check_age_20():
    age = 20
    result = check_age(age)
    assert result == "Доступ разрешён"


def test_check_age_16():
    age = 16
    result = check_age(age)
    assert result == "Доступ запрещён"


def test_check_age_18():
    age = 18
    result = check_age(age)
    assert result == "Доступ разрешён"


def test_check_age_17():
    age = 17
    result = check_age(age)
    assert result == "Доступ запрещён"


def test_check_age_negative():
    age = -1
    result = check_age(age)
    assert result == "Доступ запрещён"


def test_check_age_with_string_detailed():
    with pytest.raises(TypeError):
        check_age(18.5)


def test_check_return_message_ex():
    with pytest.raises(TypeError) as ex_info:
        check_age(20.15)

    assert "Возраст должен быть целым число" in str(ex_info.value)
    assert "float" in str(ex_info.value)


@pytest.mark.parametrize(
    "arg, expected",
    [
        (17, "Доступ разрешен"),
        (19, "Доступ запрещён"),
    ],
)
@pytest.mark.xfail(reason="Проверка на падения")
def test_failed_test(arg, expected):
    result = check_age(arg)
    assert result == expected


@pytest.mark.parametrize(
    "age, expected",
    [
        (20, "Доступ разрешён"),
        (16, "Доступ запрещён"),
        (18, "Доступ разрешён"),
        (17, "Доступ запрещён"),
        (-1, "Доступ запрещён"),
    ],
)
def test_check_age_multiple(age, expected):
    result = check_age(age)
    assert result == expected


@pytest.fixture
def age_test_data():
    test_case = [
        (20, "Доступ разрешён"),
        (16, "Доступ запрещён"),
        (18, "Доступ разрешён"),
        (17, "Доступ запрещён"),
        (-1, "Доступ запрещён"),
    ]
    yield test_case


def test_check_age_with_fixture(age_test_data):
    for age, expected in age_test_data:
        result = check_age(age)
        assert result == expected

