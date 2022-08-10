from csv import DictReader, DictWriter
from repeater_management import convertList
import yaml

# Open a test file:
fields = [
    "No.",
    "Channel Name",
    "Receive Frequency",
    "Transmit Frequency",
    "Channel Type",
    "Transmit Power",
    "Band Width",
    "CTCSS/DCS Decode",
    "CTCSS/DCS Encode",
    "Contact",
    "Contact Call Type",
    "Radio ID",
    "Busy Lock/TX Permit",
    "Squelch Mode",
    "Optional Signal",
    "DTMF ID",
    "2Tone ID",
    "5Tone ID",
    "PTT ID",
    "Color Code",
    "Slot",
    "Scan List",
    "Receive Group List",
    "TX Prohibit",
    "Reverse",
    "Simplex TDMA",
    "TDMA Adaptive",
    "AES Encryption",
    "Digital Encryption",
    "Call Confirmation",
    "Talk Around",
    "Work Alone",
    "Custom CTCSS",
    "2TONE Decode",
    "Ranging",
    "Through Mode",
    "Digi APRS RX",
    "Analog APRS PTT Mode",
    "Digital APRS PTT Mode",
    "APRS Report Type",
    "Digital APRS Report Channel",
    "Correct Frequency[Hz]",
    "SMS Confirmation",
    "DMR MODE",
    "Exclude channel from roaming",
]

configFile = open("config.yml")
config = yaml.load(configFile, Loader=yaml.SafeLoader)

channels_writer = DictWriter(open("o_channels.csv", "w"), fieldnames=fields)
zones_writer = DictWriter(
    open("o_zones.csv", "w"),
    fieldnames=["No.", "Zone Name", "Zone Channel Member", "A Channel", "B Channel"],
)

channels_writer.writeheader()
zones_writer.writeheader()
# Grab the commmon stuff first
common_names = []
if "common" in config:
    reader = DictReader(open(config["common"]["file"]))
    common_names = convertList(reader, channels_writer)

for zone in config["zones"]:
    namelist = common_names.copy()
    reader = DictReader(open(config["zones"][zone]["file"]))
    rv = convertList(reader, channels_writer)
    namelist.extend(rv)

    zones_writer.writerow(
        {"Zone Name": zone, "Zone Channel Member": "|".join(namelist)}
    )
