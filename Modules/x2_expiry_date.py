import datetime
import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_expiry_date():
    while True:
        expiry_date = input('Enter expiry date (YY/MM): ').strip()
        try:
            year, month = map(int, expiry_date.split('/'))
            if not (0 <= year <= 99 and 1 <= month <= 12):
                raise ValueError()
            year += 2000 if year < 50 else 1900
            if month == 12:
                day = 31
            else:
                day = (datetime.date(year, month+1, 1) - datetime.timedelta(days=1)).day
            expiry_dt = datetime.date(year, month, day)
            return expiry_dt
        except Exception:
            print("\n[\033[91merror\033[0m] Invalid expiry date. Format should be YY/MM, e.g. 24/11")
            time.sleep(2)
            clear_screen()

def main():
    while True:
        clear_screen()
        try:
            expiry_dt = get_expiry_date()
            print(f"\nExpiry date: \033[94m{expiry_dt.strftime('%y%m%d')}\033[0m")
            input('\nPress [ENTER] to calculate another expiry date, or CTRL+C to exit...')
        except KeyboardInterrupt:
            print()
            break

if __name__ == '__main__':
    main()
