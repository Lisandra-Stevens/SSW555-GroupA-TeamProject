# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US02_BirthBeforeMarriage(unittest.TestCase):

    # Test Cases:
    # 1: Husband does not exist, Wife born before marriage
    # 2: Wife does not exist, Husband born before marriage
    # 3: Both exist, Wife born after marriage
    # 4: Both exist, Husband born after marriage
    # 5: Both exist, Both born after marriage

    def test_husband_doesnt_exist(self):
        # Create Wife Individual
        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = '14 AUG 1950'
        wife.add_spouse('F1')

        individuals = [wife]

        # Create the family
        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            #greeting("Alice")
            # Check the content (print adds a newline by default)
            #self.assertEqual(fake_out.getvalue(), "Hello, Alice!\n")

            # Call the unit under test
            result = fam.validate_birth_before_marriage(individuals)

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: Husband ID I01 does not exist in the list of individuals!\n")
            self.assertEqual(result, False)
        # End with
    # End test_husband_doesnt_exist


    def test_wife_doesnt_exist(self):
        # Create Husband Individual
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = '5 MAY 1948'
        husband.add_spouse('F1')

        individuals = [husband]

        # Create the family
        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            #greeting("Alice")
            # Check the content (print adds a newline by default)
            #self.assertEqual(fake_out.getvalue(), "Hello, Alice!\n")

            # Call the unit under test
            result = fam.validate_birth_before_marriage(individuals)

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: Wife ID I02 does not exist in the list of individuals!\n")
            self.assertEqual(result, False)
        # End with
    # End test_wife_doesnt_exist


    def test_both_exist_wife_born_before_marriage(self):
        # Create Husband Individual
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = '5 MAY 1948'
        husband.add_spouse('F1')

        # Create Wife Individual
        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = '14 AUG 1950'
        wife.add_spouse('F1')

        individuals = [husband, wife]

        # Create the family
        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1949'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            #greeting("Alice")
            # Check the content (print adds a newline by default)
            #self.assertEqual(fake_out.getvalue(), "Hello, Alice!\n")

            # Call the unit under test
            result = fam.validate_birth_before_marriage(individuals)

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: Wife ID I02 was married before their birthday!\n")
            self.assertEqual(result, False)
        # End with
    # End test_both_exist_wife_born_before_marriage


    def test_both_exist_husband_born_before_marriage(self):
        # Create Husband Individual
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = '5 MAY 1950'
        husband.add_spouse('F1')

        # Create Wife Individual
        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = '14 AUG 1948'
        wife.add_spouse('F1')

        individuals = [husband, wife]

        # Create the family
        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1949'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            #greeting("Alice")
            # Check the content (print adds a newline by default)
            #self.assertEqual(fake_out.getvalue(), "Hello, Alice!\n")

            # Call the unit under test
            result = fam.validate_birth_before_marriage(individuals)

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: Husband ID I01 was married before their birthday!\n")
            self.assertEqual(result, False)
        # End with
    # End test_both_exist_husband_born_before_marriage


    def test_both_exist_both_born_after_marriage(self):
        # Create Husband Individual
        husband = Individual()
        husband.uid = 'I01'
        husband.name = 'Thomas /Carter/'
        husband.gender = 'M'
        husband.birthday = '5 MAY 1948'
        husband.add_spouse('F1')

        # Create Wife Individual
        wife = Individual()
        wife.uid = 'I02'
        wife.name = 'Evelyn /Carter/'
        wife.gender = 'F'
        wife.birthday = '14 AUG 1950'
        wife.add_spouse('F1')

        individuals = [husband, wife]

        # Create the family
        fam = Family()
        fam.uid = 'F1'
        fam.married = '22 JUN 1952'
        fam.husband_id = 'I01'
        fam.wife_id = 'I02'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            #greeting("Alice")
            # Check the content (print adds a newline by default)
            #self.assertEqual(fake_out.getvalue(), "Hello, Alice!\n")

            # Call the unit under test
            result = fam.validate_birth_before_marriage(individuals)

            # Check the content of the print statement
            self.assertEqual(result, True)
        # End with
    # End test_both_exist_husband_born_before_marriage
# End Test_US02_BirthBeforeMarriage


if __name__ == '__main__':
    unittest.main()
# End if