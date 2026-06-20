# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual


class Test_US03_DeathBeforeBirth(unittest.TestCase):

    # Test Cases:
    # 1: Death date precedes birth date (FAIL)
    # 2: Death date after birth date (PASS)
    # 3: No death date (alive individual) (PASS)

    def test_death_before_birth(self):
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Thomas /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1950'
        individual.death = '1 JAN 1940'

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = individual.validate_death_after_birth()

            self.assertEqual(fake_out.getvalue(), 'ERROR: Individual ID I01 has a death date that precedes their birth date!\n')
            self.assertEqual(result, False)
        # End with
    # End test_death_before_birth

    def test_death_after_birth(self):
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Thomas /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1948'
        individual.death = '1 JAN 2020'

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = individual.validate_death_after_birth()

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_death_after_birth

    def test_no_death_date(self):
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Thomas /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1948'

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = individual.validate_death_after_birth()

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_no_death_date

# End Test_US03_DeathBeforeBirth


if __name__ == '__main__':
    unittest.main()
# End if
