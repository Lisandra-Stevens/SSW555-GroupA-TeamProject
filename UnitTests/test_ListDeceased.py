# System Imports
from unittest.mock import patch
import unittest
import io
import sys
import os

# Make the parent directory importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Local Imports
from ged_validator import GEDCOM_Validator
from individual import Individual
from family import Family

def make_individual(uid, name, gender, birthday, death=None, spouse_fams=None):
    indi = Individual()
    indi.uid = uid
    indi.name = name
    indi.gender = gender
    indi.birthday = birthday

    if death is not None:
        indi.death = death
    # End if

    if spouse_fams:
        for fam_id in spouse_fams:
            indi.add_spouse(fam_id)
        # End for
    # End if

    return indi
# End make_individual


class Test_US29_ListDeceased(unittest.TestCase):

    # Test Cases:
    # 1: No deceased individuals
    # 2: One deceased individual
    # 3: Two deceased individuals

    def setUp(self):
        self.validator = GEDCOM_Validator()

    def test_no_deceased(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_deceased_individuals()

            self.assertEqual([], result)
        # End with
    # End test_no_deceased

    def test_one_deceased(self):
        self.validator.individuals = []
        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        self.validator.individuals.append(indi1)

        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990', death='08 JAN 2025')
        self.validator.individuals.append(indi2)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_deceased_individuals()

            self.assertEqual([indi2], result)
        # End with
    # End test_one_deceased

    def test_two_deceased(self):
        self.validator.individuals = []
        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', death='09 JUN 2005')
        self.validator.individuals.append(indi1)

        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990', death='08 JAN 2025')
        self.validator.individuals.append(indi2)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_deceased_individuals()

            self.assertEqual([indi1, indi2], result)
        # End with
    # End test_two_deceased

# End Test_US29_ListDeceased


if __name__ == '__main__':
    unittest.main()
# End if
