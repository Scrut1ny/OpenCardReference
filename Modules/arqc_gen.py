import hashlib, hmac, re

# set constant variables
MDK = "0123456789ABCDEFFEDCBA9876543210"
MK = "9249345E0220CEBA0D20D6A2453BF407"
AMOUNT_AUTHORIZED = "000000001000"
AMOUNT_OTHER = "000000000000"
COUNTRY_CODE = "0840"
TVR = "0000000000"
CURRENCY_CODE = "0840"
TYPE = "00"
UN = "30901B6A"
AIP_ICC = "3C00"
ATC_ICC = "0001"
AID_ICC = "03A4A082"
PAD = "800000"


# ask for user input for PAN and date
while True:
    pan = input("Please enter the PAN (Card Number): ")
    if not re.match("^[0-9]{16}$", pan):
        print("Invalid PAN format. Please enter a 16-digit number.")
        continue
    else:
        break

while True:
    date = input("Please enter the date (YYMMDD): ")
    if not re.match("^[0-9]{6}$", date):
        print("Invalid date format. Please enter a 6-digit number in YYMMDD format.")
        continue
    else:
        break


# combine all variables
Terminal_Data = AMOUNT_AUTHORIZED + AMOUNT_OTHER + COUNTRY_CODE + TVR + CURRENCY_CODE + date + TYPE + UN + AIP_ICC + ATC_ICC + AID_ICC + PAD

ARQC = hmac.new(bytes.fromhex(MK), Terminal_Data, hashlib.sha256).hexdigest().upper()[:16]

# print the result
print("ARQC:", ARQC)
