import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from plyer import notification

# Function to fetch webpage content
def fetch_webpage(url):
    response = requests.get(url)
    return response.text

# Function to extract announcements and dates
def extract_announcements(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    announcements = []
    dates_list = []

    # Find all announcement entries
    announcement_entries = soup.find_all('div', class_='announcement-lists--rows-wrapper')

    # Extract announcements and dates from each entry
    for entry in announcement_entries:
        # Extract date
        date_tag = entry.find('time')
        date = date_tag.get_text(strip=True) if date_tag else ''

        # Extract announcement title
        title_tag = entry.find('a')
        announcement_title = title_tag.get_text(strip=True) if title_tag else ''

        announcements.append(announcement_title)
        dates_list.append(date)
        
        dates=[date.split(', ')[1] for date in dates_list]

    return announcements, dates

# Main function
def main():
    url = 'https://fme.aegean.gr/el/news'
    keywords = ['Καθομολόγηση', 'keyword2']

    # Fetch webpage content
    html_content = fetch_webpage(url)

    # Extract announcements and dates
    announcements, dates = extract_announcements(html_content)
    
    # Concatenate Lists
    combined = list(zip(dates, announcements))
    sorted_combined = sorted(combined, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'), reverse=True)

    # Turn them into dataframe
    df = pd.DataFrame(sorted_combined, columns=['Date', 'Announcement'])
    print(df)

    # Get Current Date
    current_date = datetime.now().strftime('%d/%m/%Y')
    
    # Filter dataframe based on date
    filtered_df = df[df['Date'] == current_date]
    
    # Filter date filtered dataframe based on keywords
    keyword_filtered_df = filtered_df[filtered_df['Announcement'].str.contains('|'.join(keywords), case=False)]

    # Notify user of the results
    if not keyword_filtered_df.empty:
        message = "Announcements for today containing keywords were found."

        # Display notification
        notification.notify(
            title='Keyword Filtered Announcements',
            message=message,
            app_name='Announcement Alert',
            timeout=15  
        )
    else:
        message = "No announcements today."

        # Display notification
        notification.notify(
            title='No Announcements Today',
            message=message,
            app_name='Announcement Alert',
            timeout=10  
        )

if __name__ == '__main__':
    main()
