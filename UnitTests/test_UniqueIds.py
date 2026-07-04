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

def make_family(uid, married, husband_id, wife_id, children=None):
    fam = Family()
    fam.uid = uid
    fam.married = married
    fam.husband_id = husband_id
    fam.wife_id = wife_id

    if (children is not None):
        fam.add_children('I03')
    # End if

    return fam
# End make_family


class Test_US22_UniqueIds(unittest.TestCase):

    # Test Cases:
    # 1: All unique IDs for families and individuals
    # 2: All unique IDs for families, matching unique IDs for individuals
    # 3: All unique IDs for individuals, matching unique IDs for families
    # 4: Matching unique IDs for individuals and families

    def setUp(self):
        self.validator = GEDCOM_Validator()

    def test_unique_ids_for_fam_and_individ(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02'))
        self.validator.families.append(make_family('F02', '22 MAY 2021', 'I03', 'I04'))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.validate_unique_ids()
            
            self.assertEqual(True, result)
        # End with
    # End test_unique_ids_for_fam_and_individ

    def test_unique_family_uid_matching_individ_uid(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I01', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02'))
        self.validator.families.append(make_family('F02', '22 MAY 2021', 'I03', 'I04'))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.validate_unique_ids()

            self.assertEqual(fake_out.getvalue(), 'ERROR: US22: Individual UID I01 is a duplicate UID!\n')
            self.assertEqual(False, result)
        # End with
    # End test_unique_family_uid_matching_individ_uid

    def test_unique_individ_uid_matching_family_uid(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))

        self.validator.families = []
        self.validator.families.append(make_family('F02', '22 JUN 1952', 'I01', 'I02'))
        self.validator.families.append(make_family('F02', '22 MAY 2021', 'I03', 'I04'))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.validate_unique_ids()

            self.assertEqual(fake_out.getvalue(), 'ERROR: US22: Family UID F02 is a duplicate UID!\n')
            self.assertEqual(False, result)
        # End with
    # End test_unique_individ_uid_matching_family_uid

    def test_matching_uid_family_and_individual(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I02', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02'))
        self.validator.families.append(make_family('F01', '22 MAY 2021', 'I03', 'I04'))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.validate_unique_ids()

            self.assertEqual(fake_out.getvalue(), 'ERROR: US22: Individual UID I02 is a duplicate UID!\nERROR: US22: Family UID F01 is a duplicate UID!\n')
            self.assertEqual(False, result)
        # End with
    # End test_matching_uid_family_and_individual
# End Test_US22_UniqueIds


if __name__ == '__main__':
    unittest.main()
# End if
