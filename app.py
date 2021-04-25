from parse import parse_data_files
from calculate import calculate_data
from output import output_results


def main():
    vaers_data_by_year = parse_data_files()
    query_data_by_year = calculate_data(vaers_data_by_year)
    output_results(vaers_data_by_year, query_data_by_year)


if __name__ == "__main__":
    main()
