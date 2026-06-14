# System Imports
from prettytable import PrettyTable
from datetime import datetime
import sys
import os
import re

# Local imports
# None

class GEDCOM_Validator:

    def __init__(self):
        self.valid_tags = {
            'INDI': 0,
            'NAME': 1,
            'SEX':  1,
            'BIRT': 1,
            'DEAT': 1,
            'FAMC': 1,
            'FAMS': 1,
            'FAM':  0,
            'MARR': 1,
            'HUSB': 1,
            'WIFE': 1,
            'CHIL': 1,
            'DIV':  1,
            'DATE': 2,
            'HEAD': 0,
            'TRLR': 0,
            'NOTE': 0
        }

        self.individuals = {}
        self.families = {}

        self.current_record = None
        self.current_record_type = None
        self.pending_tag = None
    # End __init__

    def check_tag_valid(self, tag, level):
        # Default value is the tag is not valid or 'N'
        ret_val = 'N'

        # Check to see if the tag is in the valid list
        if (tag in self.valid_tags):
            # The tag is valid, does it match the valid level though
            if (level == str(self.valid_tags[tag])):
                ret_val = 'Y'
            # End if
        # End if

        return ret_val
    # End check_tag_valid

    def get_year_difference(self, start_date, end_date):
        # Subtract years, then subtract 1 if the end date hasn't crossed the birthday/anniversary yet
        has_not_passed = (end_date.month, end_date.day) < (start_date.month, start_date.day)
        years = end_date.year - start_date.year - has_not_passed

        return years
    # End get_year_difference

    def print_invidiuals(self):
        # Start the table and add the field names
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

        for uid,individual in self.individuals.items():
            fields = []
            fields.append(individual['id'])
            fields.append(individual['name'])
            fields.append(individual['sex'])

            birth_dt = datetime.strptime(individual['birt'], "%d %b %Y")
            fields.append(birth_dt.strftime("%Y-%m-%d"))

            if (individual['deat'] is None):
                # As the individual is not dead, we can use the current date for age
                current_dt = datetime.now()
                fields.append(self.get_year_difference(birth_dt, current_dt))

                fields.append('True')
                fields.append('N/A')

            else:
                death_dt = datetime.strptime(individual['deat'], "%d %b %Y")

                fields.append(self.get_year_difference(birth_dt, death_dt))
                fields.append('False')
                fields.append(death_dt.strftime("%Y-%m-%d"))
            # End if-else

            data = individual['famc']
            fields.append(data if len(data) != 0 else 'N/A')
            data = individual['fams']
            fields.append(data if len(data) != 0 else 'N/A')

            table.add_row(fields)
        # End for

        print(table.get_string())
    # End print_invidiuals

    def print_family(self):
        # Start the table and add the field names
        table = PrettyTable()
        table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

        for fid,family in self.families.items():
            fields = []
            fields.append(family['id'])
            
            marr_dt = datetime.strptime(family['marr'], "%d %b %Y")
            fields.append(marr_dt.strftime("%Y-%m-%d"))

            if (family['div'] is None):
                fields.append('N/A')
            else:
                div_dt = datetime.strptime(family['div'], "%d %b %Y")
                fields.append(div_dt.strftime("%Y-%m-%d"))
            # End if-else

            fields.append(family['husb'])
            fields.append(self.individuals[family['husb']]['name'])
            fields.append(family['wife'])
            fields.append(self.individuals[family['wife']]['name'])
            fields.append(family['chil'])
            table.add_row(fields)
        # End for

        print(table.get_string())
    # End print_family

    def run(self, gedcom_file):
        print(gedcom_file)

        # Check if the input file exists, if it doesnt we stop execution
        if not os.path.exists(gedcom_file):
            print(f'ERROR: Provided file ({gedcom_file}) does not exist!')
            return
        # End if

        # Open the file
        with open(gedcom_file, 'r') as fileh:
            for line in fileh:
                # Remove special chars!
                strip_line = line.strip()

                # First print
                # print(f'--> {strip_line}')

                # Split the line by spaces
                split_line = strip_line.split(' ', maxsplit=2)
                level = split_line[0]

                # There are two types of tags that do not match the standard format
                if (('INDI' in line) or ('FAM' in line)) and (level == '0'):
                    arguments = split_line[1]
                    tag = split_line[2]
                else:
                    tag = split_line[1]
                    arguments = split_line[2] if len(split_line) >= 3 else ''
                # End if-else

                # Post processing!
                arguments = arguments.strip('@')

                # Check if the tag is valid!
                valid = self.check_tag_valid(tag, level)

                # Second print - added newline for readability
                # print(f'<-- {level}|{tag}|{valid}|{arguments}\n')

                # Build individual/family collections
                if level == '0':
                    if tag == 'INDI':
                        uid = int(re.search(r'\d+', arguments).group())
                        iid = arguments.strip('@')
                        self.current_record = {'id': iid, 'uid': uid, 'name': None, 'sex': None,
                                               'birt': None, 'deat': None, 'famc': [], 'fams': []}
                        self.individuals[arguments] = self.current_record
                        self.current_record_type = 'INDI'
                    elif tag == 'FAM':
                        fid = int(re.search(r'\d+', arguments).group())
                        iid = arguments.strip('@')
                        self.current_record = {'id': iid, 'fid': fid, 'marr': None, 'div': None,
                                               'husb': None, 'wife': None, 'chil': []}
                        self.families[arguments] = self.current_record
                        self.current_record_type = 'FAM'
                    else:
                        self.current_record = None
                        self.current_record_type = None
                    self.pending_tag = None

                elif level == '1' and self.current_record is not None:
                    if tag in ('NAME', 'SEX', 'HUSB', 'WIFE'):
                        self.current_record[tag.lower()] = arguments
                    elif tag in ('FAMC', 'FAMS'):
                        self.current_record[tag.lower()].append(arguments)
                    elif tag == 'CHIL':
                        self.current_record['chil'].append(arguments)
                    elif tag in ('BIRT', 'DEAT', 'MARR', 'DIV'):
                        self.pending_tag = tag.lower()

                elif level == '2' and tag == 'DATE' and self.pending_tag and self.current_record is not None:
                    self.current_record[self.pending_tag] = arguments
                    self.pending_tag = None
            # End for
        # End with

        # Now print the tables
        self.print_invidiuals()
        print()
        self.print_family()
    # End run

# End GEDCOM_Validator


if __name__ == '__main__':
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="The arguments for the GEDCOM Validator.")
    parser.add_argument("-g", "--gedcom", required=True, help="Path to the GEDCOM file to process")
    args = parser.parse_args()

    # Call the run
    gedcom_val = GEDCOM_Validator()
    gedcom_val.run(args.gedcom)
# End if