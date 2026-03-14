import json

class Participant:
    def __init__(self):
        self.events_path = r'D:\FBS Work\Python\Project\data\events.json'
        self.registration_path = r'D:\FBS Work\Python\Project\data\registrations.json'

    def load_data(self, path):
        try:
            with open(path, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def store_data(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def participant_login(self):
        print("\n" + "=" * 40)
        print("          PARTICIPANT LOGIN")
        print("=" * 40)

        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return
        print(f"\nWelcome, {name}!")
        self.participant_menu(name)

    def view_event(self):
        events = self.load_data(self.events_path)
        if not events:
            print("No events available.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<6}{'NAME':<20}{'DATE':<15}{'TIME':<12}{'LOCATION':<15}")
        print("-" * 70)
        for e in events:
            print(f"{e['id']:<6}{e['name']:<20}{e['date']:<15}{e['time']:<12}{e['location']:<15}")
        print("=" * 70)

    def _process_payment(self):
        print("\nPayment Options:")
        print("1. Cash payment")
        print("2. Card Payment (Dummy)")

        ch = input("Choose (1/2): ").strip()
        if ch == '1':
            print("Cash Payment selected. Payment due at event venue.")
            return {'method': 'Cash Payment', 'paid': False}
        elif ch == '2':
            card = input("Enter Card Number: ").strip()
            cvv = input("Enter CVV: ").strip()
            if not (card.isdigit() and 13 <= len(card) <= 19):
                print("Invalid Card Number.")
                return None
            if not (cvv.isdigit() and len(cvv) in (3, 4)):
                print("Invalid CVV.")
                return None
            print("Card payment successfu.")
            return {'method': 'CARD', 'paid': True, 'last4': card[-4:]}
        else:
            print("Invalid choice.")
            return None

    def register_event(self, username):
        events = self.load_data(self.events_path)
        registrations = self.load_data(self.registration_path)

        if not events:
            print("No events available.")
            return

        print("\nAvailable Events:")
        for e in events:
            print(f" - {e['id']} : {e['name']} ({e['date']}, {e['location']})")

        event_id = input("\nEnter Event ID to register: ").strip()
        event = next((e for e in events if e['id'] == event_id), None)
        if not event:
            print("Event not found.")
            return

        if any(r['user'] == username and r['event_id'] == event_id for r in registrations):
            print("You already registered for this event.")
            return

        payment = self._process_payment()
        if payment is None:
            print("Payment failed.")
            return

        registrations.append({
            'user': username,
            'event_id': event['id'],
            'event_name': event['name'],
            'event_date': event['date'],
            'event_location': event['location'],
            'payment': payment
        })

        self.store_data(self.registration_path, registrations)
        print(f"Successfully registered for {event['name']}.")

    def view_registrations(self, username):
        registrations = self.load_data(self.registration_path)
        my_regs = [r for r in registrations if r['user'] == username]

        if not my_regs:
            print("No registrations found.")
            return

        print("\n" + "=" * 90)
        print(f"{'EVENT ID':<10}{'NAME':<20}{'DATE':<15}{'LOCATION':<20}{'PAYMENT':<15}")
        print("-" * 90)
        for r in my_regs:
            pay = r['payment']['method']
            print(f"{r['event_id']:<10}{r['event_name']:<20}{r['event_date']:<15}{r['event_location']:<20}{pay:<15}")
        print("=" * 90)

    def cancel_registration(self, username):
        registrations = self.load_data(self.registration_path)
        event_id = input("Enter Event ID to cancel: ").strip()
        new_regs = [r for r in registrations if not (r['user'] == username and r['event_id'] == event_id)]
        self.store_data(self.registration_path, new_regs)
        print("Registration cancelled.")

    def give_feedback(self, username):
        feedback = input("Enter your feedback: ").strip()
        if not feedback:
            print("Feedback cannot be empty.")
            return
        with open(r'D:\FBS Work\Python\Project\feedback.txt', 'a') as fp:
            fp.write(f"{username}: {feedback}\n")
        print("Thank you for your feedback!")

    def participant_menu(self, username):
        while True:
            print("\n" + "=" * 50)
            print("           PARTICIPANT MENU")
            print("=" * 50)
            print("""
            1. View Events
            2. Register for Event
            3. View My Registrations
            4. Cancel Registration
            5. Give Feedback
            6. Log Out
            """)
            ch = input("Enter your choice: ").strip()

            if ch == '1':
                self.view_event()
            elif ch == '2':
                self.register_event(username)
            elif ch == '3':
                self.view_registrations(username)
            elif ch == '4':
                self.cancel_registration(username)
            elif ch == '5':
                self.give_feedback(username)
            elif ch == '6':
                print("Logged out.")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    Participant().participant_login()
