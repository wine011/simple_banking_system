import create_new_acc


def log_in_action():

    global user_input_acc

    user_input_acc = input("Enter your card number:\n")
    user_input_pin = input("Enter your PIN:\n")

    # Check the account number is in database or not
    create_new_acc.cur.execute("""SELECT number, pin FROM card
                WHERE number = ?""", (user_input_acc,))
    check_acc = create_new_acc.cur.fetchone()
    create_new_acc.conn.commit()
    #print(check_acc)

    if check_acc is None:
        print("Wrong card number or PIN!")
    elif check_acc is not None:
        if check_acc[0] == user_input_acc and check_acc[1] == user_input_pin:
            print("You have successfully logged in!")
            while True:
                user_log_in_action = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
                if user_log_in_action == "1":
                    check_balance()

                elif user_log_in_action == "2":
                    add_income()

                elif user_log_in_action == "3":
                    do_transfer()

                elif user_log_in_action == "4":
                    close_account()
                    return
                    

                elif user_log_in_action == "5":
                    print("Logged Out")
                    return

                elif user_log_in_action == "0":
                    exit()
        else:
            print("Wrong card number or PIN!")


def check_balance():
    global user_input_acc

    create_new_acc.cur.execute("""SELECT balance FROM card WHERE number = ?""", (user_input_acc,))
    balance = create_new_acc.cur.fetchone()
    print(f"Balance: {balance[0]}")


def add_income():
    global user_input_acc
    add_balance = int(input("Enter income:\n"))

    create_new_acc.cur.execute("""UPDATE card SET balance = balance + ?
                                WHERE number = ?""", (add_balance, user_input_acc))
    create_new_acc.conn.commit()
    print("Income was added!")


def do_transfer():
    global user_input_acc
    # Check account no is in database or not
    print("Transfer")
    transfer_card_no = input("Enter card number:\n")

    check_luhn = list([int (x) for x in transfer_card_no])
    temp3 = []
    temp4 = []
    for i in range(0, len(check_luhn)):
        if i % 2 == 0:
            temp3.append(check_luhn[i] * 2)
        else:
            temp3.append(check_luhn[i])
    #print(temp3)

    for x in temp3:
        if x > 9 :
            x -= 9
            temp4.append(x)
        else:
            temp4.append(x)
    #print(temp4)

    sum = 0
    for x in temp4:
        sum += x
    #print(sum)

    if sum % 10 == 0 :
        #print("Card Passed Luhn Algorithm")
        create_new_acc.cur.execute("""SELECT number FROM card
                                WHERE number = ?""", (transfer_card_no,))
        sql_check = create_new_acc.cur.fetchone()


        if sql_check is None:
            print("Such a card does not exist.")

        elif sql_check[0] == user_input_acc:
            print("You can't transfer money to the same account!")

        elif sql_check[0] == transfer_card_no:
            u_input_balance = int(input("Enter how much money you want to transfer:\n"))
            create_new_acc.cur.execute("""SELECT balance FROM card
                                WHERE number = ?""", (user_input_acc,))
            check_balance = create_new_acc.cur.fetchone()

            if check_balance[0] > u_input_balance or check_balance[0] == u_input_balance:
                create_new_acc.cur.execute("""UPDATE card SET balance = balance - ?
                WHERE number = ?""", (u_input_balance, user_input_acc,))
                create_new_acc.cur.execute("""UPDATE card SET balance = balance + ?
                WHERE number = ?""", (u_input_balance, transfer_card_no))
                create_new_acc.conn.commit()
                print("Success")
            else:
                print("Not enough money!")


    else:
        print("Probably you made a mistake in the card number. Please try again!")


def close_account():
    global row_id
    create_new_acc.cur.execute("""DELETE FROM card
                                WHERE number = ?""", (user_input_acc,))
    #create_new_acc.cur.execute("""UPDATE card SET id = ? - 1""")
    create_new_acc.conn.commit()
    print("The account has been closed!")



    
