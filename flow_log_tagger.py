import csv
from collections import defaultdict

# apologies for all the debug print comments

# creates an array for the lookup table where dstport and protocol is the address location, and the tag is the value stored there
# lookup_dict = {('25', 'tcp'): 'sv_P1', ('68', 'udp'): 'sv_P2', ('23', 'tcp'): 'sv_P1'}
def load_lookup_table(lookup_file):
    lookup_dict = {}
    with open(lookup_file, mode='r') as csvfile:
        # delimiter to prevent issues with the formatting of excel file
        reader = csv.DictReader(csvfile, delimiter='\t')

        # print("CSV Headers:", reader.fieldnames)
        for row in reader:
            dstport = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()  # Case-insensitive protocol
            tag = row['tag'].strip()
            lookup_dict[(dstport, protocol)] = tag
        # print(lookup_dict)
    return lookup_dict

# bulk of program, determines tag counts and port/protocol counts
def parse_flow_logs(log_file, lookup_dict):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    
    with open(log_file, mode='r') as logfile:
        for line in logfile:
            fields = line.strip().split()
            # print(fields)

            # skip incorrectly formatted lines
            if len(fields) < 10:
                continue
            
            # destination port is field 6, protocol number is field 7 (according to AWS)
            dstport = fields[6].strip()
            protocol_num = fields[7].strip()
            # print(dstport)
            # print(protocol_num)
            
            # mapping protocol numbers to protocol names (TCP=6, UDP=17, ICMP=1)
            protocol = map_protocol(protocol_num)
            
            if protocol:
                tag = lookup_dict.get((dstport, protocol), 'Untagged')
                if tag == 'Untagged':
                    untagged_count += 1
                else:
                    tag_counts[tag] += 1
                
                port_protocol_counts[(dstport, protocol)] += 1
    
    # add untagged count at the end
    tag_counts['Untagged'] = untagged_count
    # print(tag_counts)
    
    return tag_counts, port_protocol_counts

# helper func
def map_protocol(protocol_num):
    # assuming the flow logs only use these 3 protocols
    protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}
    return protocol_map.get(protocol_num)

# print data in output.txt
def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, mode='w') as outfile:
        outfile.write("Tag Counts:\nTag,Count\n")
        for tag, count in tag_counts.items():
            outfile.write(f"{tag},{count}\n")
        
        outfile.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            outfile.write(f"{port},{protocol},{count}\n")

# runs this code if you enter "python flow_log_tagger.py" into console
if __name__ == '__main__':
    lookup_file = 'lookup_table.csv'
    log_file = 'flow_logs.txt'
    output_file = 'output.txt'
    
    # Load the lookup table
    lookup_dict = load_lookup_table(lookup_file)
    
    # Parse the flow logs and compute counts
    tag_counts, port_protocol_counts = parse_flow_logs(log_file, lookup_dict)
    
    # Write the results to the output file
    write_output(tag_counts, port_protocol_counts, output_file)