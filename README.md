# Hotel Scraper - Booking.com

## Overview

This Python script automates the process of collecting hotel listings from Booking.com based on user-specified search criteria. It uses Playwright to navigate the website, extract relevant hotel details (such as name, price, taxes, total cost, and reviews), and saves the results in an Excel file.

## Features

- Searches for hotels on Booking.com based on user input.
- Extracts hotel details, including name, price, taxes, total cost, and review scores.
- Ensures all available listings are loaded for comprehensive scraping.
- Saves results in an Excel file at a specified location.
- Handles pop-ups and lazy-loaded elements automatically.

## Requirements

Make sure you have the following dependencies installed before running the script:

- Python 3.x
- Playwright
- Pandas

### Install dependencies:

```bash
pip install pandas playwright
playwright install
```

## Usage

Run the script with the following arguments:

```bash
python hotels_scraper.py --city "CityName" --country "CountryName" --indate "YYYY-MM-DD" --outdate "YYYY-MM-DD" --nadult N --nchild N --nroom N --path "output_directory" --sheetname "output_filename"
```

### Example:

```bash
python hotels_scraper.py --city "Alexandria" --country "Egypt" --indate "2025-02-24" --outdate "2025-02-27" --nadult 2 --nchild 2 --nroom 2 --path "D:\Projects\Scraping" --sheetname "hotels_list"
```

## Arguments

| Argument      | Description                                          |
| ------------- | ---------------------------------------------------- |
| `--city`      | The city to search for hotels in.                    |
| `--country`   | The country of the city.                             |
| `--indate`    | Check-in date (YYYY-MM-DD).                          |
| `--outdate`   | Check-out date (YYYY-MM-DD).                         |
| `--nadult`    | Number of adults.                                    |
| `--nchild`    | Number of children.                                  |
| `--nroom`     | Number of rooms required.                            |
| `--path`      | Directory where the output Excel file will be saved. |
| `--sheetname` | Name of the output Excel file.                       |

## Notes

- If an invalid file path is provided, the output file is created in the current working directory.
- The script uses the `End` key to trigger lazy loading and ensures all listings are retrieved.
- Ensure your internet connection is stable for uninterrupted scraping.

## License

This script is open-source and free to use. Modify and distribute it as needed.

## Author

Developed for web scraping hotel listings efficiently from Booking.com using Playwright and Python.

---

For any issues or improvements, feel free to contribute!

