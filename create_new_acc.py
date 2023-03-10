import random
import sqlite3



row_id = 0

conn = sqlite3.connect("card.s3db")

cur = conn.cursor()

cur.execute("DROP TABLE card")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY,
    number TEXT UNIQUE,
    pin TEXT,
    balance INTEGER DEFAULT 0
);""")

conn.commit()



# Create new account number using Luhn Algorithm
def create_new_acc():
    global row_id

    temp1 = []  # Multiply_list
    temp2 = []  # Subtract_list

    """Luhn Algorithm : multiply by 2 to odd digits
    no greater than 9 -> subtract 9 from the numbers greater than 9
    add all digits
    modulo by 10
    --> must be divisible ; number % 10 == 0 """

    print("Your card has been created")

    # Generate BIN = IIN (400000) + 9 digits (account identifier-random)
    # store in list as int -- need to work with each item
    IIN = [4, 0, 0, 0, 0, 0]    
    account_no_random = str(random.randrange(100000000, 999999999))
    account_no = list([int (x) for x in account_no_random])
    card_number = IIN + account_no

    # Multiply odd digits by 2. Index starts with 0.
    for i in range(0, len(card_number)):
        if i % 2 == 0:
            temp1.append(card_number[i] * 2)

        else:
            temp1.append(card_number[i])

    #print(f"Multiply list: {temp1}")
    # Subtract 9 from greather than 9 numbers
    for x in temp1:
        if x > 9:
            x -= 9
            temp2.append(x)

        else:
            temp2.append(x)
    #print(f"Subtract list: {temp2}")
    # Add all numbers in subtract list
    sum = 0
    for x in temp2:
        sum += x
    #print(f"sum:{sum}")

    # Calculate checksum
    checksum = sum % 10
    if checksum == 0:
        card_number.append(checksum)
     
    else:
        checksum_no = 10 - checksum
        card_number.append(checksum_no)
    
    card_no = "".join(map(str, card_number))
    print(f"Your card number:\n{card_no}")

    # Generate 4 pin digits
    pin_no = random.randint(1000, 9999)
    print(f"Your card PIN:\n{pin_no}")

    
    cur.execute("""INSERT INTO card (id, number, pin)
                VALUES (?, ?, ?)""", (row_id, card_no, pin_no))
    conn.commit()

    