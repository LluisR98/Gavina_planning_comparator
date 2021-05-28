#
# Requirements: 
#   - Python 3.x installed, programmed with Python 3.9.x.
#   - Excel Planning Scenario 1 and 2 converted to CSV.
#   - Excel Planning WAN converted to CSV.
#
# Code execution:
#   - $ planning-analyser.py --wan [WAN_planning.csv] --scenario1 [Scenario_1_planning.csv] --scenario2 [Scenario_2_planning.csv]
#
# Preprocessing necessary to leave administrative at:
# Start counting from 0.
#   - File WAN Planning at column: 3.
#   - File WiFi Scenario 1 at column: 6.
#   - File WiFi Scenario 2 at column: 3.
#

# Import time
import argparse
import os
import sys
from csv import reader
from csv import writer

# Parse arguments 
def get_args():
    parser = argparse.ArgumentParser(description="Tool to cross-check planning schedules of Gavina WAN and Gavina WiFI projects.")
    requiredvalues = parser.add_argument_group('Required arguments')
    requiredvalues.add_argument('-wan', required=True, help='CSV WAN planning. Please put the WAN Admin in column number 3 (starting from 0).')
    requiredvalues.add_argument('-scenario1', required=True, help='CSV WiFi planning scenario 1. Please put the WAN Admin in column number 6 (starting from 0).')
    requiredvalues.add_argument('-scenario2', required=True, help='CSV WiFi planning scenario 2. Please put the WAN Admin in column number 3 (starting from 0).')
    args = parser.parse_args()
    return args

# Main menu
if __name__ == "__main__":

    args = get_args()
    scenario1_list = []
    scenario2_list = []
    wan_list = []
    wifi_transformed = []
    wifi_transformed_analysed = "WiFi_Transformed.csv"

# Check if all parameters contain something
    if args.scenario1 != "none" and args.scenario2 != "none" and args.wan != "none":

# Check if files exist
        if os.path.isfile(args.scenario1) and os.path.isfile(args.scenario2) and os.path.isfile(args.wan):

# Open CSV files and import WAN numbers
            try:
                with open(args.scenario1, 'r', encoding="utf8") as scenario1:
                    scenario1_planning = reader(scenario1, delimiter=';')
                    for school in scenario1_planning:
                        scenario1_list.append(school[6])
            except:
                print("ERROR: An error occurred while processing the file: " + args.scenario1)

            try:
                with open(args.scenario2, 'r', encoding="utf8") as scenario2:
                    scenario2_planning = reader(scenario2, delimiter=';')
                    for school in scenario2_planning:
                        scenario2_list.append(school[3])
            except:
                print("ERROR: An error occurred while processing the file: " + args.scenario2)

            try:
                with open(args.wan, 'r', encoding="utf8") as wan:
                    wan_planning = reader(wan, delimiter=';')
                    for school in wan_planning:
                        wan_list.append(school[3])
            except:
                print("ERROR: An error occurred while processing the file: " + args.wan)

# Check the existence of the WAN numbers
            for admin_wan in wan_list:
                if admin_wan in scenario2_list and admin_wan not in wifi_transformed:
                    wifi_transformed.append(admin_wan)
                if admin_wan in scenario1_list and admin_wan not in wifi_transformed:
                    wifi_transformed.append(admin_wan)

# Check the results and generate a CSV with the results 
            if len(wifi_transformed) != 0:

# Check if the analysed file exists and delete it if necessary
                if os.path.isfile(wifi_transformed_analysed):
                    ask = input("WARNING!\n\nThis file already exists!\n\nDo you want to delete it and create a new one with the current version? [Y / N] ")
                    if ask == "Y" or ask == "y":
                        os.remove(wifi_transformed_analysed)
                    elif ask == "N" or ask == "n":
                        print("No file has been modified.")
                        sys.exit()
                    else:
                        print("The requested character [Y] has not been detected. No file has been modified.")
                        sys.exit()

                try:
                    with open(wifi_transformed_analysed, 'w', encoding="utf8", newline='') as output:
                        result = writer(output)
                        result.writerow(['WAN','Type of scenario','Date'])
                        for school in wifi_transformed:
                            result.writerow([school])
                        print("Success!")
                except:
                    print("ERROR: An error occurred while processing the file: " + wifi_transformed_analysed)

            else:
                print("No matches found!")

        else:
            print("Some of the requested files do not exist, please check it.")

    else:
        print("Any of the arguments are wrong, please check it.")