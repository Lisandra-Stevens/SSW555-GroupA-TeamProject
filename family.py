# System Imports
from datetime import datetime, timedelta

# Local imports
# None

class Family:

    def __init__(self,
                 uid=None,
                 married=None,
                 divorced=None,
                 husband_id=None,
                 wife_id=None,
                 children=None
        ):
        # Store the fields we need for individuals
        self._uid = uid
        # Dates
        self._married = married
        self._divorced = divorced
        # IDs
        self._husband_id = husband_id
        self._wife_id = wife_id
        # List of children IDs
        self._children = [] if children is None else children
    # End __init__

    ###########################################################################
    #
    # Validators
    #
    ###########################################################################

    def validate_birth_before_marriage(self, individuals):
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        if husband is not None:
            if husband.birthday >= self._married:
                print(f'ERROR: Husband ID {self._husband_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: Husband ID {self._husband_id} does not exist in the list of individuals!')
            result = False

        if wife is not None:
            if wife.birthday >= self._married:
                print(f'ERROR: Wife ID {self._wife_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: Wife ID {self._wife_id} does not exist in the list of individuals!')
            result = False

        return result
    # End validate_birth_before_marriage

    def validate_children_birth_dates(self, individuals):
        result = True

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None:
                print(f'ERROR: Child ID {child_id} does not exist in the list of individuals!')
                result = False
                continue

            if child.birthday is None:
                continue

            if self._married is not None and child.birthday < self._married:
                print(f'ERROR: Child ID {child_id} was born before the marriage of their parents in family {self._uid}!')
                result = False

            if self._divorced is not None:
                nine_months_after_divorce = self._divorced + timedelta(days=274)
                if child.birthday > nine_months_after_divorce:
                    print(f'ERROR: Child ID {child_id} was born more than 9 months after the divorce of their parents in family {self._uid}!')
                    result = False

        return result
    # End validate_children_birth_dates

    def validate_multiple_births(self, individuals):
        result = True
        birth_date_counts = {}

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None or child.birthday is None:
                continue

            birth_date = child.birthday.date()

            if birth_date not in birth_date_counts:
                birth_date_counts[birth_date] = []

            birth_date_counts[birth_date].append(child_id)

        for birth_date, children in birth_date_counts.items():
            if len(children) > 5:
                print(f'ERROR: Family ID {self._uid} has more than five children born on {birth_date}!')
                result = False

        return result
    # End validate_multiple_births

    def validate(self, individuals):
        result = True

        result &= self.validate_birth_before_marriage(individuals)
        result &= self.validate_children_birth_dates(individuals)
        result &= self.validate_multiple_births(individuals)

        return result
    # End validate
