# utils.py
import re
from datetime import datetime

def validate_contact(contact):
    """Validate phone number (simple validation)"""
    return bool(re.match(r'^[0-9]{10,15}$', contact))

def validate_date(date_str):
    """Validate date in YYYY-MM-DD HH:MM format"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

def display_table(headers, rows):
    """Display data in a formatted table"""
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create separator
    separator = '+' + '+'.join(['-' * (w + 2) for w in col_widths]) + '+'
    
    # Print header
    print(separator)
    header_row = '|' + '|'.join([f' {headers[i]:^{col_widths[i]}} ' for i in range(len(headers))]) + '|'
    print(header_row)
    print(separator)
    
    # Print rows
    for row in rows:
        row_str = '|' + '|'.join([f' {str(row[i]):^{col_widths[i]}} ' for i in range(len(headers))]) + '|'
        print(row_str)
    print(separator)

def get_valid_input(prompt, validation_func, error_msg="Invalid input. Try again."):
    """Get validated user input"""
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_msg)

def format_date(iso_date):
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return iso_date
