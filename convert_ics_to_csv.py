import os
import csv
import sys
from datetime import datetime

# from bs4 import BeautifulSoup
from icalendar import Calendar, Event

def convert_timestamps(component, selector):
    data = component.get(selector)
    if not data:
        return None
    return data.dt.strftime("%m/%d/%Y %H:%M:%S")

files = [f for f in os.listdir('.') if os.path.isfile(f) and ".ics" in f and "contacts" not in f]
if not files or not os.path.isfile(files[0]):
    sys.exit("\nPlease ensure your exported calendar (unzipped to `.ics`) is in the folder your Terminal session is in\n")

filepath = (os.getcwd() + "/" + files[0])

f = open(filepath, 'rb')
gcal = Calendar.from_ical(f.read())

output_lod = []
for n, component in enumerate(gcal.walk()):
    if component.name == "VEVENT":
        output_dict = {
            "#": n,
            "Event Name": component.get('summary'),
            "Description": component.get('description'),
            "Type": "",
            "With": "",
            "Location": component.get('location'),
            "Duration": "",# component.get('duration').dt, #Y3/29/2014 16:00:00
            "Raw Start": convert_timestamps(component, 'dtstart'),# component.get('dtstart').dt.strftime("%m/%d/%Y %H:%M:%S"),
            "Raw End": convert_timestamps(component, 'dtend'),# component.get('dtend').dt.strftime("%m/%d/%Y %H:%M:%S"),
        }
        if output_dict["Raw Start"] and output_dict["Raw End"]:
            output_dict["Duration"] = (datetime.strptime(output_dict["Raw End"], "%m/%d/%Y %H:%M:%S") - datetime.strptime(output_dict["Raw Start"], "%m/%d/%Y %H:%M:%S")).total_seconds() / 60


        output_lod.append(output_dict)
f.close()


# Event Name  Description Type    With    Location    Duration (min)  Start Time  Finish Time Raw Start   Raw Finish  Days Total
# description
# location
# duration


# parsed = BeautifulSoup(open(filepath), "html.parser")

# output_lod = []
# for birthday_row in parsed.find_all("li", {"class": "_43q7"}):   # Querying into li for each individual

#     birthday_data = birthday_row.find("a", {"class": "link"})
#     birthday_info = birthday_data.get("data-tooltip-content")    # Get string with our wanted substrings in it

#     output_dict = {
#         "Name": birthday_info.split(" (",1)[0],                   # Get Name substring from Info string
#         "Date": birthday_info.split(" (",1)[1].replace(")", ""),  # Get Date substring from Info string
#         "Link": birthday_data.get("href")                         # Get FB Profile Link
#     }

#     output_lod.append(output_dict)

with open("Processed Calendar Events.csv", "w") as output_file:
    dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(output_lod)

print("Data successfully processed. Output file is called: Processed Birthdays.csv")
