import csv
import collections
import os
import json
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
        # self.recovered = row["RECOVD"]
        self.vax_date = row["VAX_DATE"]
        self.onset_date = row["ONSET_DATE"]
        # self.symptom_text = row["SYMPTOM_TEXT"]
        # self.lab_data = row["LAB_DATA"]
        self.other_meds = row["OTHER_MEDS"]
        # self.current_ill = row["CUR_ILL"]
        # self.history = row["HISTORY"]
        # self.prior_vax = row["PRIOR_VAX"]
        # self.birth_defect = row["BIRTH_DEFECT"]
        # self.allergies = row["ALLERGIES"]

        self.vax_type = None
        self.vax_manufacturer = None
        self.vax_dose_series = None
        self.vax_string = None

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


class DataLoader:

    @staticmethod
    def load():
        vaers_data = parse_data_files()
        totals = calculate_totals(vaers_data)
        deaths = calculate_deaths(vaers_data)
        return {
            "totals": totals,
            "deaths": deaths,
        }


def calculate_totals(vaers_data):
    print("Calculating totals")
    results = collections.defaultdict(int)
    results["vax_type"] = collections.defaultdict(int)
    results["vax_string"] = collections.defaultdict(int)

    for d in vaers_data:
        results["total"] += 1
        results["vax_type"][d.vax_type] += 1
        results["vax_string"][d.vax_string] += 1

    return results


def calculate_deaths(vaers_data):
    print("Calculating deaths")
    results = collections.defaultdict(int)
    results["vax_type"] = collections.defaultdict(int)
    results["vax_string"] = collections.defaultdict(int)

    for d in vaers_data:
        if d.died == "Y":
            results["total"] += 1
            results["vax_type"][d.vax_type] += 1
            results["vax_string"][d.vax_string] += 1

    return results


def parse_data_files():
    print("Parsing data files")
    data_folder = "data"

    for entry in os.scandir(data_folder):
        if not entry.is_file() or not entry.name.endswith(".csv"):
            continue

        if entry.name.endswith("DATA.csv"):
            vaers_data = parse_data_file(entry.path, VaersData)

        if entry.name.endswith("VAX.csv"):
            vax_data = parse_data_file(entry.path, VaxData)

        if entry.name.endswith("SYMPTOMS.csv"):
            symptom_data = parse_data_file(entry.path, SymptomData)

    print("Combining data")
    # Convert vaers data to map to make it easier to combine all data models
    vaers_map = map_vaers_data(vaers_data)
    combine_symptom(vaers_map, symptom_data)
    # Flatten data when combining with vax data (so now there will be repeating vaers IDs)
    return combine_vax(vaers_map, vax_data)


def parse_data_file(file_path, data_class):
    print(f"Parsing {file_path}")
    results = []

    with open(file_path, encoding="raw_unicode_escape") as csv_file:
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
        result.vax_string = f"{d.vax_type};{d.vax_manufacturer}"
        results.append(result)

    return results


def combine_symptom(vaers_map, data):
    print("Combining symptom data")
    for d in data:
        result = vaers_map[d.vaers_id]
        result.append_symptom_data(d)
        vaers_map[result.vaers_id] = result
