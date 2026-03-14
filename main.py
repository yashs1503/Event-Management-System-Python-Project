from admin import Admin
from organizer import Organizer
from participant import Participant


def main():
    while True:
        print("\n" + "=" * 60)
        print("                EVENT MANAGEMENT SYSTEM ")
        print("=" * 60)
        print("""
        1. Admin 
        2. Organizer
        3. Participant
        4. Exit
        """)
        
        ch = input("Enter your choice: ").strip()
        print()

        if ch == '1':
            Admin().admin_menu()
        elif ch == '2':
            Organizer().organizer_login()
        elif ch == '3':
            Participant().participant_login()
        elif ch == '4':
            print("Thank you for using Event Management System. Goodbye!")
            break
        else:
            print("  Invalid Choice. Please try again.")


if __name__ == "__main__":
    main()
