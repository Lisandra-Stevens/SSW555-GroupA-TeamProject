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
        for child in children:
            fam.add_children(child)
        # End for
    # End if

    return fam
# End make_family


class Test_US33_ListOrphans(unittest.TestCase):

    # Test Cases:
    # 1: No parents dead - No orphans
    # 2: One parent dead - No orphans
    # 3: Both parents dead - Orphans

    def setUp(self):
        self.validator = GEDCOM_Validator()
    # End setUp

    def test_no_dead_parents(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))
        self.validator.individuals.append(make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 2000'))

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02', children=['I03']))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_orphans()
            
            self.assertEqual([], result)
        # End with
    # End test_no_dead_parents

    def test_one_dead_parents(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', death='17 JUN 2002'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990'))
        self.validator.individuals.append(make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 2000'))

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02', children=['I03']))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_orphans()

            self.assertEqual([], result)
        # End with
    # End test_one_dead_parents

    def test_both_dead_parents(self):
        self.validator.individuals = []
        self.validator.individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', death='17 JUN 2002'))
        self.validator.individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990', death='17 JUN 2002'))
        child = make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 2000')
        self.validator.individuals.append(child)

        self.validator.families = []
        self.validator.families.append(make_family('F01', '22 JUN 1952', 'I01', 'I02', children=['I03']))

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_orphans()

            self.assertIn(child, result)
        # End with
    # End test_both_dead_parents

# End Test_US33_ListOrphans


if __name__ == '__main__':
    unittest.main()
# End if
