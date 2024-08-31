# EmailRequestChecker

**EmailRequestChecker** is a Python script designed to validate email addresses by sending HTTP POST requests to a specified web service. 
It reads email addresses from a file, checks each email, and categorizes them as valid or invalid based on the server’s response.

## Features

- Validates emails by sending POST requests to a specified URL.
- Handles and reports errors such as invalid URL formats and network issues.
- Outputs valid and invalid emails to the console.
- Supports custom error messages for identifying invalid emails.

## Prerequisites

- Python 3. x
- `requests` library

You can install the `requests` library using pip:

```pip install requests```
## Usage
To run the script, use the following command:
```python3 script.py <email_list_file> <url> <invalid_error>```

- email_list_file: Path to the file containing the list of email addresses (one per line).
- URL: The server URL to which the POST requests will be sent.
- invalid_error: The error message indicating an invalid email. The script will check the server’s response string to determine invalid emails.

## Example :
```python3 script.py email_list.txt http://example.com/login "Email does not exist"```
This command will read email addresses from email_list.txt, send POST requests to http://example.com/login, 
and check if the response contains the string "Email does not exist" to classify emails as invalid.

## Output
- Valid Emails: Printed to the console with the [VALID] prefix.
- Invalid Emails: Printed to the console with the [INVALID] prefix.
- Errors: Any issues encountered (e.g., network errors, unexpected responses) will be reported to the console.

## Error Handling
- Invalid URL: The script will terminate with an error message if the URL provided is not correctly formatted.
- File Not Found:  The script will terminate with an error message if the specified email list file is not found.
- HTTP Errors: The script will handle HTTP errors and print relevant messages.

## Notes
- The script assumes the web service returns JSON responses. Ensure the target server provides valid JSON data.
- The invalid_error string should match the error message returned by the server for invalid emails.

