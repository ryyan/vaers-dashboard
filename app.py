import json

import data


def main():
    vaers_data_by_year, vaers_data_json = data.parse_data_files()
    with open("results/vaers_data.json", "w") as outfile:
        outfile.write(vaers_data_json)

    results = data.calculate_data(vaers_data_by_year)
    with open("results/results.json", "w") as outfile:
        outfile.write(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
