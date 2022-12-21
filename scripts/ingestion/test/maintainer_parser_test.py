from parsers.maintainer_parser import parse_line
import pytest

def test_parse_line1():
    assert parse_line('1     Debian Gnome Maintainers       25448719 8522878 8289960 2616491 6019390') == ('1','Debian Gnome Maintainers','25448719','8522878','8289960','2616491','6019390')

def test_parse_line2():
    assert parse_line('1     Debian 25448719 8522878 8289960 2616491 6019390') == ('1','Debian','25448719','8522878','8289960','2616491','6019390')

def test_parse_line3():
    assert parse_line('1    Debian           Gnome     25448719     8522878   8289960    2616491    6019390') == ('1','Debian Gnome','25448719','8522878','8289960','2616491','6019390')    

def test_parse_line4():
    with pytest.raises(ValueError) as exp:
        parse_line('#<name> is the developer name;')
    
    assert str(exp.value) == 'Invalid Input!'

def test_parse_line5():
    with pytest.raises(ValueError) as exp:
        parse_line('#rank name                            inst  vote   old recent no-files')
    
    assert str(exp.value) == 'Invalid Input!'

def test_parse_line6():
    with pytest.raises(ValueError) as exp:
        parse_line('1     Debian Gnome Maintainers')
    
    assert "not enough values to unpac" in str(exp.value)

def test_parse_line7():
    with pytest.raises(ValueError) as exp:
        parse_line('#')
    
    assert str(exp.value) == 'Invalid Input!'