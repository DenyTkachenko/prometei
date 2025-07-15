from datetime import datetime, timedelta

DATE_FORMAT_MAP = {
    '%d': 'DD',
    '%m': 'MM',
    '%Y': 'YYYY'
}

def date_to_readable_format(fmt):
    for key, val in DATE_FORMAT_MAP.items():
        fmt = fmt.replace(key, val)
    return fmt

def get_upcoming_birthdays(records, days=7, out_birthday_format='%d.%m.%Y'):
    upcoming_birthdays = []
    today = datetime.today().date()

    for record in records:
        if record.birthday:
            try:
                birthday = record.birthday.date
                current_year_birthday = birthday.replace(year=today.year)

                # If there's already been a birthday this year, look for next year's.
                if current_year_birthday < today:
                    current_year_birthday = current_year_birthday.replace(year=today.year + 1)

                delta = (current_year_birthday - today).days

                if 0 <= delta <= days:
                    # Postponing greetings from the weekend to Monday
                    if current_year_birthday.weekday() == 5:  # Saturday
                        congratulation_date = current_year_birthday + timedelta(days=2)
                    elif current_year_birthday.weekday() == 6:  # Sunday
                        congratulation_date = current_year_birthday + timedelta(days=1)
                    else:
                        congratulation_date = current_year_birthday

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime(out_birthday_format)
                    })
            except Exception:
                print(f'Incorrect birthday format for {record.name.value}')
    return upcoming_birthdays