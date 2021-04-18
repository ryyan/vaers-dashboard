import csv
import os
import json


class VaersData:
    def __init__(self, row):
        self.vaers_id = row["VAERS_ID"]
        self.recv_date = row["RECVDATE"]
        self.state = row["STATE"]
        self.age_years = row["AGE_YRS"]
        # self.cage_year = row["CAGE_YR"]
        # self.cage_month = row["CAGE_MO"]
        self.sex = row["SEX"]
        # self.report_date = row["RPT_DATE"]
        self.died = row["DIED"]
        self.date_died = row["DATEDIED"]
        # self.l_threat = row["L_THREAT"]
        # self.er_visit = row["ER_VISIT"]
        # self.hospital = row["HOSPITAL"]
        # self.hospital_days = row["HOSPDAYS"]
        # self.x_stay = row["X_STAY"]
        # self.disable = row["DISABLE"]
        self.recovered = row["RECOVD"]
        self.vax_date = row["VAX_DATE"]
        self.onset_date = row["ONSET_DATE"]
        # self.num_days = row["NUMDAYS"]
        self.symptom_text = row["SYMPTOM_TEXT"]
        self.lab_data = row["LAB_DATA"]
        # self.v_admin_by = row["V_ADMINBY"]
        # self.v_fund_by = row["V_FUNDBY"]
        self.other_meds = row["OTHER_MEDS"]
        self.current_ill = row["CUR_ILL"]
        self.history = row["HISTORY"]
        self.prior_vax = row["PRIOR_VAX"]
        # self.splt_type = row["SPLTTYPE"]
        # self.form_version = row["FORM_VERS"]
        # self.todays_date = row["TODAYS_DATE"]
        self.birth_defect = row["BIRTH_DEFECT"]
        # self.office_visit = row["OFC_VISIT"]
        # self.er_ed_visit = row["ER_ED_VISIT"]
        self.allergies = row["ALLERGIES"]
        self.vaxes = []
        self.symptoms = []

    def append_vax_data(self, vax_data):
        result = vax_data.__dict__
        del result["vaers_id"]
        self.vaxes.append(result)

    def append_symptom_data(self, symptom_data):
        for s in symptom_data.symptoms:
            self.symptoms.append(s)


class VaxData:
    def __init__(self, row):
        self.vaers_id = row["VAERS_ID"]
        self.vax_type = row["VAX_TYPE"]
        self.vax_manufacturer = row["VAX_MANU"]
        self.vax_dose_series = row["VAX_DOSE_SERIES"]
        # self.vax_lot = row["VAX_LOT"]
        # self.vax_route = row["VAX_ROUTE"]
        # self.vax_site = row["VAX_SITE"]
        # self.vax_name = row["VAX_NAME"]


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


class CombinedData:
    def __init__(self, vaers_id, vax_data, vaers_data, symptom_data):
        self.vaers_id = vaers_id
        self.vaers_data = vaers_data
        self.vax_data = vax_data
        self.symptom_data = symptom_data


def parseAll():
    print("Parsing data files")

    data_folder = "data"

    for entry in os.scandir(data_folder):
        if not entry.is_file() or not entry.name.endswith(".csv"):
            continue

        if entry.name.endswith("DATA.csv"):
            vaers_data = parse(entry.path, VaersData)
            vaers_map = to_map(vaers_data)

        if entry.name.endswith("VAX.csv"):
            vax_data = parse(entry.path, VaxData)

        if entry.name.endswith("SYMPTOMS.csv"):
            symptom_data = parse(entry.path, SymptomData)

    combine_vax(vaers_map, vax_data)
    combine_symptom(vaers_map, symptom_data)

    print("Converting results to json")
    results = []
    for val in vaers_map.values():
        results.append(val.__dict__)

    return json.dumps(results)


def parse(file_path, data_class):
    print(f"Parsing {file_path}")
    results = []

    with open(file_path, encoding="raw_unicode_escape") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            results.append(data_class(row))

    print(f"Parsed {len(results)}")
    return results


def to_map(data):
    results = {}
    for d in data:
        results[d.vaers_id] = d

    return results


def combine_vax(vaers_map, data):
    print("Combining vax data")
    for d in data:
        result = vaers_map[d.vaers_id]
        result.append_vax_data(d)
        vaers_map[result.vaers_id] = result


def combine_symptom(vaers_map, data):
    print("Combining symptom data")
    for d in data:
        result = vaers_map[d.vaers_id]
        result.append_symptom_data(d)
        vaers_map[result.vaers_id] = result
