import csv
import os
from copy import copy


class VaersData:
    def __init__(self, row):
        self.vaers_id = row["VAERS_ID"]
        self.recv_date = row["RECVDATE"]
        self.state = row["STATE"]
        self.age_years = row["AGE_YRS"]
        self.sex = row["SEX"]
        self.died = row["DIED"]
        self.date_died = row["DATEDIED"]
        self.vax_date = row["VAX_DATE"]
        self.onset_date = row["ONSET_DATE"]
        self.other_meds = row["OTHER_MEDS"]

        # These fields will be populated after object creation
        self.vax_type = None
        self.vax_manufacturer = None
        self.vax_dose_series = None
        self.vax_id = None
        self.symptoms = []

    def append_symptom_data(self, symptom_data):
        for s in symptom_data.symptoms:
            self.symptoms.append(s)


class VaxData:
    def __init__(self, row):
        self.vaers_id = row["VAERS_ID"]
        self.vax_type = row["VAX_TYPE"]
        self.vax_manufacturer = row["VAX_MANU"]
        self.vax_dose_series = row["VAX_DOSE_SERIES"]


class SymptomData:
    def __init__(self, row):
        self.vaers_id = row["VAERS_ID"]
        self.symptoms = []

        if row["SYMPTOM1"]:
            self.symptoms.append(row["SYMPTOM1"])
        if row["SYMPTOM2"]:
            self.symptoms.append(row["SYMPTOM2"])
        if row["SYMPTOM3"]:
            self.symptoms.append(row["SYMPTOM3"])
        if row["SYMPTOM4"]:
            self.symptoms.append(row["SYMPTOM4"])
        if row["SYMPTOM5"]:
            self.symptoms.append(row["SYMPTOM5"])


def parse_data_files():
    print("Parsing data files")
    data_folder = "data"
    parsed_data = {}

    for entry in os.scandir(data_folder):
        if not entry.is_file() or not entry.name.endswith(".csv"):
            continue

        # Ex: 2020VAERSDATA.csv
        year = int(entry.name[:4])

        if year not in parsed_data:
            parsed_data[year] = {}

        if entry.name.endswith("DATA.csv"):
            parsed_data[year]["vaers_data"] = parse_data_file(entry.path, VaersData)

        if entry.name.endswith("VAX.csv"):
            parsed_data[year]["vax_data"] = parse_data_file(entry.path, VaxData)

        if entry.name.endswith("SYMPTOMS.csv"):
            parsed_data[year]["symptom_data"] = parse_data_file(entry.path, SymptomData)

    print("Combining data")
    results = {}
    for year, val in parsed_data.items():
        # Convert vaers data to map to make it easier to combine all data models
        vaers_map = map_vaers_data(val["vaers_data"])
        combine_symptom(vaers_map, val["symptom_data"])
        # Flatten data when combining with vax data (so now there will be repeating vaers IDs)
        # Multiple VAERS data objects can have the same VAERS ID but will have different vax data
        results[year] = combine_vax(vaers_map, val["vax_data"])

    return results


def parse_data_file(file_path, data_class):
    print(f"Parsing {file_path}")
    results = []

    with open(file_path, encoding="windows-1252") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            results.append(data_class(row))

    print(f"Parsed {len(results)}")
    return results


def map_vaers_data(data):
    results = {}
    for d in data:
        results[d.vaers_id] = d

    return results


def combine_vax(vaers_map, data):
    print("Combining vax data")
    results = []

    for d in data:
        result = copy(vaers_map[d.vaers_id])
        result.vax_type = d.vax_type
        result.vax_manufacturer = d.vax_manufacturer
        result.vax_dose_series = d.vax_dose_series
        result.vax_id = f"{d.vax_type}-{d.vax_manufacturer}"
        results.append(result)

    return results


def combine_symptom(vaers_map, data):
    print("Combining symptom data")
    for d in data:
        result = vaers_map[d.vaers_id]
        result.append_symptom_data(d)
        vaers_map[result.vaers_id] = result
