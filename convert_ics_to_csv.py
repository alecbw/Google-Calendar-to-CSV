import os
import csv
import sys
from datetime import datetime

try:
    from icalendar import Calendar, Event
except ImportError:
    sys.exit("~ Make sure you install icalendar. Run `pip install icalendar` and try this again ~")


def convert_timestamps(component, selector):
    data = component.get(selector)
    if not data:
        return None
    return data.dt.strftime("%m/%d/%Y %H:%M:%S")

if __name__ == "__main__":
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
                "Type": "", # Makes the columns in the right order later
                "With": "",
                "Location": component.get('location'),
                "Duration": "",
                "Raw Start": convert_timestamps(component, 'dtstart'),
                "Raw End": convert_timestamps(component, 'dtend'),
            }
            if output_dict["Raw Start"] and output_dict["Raw End"]:
                output_dict["Duration"] = (datetime.strptime(output_dict["Raw End"], "%m/%d/%Y %H:%M:%S") - datetime.strptime(output_dict["Raw Start"], "%m/%d/%Y %H:%M:%S")).total_seconds() / 60


            output_lod.append(output_dict)
    f.close()

    with open("Processed Calendar Events.csv", "w") as output_file:
        dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(output_lod)

    print("Data successfully processed. Output file is called: Processed Birthdays.csv")
