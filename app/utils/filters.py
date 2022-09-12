# Jinja helper functions (formatting)
# format date to mm/dd/yy string
def format_date(date):
    return date.strftime('%m/%d/%y')

# format url to readable string
def format_url(url):
    return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# format plurals for 'comment', other english words
def format_plural(amount, word):
    if amount != 1:
        return word + 's'
    
    return word