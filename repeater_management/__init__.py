from csv import DictReader, DictWriter


def convertList(
    list: DictReader,
    writer: DictWriter,
):
    """
    This will take in the generic form of the csv from RepeaterBook, and add
    them to the CSV writer, using the default field_defaults
    """
    default_data = {
        "2TONE Decode": "1",
        "2Tone ID": "1",
        "5Tone ID": "1",
        "AES Encryption": "Normal Encryption",
        "APRS Report Type": "Off",
        "Analog APRS PTT Mode": "Off",
        "Band Width": "12.5K",
        "Busy Lock/TX Permit": "Off",
        "CTCSS/DCS Decode": "Off",
        "CTCSS/DCS Encode": "Off",
        "Call Confirmation": "Off",
        "Channel Name": "Channel VFO B",
        "Channel Type": "A-Analog",
        "Color Code": "1",
        "Contact": "Contact1",
        "Contact Call Type": "Group Call",
        "Correct Frequency[Hz]": "0",
        "Custom CTCSS": "131.8",
        "DMR MODE": "0",
        "DTMF ID": "1",
        "Digi APRS RX": "Off",
        "Digital APRS PTT Mode": "Off",
        "Digital APRS Report Channel": "1",
        "Digital Encryption": "Off",
        "Exclude channel from roaming": "0",
        "Optional Signal": "Off",
        "PTT ID": "Off",
        "Radio ID": "My Radio",
        "Ranging": "Off",
        "Receive Frequency": "145.12500",
        "Receive Group List": "None",
        "Reverse": "Off",
        "SMS Confirmation": "Off",
        "Scan List": "None",
        "Simplex TDMA": "Off",
        "Slot": "1",
        "Squelch Mode": "Carrier",
        "TDMA Adaptive": "Off",
        "TX Prohibit": "Off",
        "Talk Around": "Off",
        "Through Mode": "Off",
        "Transmit Frequency": "145.12500",
        "Transmit Power": "High",
        "Work Alone": "Off",
    }
    name_list = []
    for row in list:
        # We going to go through each row, make some changes and then add it to
        # the master list
        new_data = default_data.copy()

        new_data["Receive Frequency"] = f"{float(row['Frequency']):.3f}"
        suffix = ""
        if float(new_data["Receive Frequency"]) < 400:
            suffix = "2m"
        else:
            suffix = "70cm"
        new_data["Channel Name"] = f"{row['Name']} ({suffix})"
        name_list.append(new_data["Channel Name"])
        tx = float(row["Frequency"]) + (
            float(f"{row['Duplex']}1") * float(row["Offset"])
        )
        new_data["Transmit Frequency"] = f"{tx:.3f}"
        new_data["Channel Type"] = "D-Digital" if "DIG" in row["Mode"] else "A-Analog"
        if len(row["Tone"]) > 0:
            # We have some tone settings to move over
            # cToneFreq -> Transmit CTCSS Freq
            # rToneFreq -> Receive CTCSS Freq
            new_data["CTCSS/DCS Decode"] = row["rToneFreq"]
            new_data["CTCSS/DCS Encode"] = row["cToneFreq"]
            new_data["Custom CTCSS"] = row["cToneFreq"]
        writer.writerow(new_data)

    return name_list
