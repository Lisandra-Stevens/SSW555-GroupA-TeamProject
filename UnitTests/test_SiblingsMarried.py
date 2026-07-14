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

def make_individual(uid, name, gender, birthday, death=None, spouse_fams=None, child_famc=None):
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

    if child_famc:
        for fam_id in child_famc:
            indi.add_child(fam_id)
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


class Test_US18_SiblingsCantMarry(unittest.TestCase):

    # Test Cases:
    # 1: Husband and wife are not siblings
    # 2: Husband and wire are siblings

    def test_husband_wife_not_siblings(self):
        individuals = []
        individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', child_famc=['F02']))
        individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990', child_famc=['F03']))
        
        uut = make_family('F01', '22 JUN 1952', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = uut.validate_no_sibling_marriage(individuals)
            
            self.assertEqual(True, result)
        # End with
    # End test_husband_wife_not_siblings

    def test_husband_wife_siblings(self):
        individuals = []
        individuals.append(make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', child_famc=['F02']))
        individuals.append(make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990', child_famc=['F02']))
        
        uut = make_family('F01', '22 JUN 1952', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = uut.validate_no_sibling_marriage(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US18: Family ID F01 has married siblings from family F02!\n')
            self.assertEqual(False, result)
        # End with
    # End test_husband_wife_siblings

# End Test_US18_SiblingsCantMarry


if __name__ == '__main__':
    unittest.main()
# End if
