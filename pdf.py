import requests
import os
import time

def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded successfully: {save_path}")
    else:
        print(f"Failed to download {pdf_url}. Status code: {response.status_code}")

def download_pdfs_from_file(file_path):
    with open(file_path, 'r') as file:
        pdf_links = [line.strip() for line in file.readlines() if line.strip().lower().endswith('.pdf')]
    
    if pdf_links:
        for pdf_url in pdf_links:
            file_name = pdf_url.split("/")[-1]
            save_path = os.path.join(os.path.dirname(__file__), file_name)
            download_pdf(pdf_url, save_path)
            time.sleep(1)
    else:
        print(f"No PDF links found in {file_path}.")

if __name__ == "__main__":
    download_pdfs_from_file("pdfs.txt")