# System Imports
from unittest.mock import patch
import unittest
import io
import sys
import os

# Make the parent directory importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Local Imports
from individual import Individual
from ged_validator import GEDCOM_Validator


def make_individual(uid, name, gender, birthday, death=None, spouse_fams=None):
    indi = Individual()
    indi.uid = uid
    indi.name = name
    indi.gender = gender
    indi.birthday = birthday
    if death is not None:
        indi.death = death
    if spouse_fams:
        for fam_id in spouse_fams:
            indi.add_spouse(fam_id)
    return indi


class Test_US31_LivingUnmarriedOver30(unittest.TestCase):

    # Test Cases:
    # 1: Living person over 30, no spouse -> included
    # 2: Living person over 30, has spouse -> NOT included
    # 3: Living person under 30, no spouse -> NOT included
    # 4: Deceased person over 30, no spouse -> NOT included
    # 5: No qualifying individuals -> returns empty list
    # 6: Multiple qualifying individuals -> all returned

    def setUp(self):
        self.validator = GEDCOM_Validator()

    def test_living_over_30_no_spouse_included(self):
        indi = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertIn(indi, result)
    # End test_living_over_30_no_spouse_included

    def test_living_over_30_has_spouse_excluded(self):
        indi = make_individual('I02', 'Thomas /Carter/', 'M', '5 MAY 1948', spouse_fams=['F1'])
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertNotIn(indi, result)
    # End test_living_over_30_has_spouse_excluded

    def test_living_under_30_no_spouse_excluded(self):
        indi = make_individual('I03', 'Emma /Carter/', 'F', '21 JUN 2005')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertNotIn(indi, result)
    # End test_living_under_30_no_spouse_excluded

    def test_deceased_over_30_no_spouse_excluded(self):
        indi = make_individual('I04', 'Laura /Bennett/', 'F', '9 SEP 1978', death='18 JAN 2020')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertNotIn(indi, result)
    # End test_deceased_over_30_no_spouse_excluded

    def test_no_qualifying_individuals_returns_empty(self):
        indi = make_individual('I05', 'Noah /Carter/', 'M', '7 APR 2019')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertEqual(result, [])
    # End test_no_qualifying_individuals_returns_empty

    def test_multiple_qualifying_individuals_all_returned(self):
        indi1 = make_individual('I06', 'Alice /Smith/', 'F', '10 JAN 1980')
        indi2 = make_individual('I07', 'Bob /Jones/', 'M', '22 NOV 1975')
        # Non-qualifying: married, under 30, deceased
        indi3 = make_individual('I08', 'Carol /Adams/', 'F', '5 MAR 1970', spouse_fams=['F2'])
        indi4 = make_individual('I09', 'Dave /Hill/', 'M', '1 JUN 2005')
        self.validator.individuals = [indi1, indi2, indi3, indi4]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_unmarried_over_30()

        self.assertIn(indi1, result)
        self.assertIn(indi2, result)
        self.assertNotIn(indi3, result)
        self.assertNotIn(indi4, result)
        self.assertEqual(len(result), 2)
    # End test_multiple_qualifying_individuals_all_returned

# End Test_US31_LivingUnmarriedOver30


if __name__ == '__main__':
    unittest.main()
# End if
