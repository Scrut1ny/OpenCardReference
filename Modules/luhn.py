def luhn_checksum(number: str) -> bool:
    checksum = 0
    is_even = False

    for i in range(len(number) - 1, -1, -1):
        if number[i].isdigit():
            d = int(number[i])
            if is_even:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
            is_even = not is_even

    return checksum % 10 == 0

if __name__ == "__main__":
    # ANSI color codes
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    try:
        user_input = input("Enter a number to validate: ").strip()
        if luhn_checksum(user_input):
            print(f"{GREEN}VALID: {user_input}{RESET}")
        else:
            print(f"{RED}INVALID: {user_input}{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted by user. Exiting.{RESET}")
