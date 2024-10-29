from dateutil import parser

def format_date(date_string):
    try:
        # Parse the date string using dateutil's parser, which can handle multiple formats
        parsed_date = parser.parse(date_string)
        # Return the date in the desired format YYYY-MM-DD
        return parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        return ""
