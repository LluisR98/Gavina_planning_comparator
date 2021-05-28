# Gavina Planing Analyser
###### Version: 1.02

Little code to cross the planning Excels of "Gavina WiFi" and "Gavina WAN" projects, these projects are implemented by Telefónica and Generalitat de Catalunya.

---

## Requirements: 
- Python 3.x installed, programmed with Python 3.9.x.
- Excel Planning Scenario 1 and 2 converted to CSV.
- Excel Planning WAN converted to CSV.

## Code execution:
```
> planning-analyser.py --h
Usage: planning-analyser.py [-h] -wan WAN -scenario1 SCENARIO1 -scenario2 SCENARIO2

Tool to cross-check planning schedules of Gavina WAN and Gavina WiFI projects.

optional arguments:
  -h, --help            show this help message and exit

Required named arguments:
  -wan WAN              CSV WAN planning. Please put the WAN Admin in column number 3 (starting from 0).
  -scenario1 SCENARIO1  CSV WiFi planning scenario 1. Please put the WAN Admin in column number 6 (starting from 0).
  -scenario2 SCENARIO2  CSV WiFi planning scenario 2. Please put the WAN Admin in column number 3 (starting from 0).
```
## Preprocessing necessary to leave WAN administrative at:
Start counting from 0.
- File WAN Planning at column: 3.
- File WiFi Scenario 1 at column: 6.
- File WiFi Scenario 2 at column: 3.

## TODO:
- [ ] Replace column number to field name when importing data.
- [ ] Specify type of scenario.
- [ ] Specify date of installation if available.
