from model.list import IndexList

import unittest
import unittest.mock

class IndexListTestCase(unittest.TestCase):

    def setUp(self):
        self.good_data = [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]
        self.bad_data = ['bob', 'jimmy', True, False, 'haha', 42, 3.14]
        self.data1 = [1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1]
        self.data2 = [0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0]

    def test_pass_list_of_1_and_0(self):
        # this tests the actual list inside the IndexList
        indexlist = IndexList(self.good_data)
        assert indexlist._lst == self.good_data

    def test_lst_getter_works(self):
        # this tests the property getter
        indexlist = IndexList(self.good_data)
        assert indexlist.lst == self.good_data

    def test_pass_list_of_wrong_values(self):
        with self.assertRaises(ValueError):
            indexlist = IndexList(self.bad_data)

    def test_lst_setter_does_not_work_raises_attribute_error(self):
        indexlist = IndexList(self.good_data)
        with self.assertRaises(AttributeError):
            indexlist.lst = [1]

    def test_iter_overriden_method(self):
        indexlist = IndexList(self.good_data)
        assert list(indexlist) == self.good_data

    def test_or_overriden_method(self):
        expected = [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]
        il1 = IndexList(self.data1)
        il2 = IndexList(self.data2)
        assert list(il1 | il2) == expected

    def test_and_overriden_method(self):
        expected = [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        il1 = IndexList(self.data1)
        il2 = IndexList(self.data2)
        assert list(il1 & il2) == expected

    def test_invert_overriden_method(self):
        expected = [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0]
        il = IndexList(self.good_data)
        assert list(~il) == expected

    def test_str_overriden_method(self):
        indexlist = IndexList(self.good_data)
        assert str(indexlist) == f"IndexList({indexlist._lst})"
