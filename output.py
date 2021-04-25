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

    with open(f"results/all.md", "w") as outfile:
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
    result = f"Totals for All Years\n"

    result += f"Year | Vaccinations | Deaths | Symptoms\n"
    result += "--- | --- | --- | ---\n"
    for year, val in yearly_totals.items():
        result += f"{year} | {val} | {yearly_deaths[year]} | {yearly_symptoms[year]}\n"

    return result


def write_newline():
    return "---\n"
