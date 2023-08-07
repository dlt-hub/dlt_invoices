base_query = "Forget previous document, process the new one as something new with another structure. If you don't know, then return None"
INVOICE_QUERIES = {
    "recipient_company_name": f"Who is the recipient of the invoice? Just return the company name. {base_query}",
    "invoice_amount": f"What is the total amount of the invoice? Just return the amount as decimal number, no currency or text. {base_query}",
    "invoice_date": f"What is the date of the invoice? Just return the date. {base_query}",
    "invoice_number": f"What is the invoice number? Just return the number. {base_query}",
    "service_description": f"What is the description of the service that this invoice is for? Just return the description. {base_query}",
    "phone_number": f"What is the company phone number? Just return the phone number. {base_query}",
}
