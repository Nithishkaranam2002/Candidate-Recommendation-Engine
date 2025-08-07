import re

def extract_email_phone(text):
    # Simple regex-based extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){1,2}\d{4}\b', text)
    email = email_match.group(0) if email_match else ""
    phone = phone_match.group(0) if phone_match else ""
    return email, phone
def clean_text(text):
    """
    Basic text cleanup: remove extra whitespace.
    """
    import re
    text = re.sub(r"\s+", " ", text)
    return text.strip()
