# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US08_ChildrenBirthDates(unittest.TestCase):

    # Test Cases:
    # 1: Child born before parents' marriage (FAIL)
    # 2: Child born after parents' marriage, no divorce (PASS)
    # 3: Child born more than 9 months after divorce (FAIL)
    # 4: Child born within 9 months after divorce (PASS)
    # 5: Child does not exist in individuals list (FAIL)

    def _make_parents(self):
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = '5 MAY 1948'
        husband.add_spouse('F1')

        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = '14 AUG 1950'
        wife.add_spouse('F1')

        return husband, wife
    # End _make_parents

    def test_child_born_before_marriage(self):
        husband, wife = self._make_parents()

        child = Individual()
        child.uid = 'I03'
        child.name = 'Alice /Carter/'
        child.gender = 'F'
        child.birthday = '1 JAN 1951'
        child.add_child('F1')

        individuals = [husband, wife, child]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_children_birth_dates(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US08: Child ID I03 was born before the marriage of their parents in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_child_born_before_marriage

    def test_child_born_after_marriage_no_divorce(self):
        husband, wife = self._make_parents()

        child = Individual()
        child.uid = 'I03'
        child.name = 'Alice /Carter/'
        child.gender = 'F'
        child.birthday = '1 JAN 1955'
        child.add_child('F1')

        individuals = [husband, wife, child]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_children_birth_dates(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_child_born_after_marriage_no_divorce

    def test_child_born_more_than_9_months_after_divorce(self):
        husband, wife = self._make_parents()

        child = Individual()
        child.uid = 'I03'
        child.name = 'Alice /Carter/'
        child.gender = 'F'
        child.birthday = '1 JAN 1970'
        child.add_child('F1')

        individuals = [husband, wife, child]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.divorced = '1 JAN 1969'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_children_birth_dates(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US08: Child ID I03 was born more than 9 months after the divorce of their parents in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_child_born_more_than_9_months_after_divorce

    def test_child_born_within_9_months_after_divorce(self):
        husband, wife = self._make_parents()

        child = Individual()
        child.uid = 'I03'
        child.name = 'Alice /Carter/'
        child.gender = 'F'
        child.birthday = '1 JUL 1969'
        child.add_child('F1')

        individuals = [husband, wife, child]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.divorced = '1 JAN 1969'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_children_birth_dates(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_child_born_within_9_months_after_divorce

    def test_child_does_not_exist(self):
        husband, wife = self._make_parents()

        individuals = [husband, wife]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_children_birth_dates(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US08: Child ID I03 does not exist in the list of individuals!\n')
            self.assertEqual(result, False)
        # End with
    # End test_child_does_not_exist

# End Test_US08_ChildrenBirthDates


if __name__ == '__main__':
    unittest.main()
# End if
