from pathlib import Path
import argparse
import sys

from src.load_file import load_file
from src.analyze import analyze_data
from src.present_data import present_analysis_tables
from src.export_tables import export_latex_tables

def main():

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Process an Excel file.")
    
    parser.add_argument(
        "-f", "--file", dest="file_path", type=Path, required=True,
        help="Path to the Excel file (.xls or .xlsx)"
    )
    parser.add_argument(
        "-o", "--output_dir", type=Path, default=Path("out"),
        help="Directory to store output files (default: out)"
    )
    parser.add_argument(
        "-d", "--db_file", type=Path, default=Path("data/completed.db"),
        help="Path to the SQLite database file (default: completed.db)"
    )
    
    args = parser.parse_args()

    file_path = args.file_path
    output_dir = args.output_dir
    db_file = args.db_file

    # Check if the file path is valid and if the file is an Excel file
    if not file_path.is_file():
        print("Error: Provided path is not a valid file.")
        sys.exit(1)

    if file_path.suffix.lower() not in ['.xls', '.xlsx']:
        print("Error: File is not an Excel (.xls or .xlsx) file.")
        sys.exit(1)

    # Check if the output directory exists, if not create it
    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Check if the database file exists, and if its a .db file
    if not db_file.is_file():
        print(f"Error: Database file {db_file} does not exist.")
        sys.exit(1)

    if db_file.suffix.lower() != '.db':
        print("Error: Database file is not a SQLite (.db) file.")
        sys.exit(1)

    # load the file and process it
    try:
        df = load_file(file_path)
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        sys.exit(1)

    # analyze the data
    analysis = analyze_data(df)

    presented_data = present_analysis_tables(analysis)

    export_latex_tables(presented_data, output_dir)






if __name__ == "__main__":
    main()
    sys.exit(0)
