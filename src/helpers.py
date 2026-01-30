import os
import PyPDF2
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from sympy import Options

from src.constants import RESSOURCES_DIR

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawl_html_page(url):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()  # Return the formatted HTML content
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    

def read_files():
    files = os.listdir(RESSOURCES_DIR)
    pdf_files = [file for file in files if file.lower().endswith(".pdf")]
    if len(pdf_files) > 0:
        # initialize sum of pdfs
        pdf_context = ""
        for pdf in pdf_files:
            # Open the PDF file
            pdf_file = open(f"{RESSOURCES_DIR}/{pdf}", "rb")
            # Create a PDF object
            pdf_reader = PyPDF2.PdfReader (pdf_file)
            # Initialize an empty string to store the extracted text
            doc = ""
            # Iterate through each page and extract text
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                # Replace "\n" with a normal space (" ")
                page_text = page_text.replace("\n", " ")
                doc += page_text

            # Close the PDF file
            pdf_file.close()
            # add pdfs
            pdf_context += doc
    else:
        print("No pdfs Found")
        return "No pdfs Found"

    # return response
    return pdf_context


def read_file(pdf_name: str):
        # Open the PDF file
        pdf_file = open(f"{RESSOURCES_DIR}/{pdf_name}", "rb")
        # Create a PDF object
        pdf_reader = PyPDF2.PdfReader (pdf_file)
        # Initialize an empty string to store the extracted text
        context = ""
        # Iterate through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            # Replace "\n" with a normal space (" ")
            page_text = page_text.replace("\n", " ")
            context += page_text

        # Close the PDF file
        pdf_file.close()
        # add pdfs
        print(f"adding {pdf_name} to context")
        return context





def crawl_for_pdfs(base_url, output_folder="downloaded_pdfs"):
    # Create storage folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initial setup
    domain = urlparse(base_url).netloc
    queue = [base_url]
    visited = set()
    downloaded_pdfs = set()

    print(f"🚀 Starting crawl on: {base_url}")

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        print(f"🔍 Scanning: {url}")

        try:
            # Respectful delay
            time.sleep(1) 
            response = requests.get(url, timeout=10)
            
            # Ensure we only parse HTML pages
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                print(f"not text/html")

                continue

            print("html parser")
            soup = BeautifulSoup(response.text, 'html.parser')

            a_href = soup.find_all('a', href=True)
            print(f"a_href {a_href}")

            for link in soup.find_all('a', href=True):
                # Resolve relative paths to absolute URLs
                full_url = urljoin(url, link['href'])
                parsed_url = urlparse(full_url)
                print(f"full_url {full_url}")
                print(f"parsed_url {parsed_url}")


                # 1. PDF DOWNLOAD LOGIC
                if parsed_url.path.lower().endswith('.pdf'):
                    if full_url not in downloaded_pdfs:
                        download_pdf(full_url, output_folder)
                        downloaded_pdfs.add(full_url)
                
                # 2. DOMAIN FILTERING LOGIC
                # Only add to queue if it belongs to the same domain and hasn't been visited
                elif parsed_url.netloc == domain:
                    if full_url not in visited and full_url not in queue:
                        # Remove fragments (#section) to avoid duplicate scanning
                        clean_url = full_url.split('#')[0]
                        queue.append(clean_url)

        except Exception as e:
            print(f"⚠️ Error accessing {url}: {e}")

def download_pdf(url, folder, referer=None, cookies=None):
    try:
        file_name = os.path.join(folder, os.path.basename(urlparse(url).path))
        print(f"  📥 Downloading: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        if referer:
            headers['Referer'] = referer
        
        session = requests.Session()
        if cookies:
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain'))
        
        with session.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"  ❌ Failed to download {url}: {e}")


def crawl_and_download_pdfs(base_url, output_folder="downloaded_pdfs"):
    # Create storage folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initial setup
    domain = urlparse(base_url).netloc
    queue = [base_url]
    visited = set()
    downloaded_pdfs = set()

    # Selenium setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Speed up loading
    
    # Set download preferences
    download_dir = os.path.abspath(output_folder)
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    
    driver = webdriver.Chrome(options=options)

    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    print(f"🚀 Starting crawl on: {base_url}")

    try:
        while queue:
            url = queue.pop(0)
            if url in visited:
                continue
            
            visited.add(url)
            print(f"🔍 Scanning: {url}")

            try:
                # Respectful delay
                time.sleep(3)
                driver.get(url)
                
                # Wait for page to load (wait for body)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Additional wait for dynamic content
                time.sleep(5)
                
                # Get cookies for requests
                cookies = driver.get_cookies()

                # Find all links
                links = driver.find_elements(By.TAG_NAME, "a")

                print(f"Found {len(links)} links on {url}")

                for link in links:
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    
                    print(f"Processing link: {href}")
                    
                    # Resolve relative URLs
                    full_url = urljoin(url, href)
                    parsed_url = urlparse(full_url)
                    
                    # Check if it's a PDF link
                    if parsed_url.path.lower().endswith('.pdf') or '.pdf' in parsed_url.path.lower():
                        print(f"Found PDF: {full_url}")
                        if full_url not in downloaded_pdfs:
                            # Download using Selenium
                            file_name = os.path.basename(urlparse(full_url).path)
                            file_path = os.path.join(output_folder, file_name)
                            print(f"  📥 Downloading via browser: {full_url}")
                            driver.get(full_url)
                            # Wait for download to complete
                            timeout = 30
                            start_time = time.time()
                            while not os.path.exists(file_path) and (time.time() - start_time) < timeout:
                                time.sleep(1)
                            if os.path.exists(file_path):
                                print(f"  ✅ Downloaded: {file_name}")
                                downloaded_pdfs.add(full_url)
                            else:
                                print(f"  ❌ Failed to download {full_url}: Timeout")
                    
                    # Check if it's an internal link to crawl
                    elif parsed_url.netloc == domain or not parsed_url.netloc:  # relative links
                        clean_url = full_url.split('#')[0]  # remove fragments
                        if clean_url not in visited and clean_url not in queue:
                            print(f"Adding to queue: {clean_url}")
                            queue.append(clean_url)

            except Exception as e:
                print(f"⚠️ Error accessing {url}: {e}")
    finally:
        driver.quit()

    print(f"✅ Crawl completed. Downloaded {len(downloaded_pdfs)} PDFs.")