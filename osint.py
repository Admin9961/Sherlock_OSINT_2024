from googlesearch import search
import time
import subprocess
import os
from pdf import download_pdf, download_pdfs_from_file
from functools import wraps
from requests.exceptions import HTTPError

def handle_http_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = kwargs.pop('max_retries', 3)
        sleep_time = kwargs.pop('sleep_time', 2)

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                if e.response.status_code == 429:
                    print(f"Received HTTP 429 error. Retrying after {sleep_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                else:
                    print(f"Error: {e}")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
        return []

    return wrapper

@handle_http_error
def search_google(query, num_results=5, sleep_time=2):
    results = list(search(query, num_results=num_results))

    pdf_links = [link for link in results if link.lower().endswith('.pdf')]
    with open('pdfs.txt', 'w') as file:
        file.write('\n'.join(pdf_links))

    with open('links_results.txt', 'w') as file:
        file.write('\n'.join(results))

    for index, link in enumerate(results, start=1):
        print(f"{index}. {link}")

    return results

def download_pdf_prompt():
    while True:
        download_choice = input("Do you want to download all PDFs? (yes/no): ").lower()
        if download_choice in ['yes', 'no']:
            return download_choice == 'yes'
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def osint_persons():
    usernames = input("Enter multiple usernames separated by a comma: ")
    usernames_list = [username.strip() for username in usernames.split(',')]

    while True:
        try:
            num_results = int(input("Enter the number of results to download for all usernames combined: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid numerical value.")

    all_search_results = []

    for username in usernames_list:
        search_query = f"{username}"
        search_results = search_google(search_query, num_results=num_results)

        print(f"\nSearch results for {username}:")
        for index, link in enumerate(search_results, start=1):
            print(f"{index}. {link}")
            time.sleep(3)

        all_search_results.extend(search_results)

        time.sleep(3)

    pdfs_file_path = 'pdfs.txt'
    if os.path.exists(pdfs_file_path):
        print("\nDownloading PDFs from pdfs.txt:")
        download_pdfs_from_file(pdfs_file_path)

    if download_pdf_prompt():
        subprocess.run(["python", "pdf.py"])

    print("\nCombined Search Results for all Usernames:")
    for index, link in enumerate(all_search_results, start=1):
        print(f"{index}. {link}")

def main():
    while True:
        osint_type = input("Do you want to osint general things or persons? Enter 'osint' or 'persons': ").lower()
        if osint_type in ['osint', 'persons']:
            break
        else:
            print("Invalid input. Please enter 'osint' or 'persons'.")

    if osint_type == 'osint':
        search_query_input = input("Enter the search query: ")

        while True:
            try:
                num_results_input = int(input("Enter the number of results: "))
                sleep_time_input = float(input("Enter the sleep time between requests (in seconds): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid numerical value.")

        search_results = search_google(search_query_input, num_results=num_results_input, sleep_time=sleep_time_input)

        if download_pdf_prompt():
            subprocess.run(["python", "pdf.py"])
        else:
            print("Continuing without downloading PDFs.")
    elif osint_type == 'persons':
        osint_persons()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()