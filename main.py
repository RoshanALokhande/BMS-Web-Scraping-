import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Extract event details
def get_event_details(doc):
    try:
        # Find event cards
        event_cards = doc.find_all('div', class_=lambda x: x and 'sc-1ljcxl3-0' in x)
        if not event_cards:
            print("No event cards with class 'sc-1ljcxl3-0'")
            event_cards = doc.find_all('div', {'data-testid': 'event-card'})
            if not event_cards:
                print("No event cards with data-testid='event-card'")
                event_cards = doc.find_all('div', class_=lambda x: x and ('card' in x.lower() or 'event' in x.lower()))
        
        events = []
        for card in event_cards:
            event = {}
            # Name
            name_tag = card.find('div', class_=lambda x: x and 'sc-7o7nez-0' in x and 'elfplV' in x)
            event['Name'] = name_tag.text.strip() if name_tag else "Unknown"
            if not name_tag:
                print("Name tag not found")
            
            #City
            event['City Name'] = City

            # Venue
            venue_tag = card.find('div', class_=lambda x: x and 'sc-7o7nez-0' in x and 'FnmcD' in x)
            if not venue_tag:
                venue_tag = card.find('div', class_=lambda x: x and 'venue' in x.lower() or 'location' in x.lower())
            event['Venue'] = venue_tag.text.strip() if venue_tag else "Unknown"
            if not venue_tag:
                print("Venue tag not found")
                
            #Date Of the Event
            
            
            # djdFxA_tags = card.select('div', class_=lambda x: x and 'sc-7o7nez-0' in x and 'djdFxA' in x)
            # event['Date of Event'] =  djdFxA_tags[0].text.strip() if len( djdFxA_tags) > 0 else "Unknown"
            # event['Timing '] =  djdFxA_tags[1].text.strip() if len( djdFxA_tags) > 1 else "Unknown"
            # event['Duration'] =  djdFxA_tags[2].text.strip() if len( djdFxA_tags) > 0 else "Unknown"
            # event['Age_Limit '] =  djdFxA_tags[3].text.strip() if len( djdFxA_tags) > 1 else "Unknown"
            
            # if len(bsZIkT_tags) < 1:
            #     print("Category tag not found")
            # if len(bsZIkT_tags) < 2:
            #     print("Price tag not found")
            

            # Category and Price (same class, differentiate by order)
            bsZIkT_tags = card.find_all('div', class_=lambda x: x and 'sc-7o7nez-0' in x and 'bsZIkT' in x)
            event['Category'] = bsZIkT_tags[0].text.strip() if len(bsZIkT_tags) > 0 else "Unknown"
            event['Price'] = bsZIkT_tags[1].text.strip() if len(bsZIkT_tags) > 1 else "Unknown"
            if len(bsZIkT_tags) < 1:
                print("Category tag not found")
            if len(bsZIkT_tags) < 2:
                print("Price tag not found")

            # Image
            image_parent = card.find('div', class_=lambda x: x and 'sc-133848s-2' in x and 'sc-1t5vwh0-1' in x)
            image_tag = image_parent.find('img') if image_parent else None
            event['Image_URL'] = image_tag.get('src') or "Unknown" if image_tag else "Unknown"
            if not image_tag:
                print("Image tag not found")

            # Promoted (placeholder)
            promoted_tag = card.find('div', class_=lambda x: x and 'promoted' in x.lower())
            if not promoted_tag:
                promoted_tag = card.find('div', string=lambda x: x and 'PROMOTED' in x.upper())
            event['promoted'] = "Yes" if promoted_tag else "No"
            if not promoted_tag:
                print("Promoted tag not found")
                
            

            events.append(event)
        
        print(f"Found {len(events)} events")
        return events
    except Exception as e:
        print(f"Error extracting events: {e}")
        return []

# Store events
def store_events_in_dict(doc):
    try:
        events = get_event_details(doc)
        return {f"event_{i+1}": event for i, event in enumerate(events)}
    except Exception as e:
        print(f"Error storing events: {e}")
        return {}



#City Name Inputing

City = input("Please Enter City Name: ")

# Setup browser

options = Options()
options.headless = False  # Non-headless for CAPTCHA
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
try:
    driver = uc.Chrome(options=options)
    print("Browser started.")
except Exception as e:
    print(f"Error starting browser: {e}")
    exit(1)

try:
    # Load page
    print("Loading page...")
    driver.get(f'https://in.bookmyshow.com/explore/events-{City}')
    
    # Wait for page
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page loaded.")
    except TimeoutException as e:
        print(f"Page load timeout: {e}")
        html = driver.page_source[:2000]
        print("Partial HTML:", html)
        raise

    # Wait for event card
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-1ljcxl3-0, div[data-testid="event-card"]')))
        print("Event card found.")
    except TimeoutException as e:
        print(f"No event cards found: {e}")
        html = driver.page_source[:2000]
        print("Partial HTML:", html)

    # Scroll
    print("Scrolling...")
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    print("Scrolling done.")

    # Get HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Check for Cloudflare/CAPTCHA
    if "cloudflare" in html.lower() or "captcha" in html.lower():
        print("Cloudflare or CAPTCHA detected. Solve CAPTCHA in browser and wait 10 seconds.")
        time.sleep(10)  # Give time to solve CAPTCHA

    # Extract and save
    events_dict = store_events_in_dict(soup)
    if events_dict:
        events_list = [{"event_id": key, **value} for key, value in events_dict.items()]
        df = pd.DataFrame(events_list)
        df.to_excel(f"bookmyshow_{City}events.xlsx", index=False, engine='openpyxl')
        print(f"Saved to bookmyshow_{City}_events.xlsx")
    else:
        print("No events extracted.")

    # Save HTML
    with open('webpage.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("HTML saved to webpage.html")

except WebDriverException as e:
    print(f"WebDriver error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    try:
        driver.quit()
        print("Browser closed.")
    except Exception as e:
        print(f"Error closing browser: {e}")