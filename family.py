# System Imports
from datetime import datetime

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

        # First, get the individuals in the marriage
        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        # Now we verify they exist!
        if (husband is not None):
            # Check the dates
            if (husband.birthday >= self._married):
                print(f'ERROR: Husband ID {self._husband_id} was married before their birthday!')
                result = False
            # End if

        else:
            print(f'ERROR: Husband ID {self._husband_id} does not exist in the list of individuals!')
            # Validation should fail if there is no data on the individual
            result = False
        # End if-else

        # Now we verify they exist!
        if (wife is not None):
            # Check the dates
            if (wife.birthday >= self._married):
                print(f'ERROR: Wife ID {self._wife_id} was married before their birthday!')
                result = False
            # End if

        else:
            print(f'ERROR: Wife ID {self._wife_id} does not exist in the list of individuals!')
            # Validation should fail if there is no data on the individual
            result = False
        # End if-else

        return result
    # End validate_birth_before_marriage

    def validate(self, individuals):
        result = True

        # Validate birth before marriage
        result &= self.validate_birth_before_marriage(individuals)

        return result
    # End validate

    ###########################################################################
    #
    # Getters and Setters
    #
    ###########################################################################

    def set_tag_value(self, tag, value):
        # Since we are processing GEDCOM tags
        # This method will take in a tag and value abd assign it to the
        # proper python variable
        pass

        if (tag == 'FAM'):
            self.uid = value

        elif (tag == 'MARR'):
            self.married = value

        elif (tag == 'DIV'):
            self.divorced = value

        elif (tag == 'HUSB'):
            self.husband_id = value

        elif (tag == 'WIFE'):
            self.wife_id = value

        elif (tag == 'CHIL'):
            self.add_children(value)

        else:
            print(f'Unknown tag for family {tag}')
        # End if-elif-else

    # End set_tag_value

    @property
    def uid(self):
        return self._uid
    # End uid

    @uid.setter
    def uid(self, value):
        self._uid = value
    # End uid setter

    @property
    def married(self):
        return self._married
    # End married

    @married.setter
    def married(self, value):
        # The married will be converted from a string to a datetime obj
        self._married = datetime.strptime(value, "%d %b %Y")
    # End married setter

    @property
    def divorced(self):
        return self._divorced
    # End divorced

    @divorced.setter
    def divorced(self, value):
        # The divorced will be converted from a string to a datetime obj
        self._divorced = datetime.strptime(value, "%d %b %Y")
    # End divorced setter

    @property
    def husband_id(self):
        return self._husband_id
    # End husband_id

    @husband_id.setter
    def husband_id(self, value):
        self._husband_id = value
    # End husband_id setter

    @property
    def wife_id(self):
        return self._wife_id
    # End wife_id

    @wife_id.setter
    def wife_id(self, value):
        self._wife_id = value
    # End wife_id setter

    @property
    def children(self):
        return self._children
    # End child

    @children.setter
    def children(self, value):
        self._children = value
    # End child setter

    def add_children(self, value):
        self._children.append(value)
    # End add_child

# End individual