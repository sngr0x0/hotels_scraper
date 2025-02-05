from playwright.sync_api import sync_playwright
from time import sleep
import pandas as pd
import argparse
import sys
import os

# Argument parser setup for user-provided inputs
parser = argparse.ArgumentParser(
    description=(
        "This script scrapes hotels from Booking.com based on the provided parameters.\n"
        "After retrieving the search results, they are scraped and stored in an Excel sheet at the specified path."
    ),
    epilog=(
        "Usage Example:\n"
        "final_scraper.py --city Alexandria --country Egypt --indate 2025-2-24\n"
        "    --outdate 2025-2-27 --nadult 2 --nchild 2 --nroom 2 \n"
        "    --path D:\\Projects\\Scraping --sheetname final_list"
    )
)

# Adding arguments for city, country, dates, number of guests, and output file information
# Since default value for the "type" parameter is str by default, we don't pass an argument for it.
parser.add_argument("--city", required= True, help= "The city that you want to search in.", metavar= "Alexandria")
parser.add_argument("--country", required= True, help= "The country that you want to search in.", metavar= "Egypt")
parser.add_argument("--indate", required = True, help = "Checking in date.", metavar = "2025-2-24")
parser.add_argument("--outdate", required = True, help = "Checking out date.", metavar = "2025-2-25")
parser.add_argument("--nadult", required = True, help = "Number of adults who are checking in.", metavar = "2")
parser.add_argument("--nchild", required = True, help = "Number of children who are checking in.", metavar = "3")
parser.add_argument("--nroom", required = True, help = "Number of rooms needed.", metavar = "2")
parser.add_argument("--path", required = True, help = "Path of the directory where the excel sheet get stored.", metavar = "D:\\projects\\scraping")
parser.add_argument("--sheetname", required = True, help = "Name of the excel sheet file.", metavar = "hotels_list")
args = parser.parse_args()

def main():
    with sync_playwright() as p:
         # User-provided parameters
        checkin_date = args.indate
        checkout_date = args.outdate
        adults_no = args.nadult
        children_no = args.nchild
        rooms_no = args.nroom
        city = args.city
        country = args.country
        # Validate the provided file path
        if not os.path.isabs(args.path):
            print("Entered path is invalid, the file is created in the current working directory.")
            path = os.getcwd()
        else:
            path = args.path
        # Construct the full path for the output Excel file
        full_path = os.path.join(path, args.sheetname + '.xlsx')
        
        # Construct the booking.com URL with query parameters
        page_url = f'https://www.booking.com/searchresults.html?ss={city}%2C+{country}&checkin={checkin_date}&checkout={checkout_date}&group_adults={adults_no}&no_rooms={rooms_no}&group_children={children_no}'
        print(f"Navigating to: {page_url}")

        # Launch the browser and open a new page
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to the constructed URL
            page.goto(page_url, timeout = 5000)
        except Exception as e:
            print("Can't navigate to the page with these arguments.\nPlease double-check the arguments that you passed.\nExitting...")
            sleep(2)
            sys.exit()
        # Handle the initial pop-up (e.g., sign-in prompt)
        x_sign_in = page.get_by_role("button", name="Dismiss sign-in info.")
        x_sign_in.wait_for()
        x_sign_in.click()
        #I could've used assertions here too => expect(x_sign_in).to_be_visible()

        # Initialize the "Load more results" button
        next_button = page.get_by_text('Load more results') #For pagination
        

        # Scroll and load all hotel listings
        while True:
            page.keyboard.press("End") #The end key takes us to the end of the page; needed for "Lazy loading"
            print("Scrolling down...")
            page.wait_for_load_state("networkidle")
            #Wait until all elements are loaded
            try:
                next_button.wait_for()
                next_button.click()
            except Exception as e:
                hotels = page.get_by_test_id("property-card").all()
                break
        print(f"Number of hotels found: {len(hotels)}")
        #------------------------------------
        ## Extract hotel details and store it as a list of dictionaries where each dictionary represents a hotel
        print("Extracting the data from the search results...")
        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            # Extract hotel name
            try:
                hotel_dict['Hotel'] = hotel.get_by_test_id("title").inner_text()
            except Exception as e:
                hotel_dict['Hotel']= "N/A"
            
            # Extract price
            try:
                hotel_dict['Price'] = hotel.get_by_test_id("price-and-discounted-price").inner_text().replace('&nbsp;', ' ').strip()
            except Exception as e:
                hotel_dict['Price']= "N/A"
            
            # Extract taxes and charges
            try:
                hotel_dict['Taxes & Charges'] = hotel.get_by_test_id("taxes-and-charges").inner_text().replace('taxes and fees', '').replace('+', '').replace('&nbsp;', ' ').replace('Includes ', 'EGP 0').strip()
            except Exception as e:
                hotel_dict['Taxes & Charges']= "N/A"

            # Calculate total cost
            try:
                hotel_dict['Total Cost'] = f"EGP {int(hotel_dict['Price'].replace('EGP', '').replace(',','').strip()) + int(hotel_dict['Taxes & Charges'].replace('EGP', '').replace(',','').strip())}"
            except ValueError:
                hotel_dict['Total Cost'] = "N/A"

            # Extract reviews count
            review_count = hotel.get_by_test_id("review-score").locator('//div[2]/div[2]')
            if review_count.is_visible():
                try:
                    hotel_dict['Reviews Count'] = review_count.inner_text()
                except Exception as e:
                    hotel_dict['Reviews Count'] = "N/A"
            else:
                hotel_dict['Reviews Count'] = "N/A"
            
            # Extract overall rating
            overall_rate = hotel.get_by_test_id("review-score").locator('//div[1]/div[1]')
            gpa = hotel.get_by_test_id("review-score").locator('//div[2]/div[1]')

            if overall_rate.is_visible() and gpa.is_visible():
                hotel_dict['Overall Rate'] = overall_rate.inner_text().replace('Scored ', '') + " - " + gpa.inner_text()
            else:
                hotel_dict['Overall Rate'] = "N/A"

            hotels_list.append(hotel_dict)
        #------------------------------------
        print("Creating the excel sheet...")
        if hotels_list:
            df = pd.DataFrame(hotels_list)

            try:
                #Turn the data frame into an excel sheet.
                df.to_excel(full_path, index=False)
            except Exception as e:
                print("Can't create the excel sheet...")

            print(f"Excel file created: {full_path}")
        else:
            print("No hotels found!")
 
        browser.close()

if __name__ == "__main__":
    main()

#NOTE:
#references:
#https://stackoverflow.com/questions/7132861/how-can-i-create-a-full-path-to-a-file-from-parts-e-g-path-to-the-folder-name
#os.path.join() which exists because different operating systems use different separators
#------