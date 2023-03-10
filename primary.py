import create_new_acc
import log_in

# Define main function
def main():
    while True:
        user_action = input("1. Create an account\n2. Log into account\n0. Exit\n")

        if user_action == "1":
            create_new_acc.row_id += 1
            create_new_acc.create_new_acc()
        
        elif user_action == "2":
            log_in.log_in_action()

        elif user_action == "0":
            print("Bye")
            exit()

main()