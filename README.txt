Flow Log Tagging Program (AWS Networks)

Created by Nathaniel Kusiolek in August 2024
This program parses flow log data (in AWS VPC Flow Log format) and maps rows to tags based on a lookup table. 
It then generates an output file that contains the counts of matches for each tag and the counts of matches for each port/protocol combination.

List of files:
flow_log_tagger.py - the actual tagging program, all the code is in this file with multiple helper functions
lookup_table.csv - input excel file, 3 columns for destination port, protocol, and tag
flow_logs.txt - input text file, list of flow log entries in AWS VPC format
output.txt - output text file, includes tag, port, and protocol counts

Instructions:
1. Open terminal in project folder, then run the following command
2. python flow_log_tagger.py
3. Output.txt should show the correct data
NOTE: You can modify the lookup table and flow logs as much as you like, but make sure to keep the text formatted as it was originally.
The files must have the correct file names for the above command to work. Will need to modify if you want to use different input file names.

Assumptions:
    Flow Logs: Only default AWS VPC flow logs in version 2 format are supported.
    Lookup Table: CSV file with the headers dstport, protocol, and tag. The protocol is case-insensitive.
    Tagging: Flow log entries that do not match any lookup table entry are considered "Untagged."
    Protocol Mapping: Supports protocol types 6 (TCP), 17 (UDP), and 1 (ICMP).
    Log Format: Destination port and protocol are in the 6th and 7th columns, respectively (counting the '2' as column 0).

Testing:
Sample flow logs and lookup tables have been tested to verify that the tagging and counting mechanism works correctly.
Untagged entries are properly counted when no tag matches are found in the lookup table.