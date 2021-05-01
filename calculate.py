import collections


def calculate_data(vaers_data_by_year):
    results = {}
    for year, vaers_data in vaers_data_by_year.items():
        results[year] = {
            "totals": calculate_totals(vaers_data),
            "deaths": calculate_deaths(vaers_data),
            "symptoms": calculate_symptom_totals(vaers_data),
            "symptoms_details": calculate_symptoms(vaers_data),
        }

    return results


def calculate_totals(vaers_data):
    print("Calculating totals")
    results = new_results()

    for d in vaers_data:
        results["total"] += 1
        results["vax_type"][d.vax_type] += 1
        results["vax_id"][d.vax_id] += 1

    return sort_results(results)


def calculate_deaths(vaers_data):
    print("Calculating deaths")
    results = new_results()
    already_seen = set()

    for d in vaers_data:
        if not d.died == "Y":
            continue

        # Ensure we do not count deaths twice
        # If someone got 2 different vaccines and died, count it as 1 death
        if d.vaers_id not in already_seen:
            results["total"] += 1
            already_seen.add(d.vaers_id)

        results["vax_type"][d.vax_type] += 1
        results["vax_id"][d.vax_id] += 1

    return sort_results(results)


def calculate_symptom_totals(vaers_data):
    print("Calculating symptom totals")
    results = new_results()
    already_seen = set()

    for d in vaers_data:
        for _ in d.symptoms:
            # Ensure we do not count symptoms twice
            if d.vaers_id not in already_seen:
                results["total"] += 1
                already_seen.add(d.vaers_id)

            results["vax_type"][d.vax_type] += 1
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
            results["vax_id"][d.vax_id][s] += 1

    return sort_results_symptoms(results)


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
