import sys
from os import path
import ntpath
from lxml import etree as xml

# Get kml file from drag and drop
# kmlFile = sys.argv[1:]
# kmlFileName = ntpath.basename(kmlFile[0])
# kmlFileName = kmlFileName[:-4]

kmlFile = "Best Tugs 'B' Logo.kml"
kmlFileName = kmlFile[:-4]

# Parse kml file, setting 'document' as the root
with open(kmlFile) as f:
    document = xml.parse(f).getroot()

# Store coordinates into xml element then split up coordinates into a list
coordinatesXML = document[0][4][2][1]
coordinates = coordinatesXML.text.split(' ')

# Remove the last item in the list: '\n\t\t\t'
coordinates.pop()
coordinates[0] = coordinates[0][5:]


# coordinates = ['40.13,-111.99', '40.19088983459753,-111.9515247678293', '40.18340764483468,-111.8490774705657', '40.14,-111.8']

# Create 'flight-plan' element
flight_plan = xml.Element('flight-plan')
flight_plan.set('xmlns', 'http://www8.garmin.com/xmlschemas/FlightPlan/v1')
# Create 'created' element
created = xml.SubElement(flight_plan, 'created')
created.text = '20190503T16:39:24Z'
# Create 'aircraft' element and subelements
aircraft = xml.SubElement(flight_plan, 'aircraft')
aircraft_tailnumber = xml.SubElement(aircraft, 'aircraft-tailnumber')
aircraft_tailnumber.text = 'N23508'
# Create 'flight-data' element and subelements
flight_data = xml.SubElement(flight_plan, 'flight-data')
etd_zulu = xml.SubElement(flight_data, 'etd-zulu')
etd_zulu.text = '20190503T16:45:00Z'
# Create 'waypoint-table' element
waypoint_table = xml.SubElement(flight_plan, 'waypoint-table')
# Create 'route' element and subelements
route = xml.SubElement(flight_plan, 'route')
route_name = xml.SubElement(route, 'route-name')
route_name.text = kmlFileName
flight_plan_index = xml.SubElement(route, 'flight-plan-index')
flight_plan_index.text = '1'

# Initialize identifier number
i = 1

# Loop through all of the coordinates
# 293 waypoints is the limit in foreflight
# for x in range(len(coordinates)):
for x in range(300):
    # strip the coordinates by comma
    latlon = coordinates[x].split(',')
    print(latlon[1])
    # Create waypoint element and subelements
    waypoint = xml.SubElement(waypoint_table, 'waypoint')
    identifier = xml.SubElement(waypoint, 'identifier')
    identifier.text = str(i)
    _type = xml.SubElement(waypoint, 'type')
    _type.text = ''
    # latitude = latlon[1]
    lat = xml.SubElement(waypoint, 'lat')
    lat.text = str(latlon[1])
    # longitude = latlon[0]
    lon = xml.SubElement(waypoint, 'lon')
    lon.text = str(latlon[0])
    # Create route-point element and subelements
    route_point = xml.SubElement(route, 'route-point')
    waypoint_identifier = xml.SubElement(route_point, 'waypoint-identifier')
    waypoint_identifier.text = str(i)
    waypoint_type = xml.SubElement(route_point, 'waypoint-type')
    waypoint_type.text = ''

    # Increment indentifier number
    i += 1

# Create fpl file
fplFileName = kmlFileName + '.fpl'
tree = xml.ElementTree(flight_plan)
tree.write(fplFileName, encoding='utf-16', xml_declaration=True, pretty_print=True)