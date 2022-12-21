from parsers.popcon_parser import parse_line
import pytest

def test_parse_line1():
    assert parse_line('1     passwd                         205052 188305  5289 11425    33 (Shadow Package Maintainers) ') == ('1','passwd','205052','188305','5289','11425','33','Shadow Package Maintainers')

def test_parse_line2():
    assert parse_line('1 passwd 205052 188305  5289 11425 33 (Shadow) ') == ('1','passwd','205052','188305','5289','11425','33','Shadow')


def test_parse_line3():
    with pytest.raises(ValueError) as exp:
        parse_line('#<name> is the developer name;')
    
    assert str(exp.value) == 'Invalid Input!'

def test_parse_line4():
    with pytest.raises(ValueError) as exp:
        parse_line('#rank name                            inst  vote   old recent no-files')
    
    assert str(exp.value) == 'Invalid Input!'

def test_parse_line6():
    with pytest.raises(ValueError) as exp:
        parse_line('#')
    
    assert str(exp.value) == 'Invalid Input!'