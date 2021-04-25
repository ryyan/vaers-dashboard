from parse import parse_data_files
from calculate import calculate_data
from output import output_results


def main():
    vaers_data_by_year, vaers_data_json = parse_data_files()
    with open("results/vaers_data.json", "w") as outfile:
        outfile.write(vaers_data_json)

    results, results_json = calculate_data(vaers_data_by_year)
    with open("results/results.json", "w") as outfile:
        outfile.write(results_json)

    output_results(results)


if __name__ == "__main__":
    main()
