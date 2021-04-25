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


def load():
    vaers_data_by_year = parse_data_files()
    results = {}

    for year, vaers_data in vaers_data_by_year.items():
        totals = calculate_totals(vaers_data)
        deaths = calculate_deaths(vaers_data)
        # symptoms = calculate_symptoms(vaers_data)
        # symptoms_lived = calculate_symptoms_lived(vaers_data)
        # symptoms_died = calculate_symptoms_died(vaers_data)
        symptom_totals = calculate_symptom_totals(vaers_data)
        results[year] = {
            "totals": totals,
            "deaths": deaths,
            # "symptoms": symptoms,
            # "symptoms_lived": symptoms_lived,
            # "symptoms_died": symptoms_died,
            "symptom_totals": symptom_totals,
        }

    return results


def calculate_totals(vaers_data):
    print("Calculating totals")
    results = new_results()

    for d in vaers_data:
        results["total"] += 1
        results["vax_type"][d.vax_type] += 1

        if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
            results["vax_id"][d.vax_id] += 1

    return sort_results(results)


def calculate_deaths(vaers_data):
    print("Calculating deaths")
    results = new_results()

    for d in vaers_data:
        if not d.died == "Y":
            continue

        results["total"] += 1
        results["vax_type"][d.vax_type] += 1

        if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
            results["vax_id"][d.vax_id] += 1

    return sort_results(results)


def calculate_symptoms(vaers_data):
    print("Calculating symptoms")
    results = new_results()

    for d in vaers_data:
        if d.vax_type not in results["vax_type"]:
            results["vax_type"][d.vax_type] = collections.defaultdict(int)

        if d.vax_id not in results["vax_id"]:
            results["vax_id"][d.vax_id] = collections.defaultdict(int)

        for s in d.symptoms:
            results["vax_type"][d.vax_type][s] += 1

            if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
                results["vax_id"][d.vax_id][s] += 1

    return sort_results_symptoms(results)


def calculate_symptoms_lived(vaers_data):
    print("Calculating symptoms lived")
    results = new_results()

    for d in vaers_data:
        if d.died == "Y":
            continue

        if d.vax_type not in results["vax_type"]:
            results["vax_type"][d.vax_type] = collections.defaultdict(int)

        if d.vax_id not in results["vax_id"]:
            results["vax_id"][d.vax_id] = collections.defaultdict(int)

        for s in d.symptoms:
            results["vax_type"][d.vax_type][s] += 1

            if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
                results["vax_id"][d.vax_id][s] += 1

    return sort_results_symptoms(results)


def calculate_symptoms_died(vaers_data):
    print("Calculating symptoms died")
    results = new_results()

    for d in vaers_data:
        if not d.died == "Y":
            continue

        if d.vax_type not in results["vax_type"]:
            results["vax_type"][d.vax_type] = collections.defaultdict(int)

        if d.vax_id not in results["vax_id"]:
            results["vax_id"][d.vax_id] = collections.defaultdict(int)

        for s in d.symptoms:
            results["vax_type"][d.vax_type][s] += 1

            if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
                results["vax_id"][d.vax_id][s] += 1

    return sort_results_symptoms(results)


def calculate_symptom_totals(vaers_data):
    print("Calculating symptom totals")
    results = new_results()

    for d in vaers_data:
        for _ in d.symptoms:
            results["vax_type"][d.vax_type] += 1

            if d.vax_manufacturer != "UNKNOWN MANUFACTURER":
                results["vax_id"][d.vax_id] += 1

    return sort_results(results)


def new_results():
    results = collections.defaultdict(int)
    results["vax_type"] = collections.defaultdict(int)
    results["vax_id"] = collections.defaultdict(int)
    return results


def sort_results(results):
    results["vax_type"] = sort_by_val(results["vax_type"])
    results["vax_id"] = sort_by_val(results["vax_id"])
    return results


def sort_results_symptoms(results):
    for key, val in results["vax_type"].items():
        results["vax_type"][key] = sort_by_val(val)

    for key, val in results["vax_id"].items():
        results["vax_id"][key] = sort_by_val(val)

    return results


def sort_by_val(x):
    return dict(sorted(x.items(), key=lambda item: item[1], reverse=True))


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
        results[year] = combine_vax(vaers_map, val["vax_data"])

    return results


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
        result.vax_id = f"{d.vax_type}-{d.vax_manufacturer}"
        results.append(result)

    return results


def combine_symptom(vaers_map, data):
    print("Combining symptom data")
    for d in data:
        result = vaers_map[d.vaers_id]
        result.append_symptom_data(d)
        vaers_map[result.vaers_id] = result
