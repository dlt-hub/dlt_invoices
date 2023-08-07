# Unstructured data to structured
 Converts unstructured data from a specified data resource to structured data using provided queries.

## Prerequisites

- Python 3.x
- `dlt` library (you can install it using `pip install dlt`)
- destination dependencies, in our case `bigquery` (`pip install bigquery`)

## Installation

Make sure you have Python 3.x installed on your system.

Install the required library by running the following command:

```shell
pip install dlt[bigquery]
```

## Init the pipeline
```sh
dlt init unstructured_data bigquery
```

## Install requirements

```shell
pip install -r requirements.txt
```

## Set credentials
1. Open `.dlt/secrets.toml`.
2. Enter the OpenAI secrets:

    ```toml
    [sources.unstructured_data]
    openai_api_key = "openai_api_key"
    ```
3. Enter your email account secrets in the same section `[sources.unstructured_data]`:

    ```toml
    host = 'imap.example.com'
    email_account = "example@example.com"
    password = 'set me up!'
    ```

Use [App password](#getting-gmail-app-password) to set the password for a Gmail account.

## Set destination credentials
1. Open `.dlt/secrets.toml`.
2. Enter the BigQuery secrets:
   ```toml
   [destination.bigquery]
   location = "US"
   [destination.bigquery.credentials]
   project_id = "set me up!"
   private_key = "set me up!"
   client_email = "set me up!"
   ```
Read more about BigQuery destination in [Destinations: BigQuery.](https://dlthub.com/docs/dlt-ecosystem/destinations/bigquery)

## Configure unstructured source
### Define queries
You must provide a dictionary of queries to be applied to the unstructured
data during processing. Each query maps a field name to a query string
that specifies how to process the field.

Queries example:
```python
queries = {
    "recipient_company_name": "Who is the recipient of the invoice? Just return the name. If you don't know, then return None",
    "invoice_amount": "What is the total amount of the invoice? Just return the amount as decimal number, no currency or text. If you don't know, then return None",
    "invoice_date": "What is the date of the invoice? Just return the date. If you don't know, then return None",
    "invoice_number": "What is the invoice number? Just return the number. If you don't know, then return None",
    "service_description": "What is the description of the service that this invoice is for? Just return the description. If you don't know, then return None",
    "phone_number": "What is the company phone number? Just return the phone number. If you don't know, then return None",
}
```

Customize the INVOICE_QUERIES dict in the `unstructured_data/settings.py` file if you want to extract
other information, or if your invoices have different structure.

## Configure inbox source
### Usage

1. Ensure that the email account you want to access allows access by less secure apps (or use an
   [app password](#getting-gmail-app-password)).
1. Replace the placeholders in `.dlt/secrets.toml` with your IMAP server hostname, email account
   credentials.
1. Customize the FILTER_EMAILS list in the `inbox/settings.py` file if you want to fetch emails only
   from specific senders.
1. Customize the GMAIL_GROUP in the `inbox/settings.py` file if you want to fetch emails
   for specific Google Group.
1. Set the STORAGE_FOLDER_PATH in the `inbox/settings.py` file to the folder where you want to save
   attachments (if required).
1. Set the DEFAULT_START_DATE in the `inbox/settings.py` file to the date you want to fetch emails from.

### Accessing Gmail Inbox

To connect to the Gmail server, we need the below information.

- SMTP server DNS. Its value will be 'imap.gmail.com' in our case.
- SMTP server port. The value will be 993. This port is used for Internet message access protocol
  over TLS/SSL.

### Set up Gmail with a third-party email client

An app password is a 16-digit passcode that gives a less secure app or device permission to access
your Google Account. App passwords can only be used with accounts that have 2-Step Verification
turned on.

Step 1: Create and use App Passwords
1. Go to your Google Account.
1. Select Security.
1. Under "How you sign in to Google", select **2-Step Verification** -> Turn it on.
1. Select again **2-Step Verification**.
1. At the bottom of the page, select App passwords.
1. Enter a name of device that helps you remember where you’ll use the app password.
1. Select Generate.
1. To enter the app password, follow the instructions on your screen. The app password is the
   16-character code that generates on your device.
1. Select Done.

Read more in
[this article](https://pythoncircle.com/post/727/accessing-gmail-inbox-using-python-imaplib-module/)
or
[Google official documentation.](https://support.google.com/mail/answer/185833#zippy=%2Cwhy-you-may-need-an-app-password)

Step 2: Turn on IMAP in Gmail
1. In Gmail, in the top right, click Settings -> See all settings.
1. At the top, click the Forwarding and POP/IMAP tab.
1. In the IMAP Access section, select Enable IMAP.
1. At the bottom, click Save Changes.

Read more in [official Google documentation.](https://support.google.com/a/answer/9003945#zippy=%2Cstep-turn-on-imap-in-gmail)


## Run the pipeline

```python
python unstructured_data_pipeline.py
```

The `unstructured_to_structured_source` function includes a transformer-type
resource that processes each item using the `unstructured` library.
The processing results are retrieved as a dictionary, which has a structure similar to the following:
```python
{
    'file_name': '/test_data/invoice_1.pdf',
    'recipient_company_name': 'XYZ Corporation',
    'invoice_amount': '11235.00',
    'invoice_date': 'June 30, 2023',
    'invoice_number': 'INV-549283',
    'service_description': 'Premium widget delivery and installation services',
    'phone_number': 'None'
    'metadata': {...},
}
```
Then `dlt` saves all processed structured data to the database (e.g. bigquery).


## Deploy

Run the command:

```shell
dlt deploy --schedule "0 18 * * *" unstructured_data_pipeline.py github-action 
```

Read more in [Deploy with GitHub Actions.](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-github-actions)