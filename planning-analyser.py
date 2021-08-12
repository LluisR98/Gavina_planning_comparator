#
# Requirements: 
#   - Python 3.x installed, programmed with Python 3.9.x.
#   - Excel Planning Scenario 1 and 2 converted to CSV.
#   - Excel Planning WAN converted to CSV.
#
# Code execution:
#   - $ planning-analyser.py --wan [WAN_planning.csv] --scenario1 [Scenario_1_planning.csv] --scenario2 [Scenario_2_planning.csv]
#

# Import time
import argparse
import csv
import sys
import os

# Parse arguments 
def get_args():
    parser = argparse.ArgumentParser(description="Tool to cross-check planning schedules of Gavina WAN and Gavina WiFI projects.")
    requiredvalues = parser.add_argument_group('Required arguments')
    requiredvalues.add_argument('--wan', required=True, help='CSV WAN planning.')
    requiredvalues.add_argument('--scenario1', required=True, help='CSV WiFi planning scenario 1.')
    requiredvalues.add_argument('--scenario2', required=True, help='CSV WiFi planning scenario 2.')
    args = parser.parse_args()
    return args

# Main menu
if __name__ == "__main__":
    args = get_args()

    wan_data = []
    wan_school_data = []
    wan_admin = []

    scenario1_data = []
    scenario1_school_data = []
    scenario1_admin = []
    scenario1_transformed = []

    scenario2_data = []
    scenario2_school_data = []
    scenario2_admin = []
    scenario2_transformed = []

    admin_scenario2_match = []
    admin_scenario1_match = []
    wifi_transformed_filename = "WAN-WiFi_Analysed.csv"
    csv_header = ['WAN','School Code','School Name','Type of scenario','Date']

# Check if all parameters contain something
    if args.scenario1 != "none" and args.scenario2 != "none" and args.wan != "none":

# Check if files exist
        if os.path.isfile(args.scenario1) and os.path.isfile(args.scenario2) and os.path.isfile(args.wan):
            print()

# CSV WAN
            try:
                with open(args.wan, 'r', encoding='UTF-8-sig') as wan_planning:
                    wan = csv.reader(wan_planning, delimiter=';')
                    lines = 0
                    for row in wan:
                        if lines == 0:
                            wan_columns = (row)
                            lines += 1
                        else:
                            wan_data.append(row)
                            lines += 1
#                    print(wan_columns)       # If execution fails, add comments to try/except and see how it is stored.
                    wan_index = wan_columns.index("ADMIN")
                    wan_cod_centro = wan_columns.index("COD_CENTRO")
                    wan_nom_centro = wan_columns.index("NOM_SEDE")
                for wan_school in wan_data:
# Correct the length of the value
                    if len(wan_school[wan_index]) != 14:
                        wan_school[wan_index] = '0' + wan_school[wan_index]
                    wan_school_data.append(wan_school[wan_index] + ';' + wan_school[wan_cod_centro] + ';' + wan_school[wan_nom_centro])
                    wan_admin.append(wan_school[wan_index])
            except:
                print("Error while processing file: " + args.wan + ".")
                sys.exit()

# CSV Scenario 1
            try:
                with open(args.scenario1, 'r', encoding='UTF-8-sig') as scenario1_planning:
                    scenario1 = csv.reader(scenario1_planning, delimiter=';')
                    lines = 0
                    for row in scenario1:
                        if lines == 0:
                            scenario1_columns = (row)
                            lines += 1
                        else:
                            scenario1_data.append(row)
                            lines += 1
#                    print(scenario1_columns)       # If execution fails, add comments to try/except and see how it is stored.
                    scenario1_index = scenario1_columns.index("Propietario conectividad")
                    scenario1_cod_centro = scenario1_columns.index("Codi")
                    scenario1_nom_centro = scenario1_columns.index("Centre")
                for scenario1_school in scenario1_data:
# Correct the length of the value
                    if len(scenario1_school[scenario1_index]) != 14:
                        wan_school[scenario1_index] = '0' + scenario1_school[scenario1_index]
                    scenario1_school_data.append(scenario1_school[scenario1_index] + ';' + scenario1_school[scenario1_cod_centro] + ';' + scenario1_school[scenario1_nom_centro] + ';Scenario 1')
                    scenario1_admin.append(scenario1_school[scenario1_index])
            except:
                print("Error while processing file: " + args.scenario1 + ".")
                sys.exit()

# CSV Scenario 2
            try:
                with open(args.scenario2, 'r', encoding='UTF-8-sig') as scenario2_planning:
                    scenario2 = csv.reader(scenario2_planning, delimiter=';')
                    lines = 0
                    for row in scenario2:
                        if lines == 0:
                            scenario2_columns = (row)
                            lines += 1
                        else:
                            scenario2_data.append(row)
                            lines += 1
#                    print(scenario2_columns)       # If execution fails, add comments to try/except and see how it is stored.
                    scenario2_index = scenario2_columns.index("WAN")
                    scenario2_cod_centro = scenario2_columns.index("Codi")
                    scenario2_nom_centro = scenario2_columns.index("Centre")
                    scenario2_install = scenario2_columns.index("Data")
                for scenario2_school in scenario2_data:
# Correct the length of the value
                    if len(scenario2_school[scenario2_index]) != 14:
                        wan_school[scenario2_index] = '0' + scenario2_school[scenario2_index]
                    scenario2_school_data.append(scenario2_school[scenario2_index] + ';' + scenario2_school[scenario2_cod_centro] + ';' + scenario2_school[scenario2_nom_centro] + ';Scenario 2;' + scenario2_school[scenario2_install])
                    scenario2_admin.append(scenario2_school[scenario2_index])
            except:
                print("Error while processing file: " + args.scenario2 + ".")
                sys.exit()

# Cross-data time and avoid duplicates
            for admin in wan_admin:
                if admin in scenario2_admin:
                    admin_scenario2_match.append(admin)
                if admin in scenario1_admin and admin not in scenario2_admin:
                    admin_scenario1_match.append(admin)

# Check if file exists
            if os.path.isfile(wifi_transformed_filename):
                ask = input("WARNING!\n\nThis file already exists!\n\nDo you want to delete it and create a new one with the current version? [y/N] ")
                if ask == "Y" or ask == "y":
                    os.remove(wifi_transformed_filename)
                else:
                    print("No file has been modified.")
                    sys.exit()

# Create the final CSV
            try:
                myData = [csv_header]
                result = open(wifi_transformed_filename, 'w')
                with result:
                    writer = csv.writer(result)
# Add Scenario 2 matches
                    for school2 in admin_scenario2_match:
                        for i in scenario2_school_data:
                            temp = i.split(";")
                            if temp[0] == school2:
                                myData.append(temp)
# Add Scenario 1 matches
                    for school1 in admin_scenario1_match:
                        for i in scenario1_school_data:
                            temp = i.split(";")
                            if temp[0] == school1:
                                if temp[0] != '':
                                    myData.append(temp)
# Write the values ​​in the final file
                    writer.writerows(myData)
                    print("\nSuccess!")
            except:
                print("Error while processing the file: " + wifi_transformed_filename + ".")
                sys.exit()

        else:
            print("Some of the requested files do not exist, please check it.")

    else:
        print("Any of the arguments are wrong, please check it.")