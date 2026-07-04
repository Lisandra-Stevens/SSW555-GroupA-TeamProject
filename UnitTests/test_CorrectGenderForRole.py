# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US21_CorrectGenderForRole(unittest.TestCase):

    # Test Cases:
    # 1: Husband is male, wife is female (PASS)
    # 2: Husband is not male (FAIL)
    # 3: Wife is not female (FAIL)
    # 4: Both husband and wife have incorrect gender (FAIL, both errors reported)

    def _make_family(self, husband_gender, wife_gender):
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = husband_gender
        husband.birthday = '5 MAY 1948'
        husband.add_spouse('F1')

        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = wife_gender
        wife.birthday = '14 AUG 1950'
        wife.add_spouse('F1')

        individuals = [husband, wife]

        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1972'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        return fam, individuals
    # End _make_family

    def test_correct_gender_for_role(self):
        fam, individuals = self._make_family('M', 'F')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_correct_gender_for_role(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_correct_gender_for_role

    def test_husband_not_male(self):
        fam, individuals = self._make_family('F', 'F')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_correct_gender_for_role(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US21: Husband ID I01 is not male in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_husband_not_male

    def test_wife_not_female(self):
        fam, individuals = self._make_family('M', 'M')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_correct_gender_for_role(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US21: Wife ID I02 is not female in family F1!\n')
            self.assertEqual(result, False)
        # End with
    # End test_wife_not_female

    def test_both_incorrect_gender(self):
        fam, individuals = self._make_family('F', 'M')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_correct_gender_for_role(individuals)

            self.assertEqual(
                fake_out.getvalue(),
                'ERROR: US21: Husband ID I01 is not male in family F1!\n'
                'ERROR: US21: Wife ID I02 is not female in family F1!\n'
            )
            self.assertEqual(result, False)
        # End with
    # End test_both_incorrect_gender

# End Test_US21_CorrectGenderForRole


if __name__ == '__main__':
    unittest.main()
# End if
