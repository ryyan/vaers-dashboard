def output_results(results_by_year):
    yearly_totals = {}
    yearly_deaths = {}
    yearly_symptoms = {}

    for year, results in results_by_year.items():
        print(f"Writing results for year {year}")
        output = ""
        output += write_table(results["totals"], "Total Vaccinations", "Total")
        output += write_table(results["deaths"], "Total Deaths", "Deaths")
        output += write_table(results["symptoms"], "Total Symptoms", "Symptoms")

        with open(f"results/{year}.md", "w") as outfile:
            outfile.write(output)

        yearly_totals[year] = results["totals"]["total"]
        yearly_deaths[year] = results["deaths"]["total"]
        yearly_symptoms[year] = results["symptoms"]["total"]

    with open(f"results/ALL.md", "w") as outfile:
        outfile.write(write_all(yearly_totals, yearly_deaths, yearly_symptoms))


def write_table(data, header, value_column):
    result = f"# {header}\n"

    result += f"Vax Type | {value_column}\n"
    result += "--- | ---\n"
    for key, val in data["vax_type"].items():
        result += f"{key} | {val}\n"

    result += write_newline()

    result += f"Vax ID | {value_column}\n"
    result += "--- | ---\n"
    for key, val in data["vax_id"].items():
        result += f"{key} | {val}\n"

    result += write_newline()
    return result


def write_all(yearly_totals, yearly_deaths, yearly_symptoms):
    result = f"Totals By Year\n"

    result += f"Year | Total | Deaths | Deaths % | Symptoms | Symptoms %\n"
    result += "--- | --- | --- | --- | --- | ---\n"
    for year, total in yearly_totals.items():
        deaths = yearly_deaths[year]
        symptoms = yearly_symptoms[year]
        deaths_ratio = "{:.2%}".format(deaths / total)
        symptoms_ratio = "{:.0%}".format(symptoms / total)
        result += f"{year} | {total} | {deaths} | {deaths_ratio} | {symptoms} | {symptoms_ratio}\n"

    return result


def write_newline():
    return "---\n"
