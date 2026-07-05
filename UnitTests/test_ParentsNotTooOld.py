# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US12_ParentsNotTooOld(unittest.TestCase):

    # Test Cases:
    # 1: Mother less than 60 years older than child (PASS)
    # 2: Mother 60 or more years older than child (FAIL)
    # 3: Father less than 80 years older than child (PASS)
    # 4: Father 80 or more years older than child (FAIL)
    # 5: Both parents too old (FAIL, both errors reported)

    def _make_family(self, husband_birthday, wife_birthday, child_birthday):
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = husband_birthday
        husband.add_spouse('F1')

        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = wife_birthday
        wife.add_spouse('F1')

        child = Individual()
        child.uid = 'I03'
        child.name = 'Alice /Carter/'
        child.gender = 'F'
        child.birthday = child_birthday
        child.add_child('F1')

        individuals = [husband, wife, child]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'
        fam.add_children('I03')

        return fam, individuals
    # End _make_family

    def test_mother_not_too_old(self):
        fam, individuals = self._make_family('5 MAY 1930', '14 AUG 1955', '1 JAN 1980')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_parents_not_too_old(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_mother_not_too_old

    def test_mother_too_old(self):
        fam, individuals = self._make_family('5 MAY 1930', '14 AUG 1919', '1 JAN 1980')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_parents_not_too_old(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US12: Mother ID I02 is 60 or more years older than Child ID I03 in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_mother_too_old

    def test_father_not_too_old(self):
        fam, individuals = self._make_family('5 MAY 1930', '14 AUG 1955', '1 JAN 1980')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_parents_not_too_old(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_father_not_too_old

    def test_father_too_old(self):
        fam, individuals = self._make_family('5 MAY 1890', '14 AUG 1955', '1 JAN 1980')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_parents_not_too_old(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US12: Father ID I01 is 80 or more years older than Child ID I03 in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_father_too_old

    def test_both_parents_too_old(self):
        fam, individuals = self._make_family('5 MAY 1890', '14 AUG 1900', '1 JAN 1980')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_parents_not_too_old(individuals)

            self.assertEqual(
                fake_out.getvalue(),
                'ERROR: US12: Mother ID I02 is 60 or more years older than Child ID I03 in family F1!\n'
                'ERROR: US12: Father ID I01 is 80 or more years older than Child ID I03 in family F1!\n'
            )
            self.assertEqual(result, False)
        # End with
    # End test_both_parents_too_old

# End Test_US12_ParentsNotTooOld


if __name__ == '__main__':
    unittest.main()
# End if
