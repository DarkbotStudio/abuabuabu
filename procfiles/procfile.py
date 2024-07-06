def calculate_rank(popularity):
    if 0 == popularity <= 99:
        return 'D'
    elif 100 <= popularity <= 999:
        return 'C'
    elif 1000 <= popularity <= 9999:
        return 'B'
    elif 10000 <= popularity <= 99999:
        return 'A'
    elif 100000 <= popularity <= 999999:
        return 'S'
    elif popularity >= 1000000:
        return 'S+'
def extract_data(text):
    return text.split() if len(text.split()) > 1 else None