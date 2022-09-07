import datascience.utils as utils


def test_getNumericalColumnList():
    print("test_getNumericalColumnList")
    assert len(utils.getNumericalColumnList()) == 14.0
