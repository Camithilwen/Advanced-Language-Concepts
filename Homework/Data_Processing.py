import re
#
## Open input file and copy data to a list.
#
input_file = open("access.log", "rt")
input_data = input_file.readlines()
output_data = []

#
## Process data to filter for "BotPoke" and append to new, empty, list.
#
for x in input_data:
    if("BotPoke" not in x):
        output_data.append(x)

#
## Write data to a new output file.
#
output_file = open("filteredAccess.log", "wt")
output_file.writelines(output_data)
input_file.close()

#
## Count remaining lines of data
#
counter = 0
for x in output_data:
    counter += 1
print("BotPoke filer applied. Remaining log entries: ", counter)
 
#
## Use regular expression to list IP addresses present in the filtered data.
## Filter remaining addresses through set conversion and present unique entries.
#
filteredIPs = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(output_data))
uniqueIPs = list(set(filteredIPs))
print("Remaining unique IP addresses: ",uniqueIPs)