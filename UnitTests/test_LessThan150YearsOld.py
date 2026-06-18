# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual


class Test_US07_LessThan150YearsOld(unittest.TestCase):

    # Test Cases:
    # 1: Individual is less than 150 years old with no death date
    # 2: Individual is less than 150 years old with death date
    # 3: Individual is over 150 years old with no death date
    # 4: Individual is over 150 years old with death date

    def test_less_than_150_no_death_date(self):
        # Create Wife Individual
        indi = Individual()
        indi.uid = 'I32'
        indi.name = 'Evelyn /Carter/'
        indi.gender = 'F'
        indi.birthday = '14 AUG 1950'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # Call the unit under test
            result = indi.validate_less_than_150()

            # Check the content of the print statement
            self.assertEqual(result, True)
        # End with
    # End test_less_than_150_no_death_date


    def test_less_than_150_with_death_date(self):
        # Create Wife Individual
        indi = Individual()
        indi.uid = 'I32'
        indi.name = 'Evelyn /Carter/'
        indi.gender = 'F'
        indi.birthday = '14 AUG 1950'
        indi.death = '17 JUN 2000'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # Call the unit under test
            result = indi.validate_less_than_150()

            # Check the content of the print statement
            self.assertEqual(result, True)
        # End with
    # End test_less_than_150_no_death_date


    def test_over_150_no_death_date(self):
        # Create Wife Individual
        indi = Individual()
        indi.uid = 'I32'
        indi.name = 'Evelyn /Carter/'
        indi.gender = 'F'
        indi.birthday = '14 AUG 1850'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # Call the unit under test
            result = indi.validate_less_than_150()

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: ID I32 is over 150 years old!\n")
            self.assertEqual(result, False)
        # End with
    # End test_over_150_no_death_date


    def test_over_150_with_death_date(self):
        # Create Wife Individual
        indi = Individual()
        indi.uid = 'I32'
        indi.name = 'Evelyn /Carter/'
        indi.gender = 'F'
        indi.birthday = '14 AUG 1850'
        indi.death = '17 JUN 2010'

        # Redirect standard output to a string buffer
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # Call the unit under test
            result = indi.validate_less_than_150()

            # Check the content of the print statement
            self.assertEqual(fake_out.getvalue(), "ERROR: ID I32 is over 150 years old!\n")
            self.assertEqual(result, False)
        # End with
    # End test_over_150_no_death_date

# End Test_US07_LessThan150YearsOld