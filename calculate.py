import collections


def calculate_data(vaers_data_by_year):
    results = {}
    for year, vaers_data in vaers_data_by_year.items():
        results[year] = {
            "totals": calculate_totals(vaers_data),
            "deaths": calculate_deaths(vaers_data),
            # "symptoms": calculate_symptoms(vaers_data),
            # "symptoms_lived": calculate_symptoms_lived(vaers_data),
            # "symptoms_died": calculate_symptoms_died(vaers_data),
            "symptom_totals": calculate_symptom_totals(vaers_data),
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
