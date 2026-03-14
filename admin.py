import json
import getpass


class Admin:
    def __init__(self):
        self.events_path = r'D:\FBS Work\Python\Project\data\events.json'
        self.organizer_path = r'D:\FBS Work\Python\Project\data\organizers.json'

    def load_data(self, path):
        try:
            with open(path, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def store_data(self, path, data):
        with open(path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def admin_login(self):
        print("\n" + "=" * 40)
        print("               ADMIN LOGIN")
        print("=" * 40)
        username = input("Enter Username: ").strip()
        password = getpass.getpass("Enter Password: ").strip()

        if username == 'admin' and password == '1234':
            print("Login Successful!")
            return True
        else:
            print("Invalid Login Credentials.")
            return False

    def add_event(self):
        events = self.load_data(self.events_path)
        organizers = self.load_data(self.organizer_path)

        print("\n" + "=" * 40)
        print("          ADD NEW EVENT")
        print("=" * 40)

        e_id = input("Enter Event Id: ").strip()
        e_name = input("Enter Event Name: ").strip()
        e_date = input("Enter Event Date (YYYY-MM-DD): ").strip()
        e_time = input("Enter Event Time (HH:MM AM/PM): ").strip()
        e_location = input("Enter Event Location: ").strip()

        if not all([e_id, e_name, e_date, e_time, e_location]):
            print("All fields are required.")
            return

        if any(e['id'] == e_id for e in events):
            print("Event Id already exists.")
            return
        
        if len(e_date) != 10 or e_date[4] != '-' or e_date[7] != '-':
            print("Date must be (YYYY-MM-DD) format.")
            return

        e_time = e_time.upper().strip()
        if not (':' in e_time and (e_time.endswith('AM') or e_time.endswith('PM'))):
            print("Time must be HH:MM AM/PM format.")
            return

        organizer_id = ''
        if organizers:
            print("\nAvailable Organizers:")
            for o in organizers:
                print(f" - {o['id']} : {o['name']}")
            organizer_id = input("\nAssign Organizer ID (leave blank if none): ").strip()
            if organizer_id and not any(o['id'] == organizer_id for o in organizers):
                print("Organizer ID not found.")
                return

        events.append({
            'id': e_id,
            'name': e_name,
            'date': e_date,
            'time': e_time,
            'location': e_location,
            'organizer_id': organizer_id
        })

        self.store_data(self.events_path, events)
        print("Event added successfully!")

    def view_event(self):
        events = self.load_data(self.events_path)
        organizers = self.load_data(self.organizer_path)

        if not events:
            print("No events available.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<6}{'NAME':<20}{'DATE':<15}{'TIME':<10}{'LOCATION':<15}{'ORGANIZER':<15}")
        print("-" * 80)

        for e in events:
            org_name = "(Not Assigned)"
            if e.get('organizer_id'):
                org = next((o for o in organizers if o['id'] == e['organizer_id']), None)
                if org:
                    org_name = org['name']
            print(f"{e['id']:<6}{e['name']:<20}{e['date']:<15}{e['time']:<10}{e['location']:<15}{org_name:<15}")

        print("=" * 80)

    def delete_event(self):
        events = self.load_data(self.events_path)
        if not events:
            print("No Events available.")
            return

        event_id = input("Enter Event ID to delete: ").strip()
        new_events = [e for e in events if e['id'] != event_id]

        if len(new_events) == len(events):
            print("Event not found.")
        else:
            self.store_data(self.events_path, new_events)
            print("Event deleted successfully.")

    def add_organizer(self):
        organizers = self.load_data(self.organizer_path)
        print("\n" + "=" * 40)
        print("         ADD ORGANIZER")
        print("=" * 40)

        organizer_id = input("Enter Organizer Id: ").strip()
        name = input("Enter Organizer Name: ").strip()
        phone = input("Enter Organizer Phone (10 digits): ").strip()

        if not all([organizer_id, name, phone]):
            print("All fields are required.")
            return
        if not (phone.isdigit() and len(phone) == 10):
            print("Invalid phone number format.")
            return
        if any(o['id'] == organizer_id for o in organizers):
            print("Organizer ID already exists.")
            return

        organizers.append({'id': organizer_id, 'name': name, 'phone': phone, 'username': '', 'password': ''})
        self.store_data(self.organizer_path, organizers)
        print("Organizer added successfully.")

    def view_organizers(self):
        organizers = self.load_data(self.organizer_path)
        if not organizers:
            print("No organizers found.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<6}{'NAME':<20}{'PHONE':<15}{'USERNAME':<20}{'STATUS':<15}")
        print("-" * 80)
        for o in organizers:
            username = o.get('username', '(Not Set)')
            status = 'Password Set' if o.get('password') else 'Password Not Set'
            print(f"{o['id']:<6}{o['name']:<20}{o['phone']:<15}{username:<20}{status:<15}")
        print("=" * 80)

    def admin_menu(self):
        if not self.admin_login():
            return

        while True:
            print("\n" + "=" * 50)
            print("                 ADMIN MENU")
            print("=" * 50)
            print("""
            1. Add Event
            2. View Event
            3. Delete Event
            4. Add Organizer
            5. View Organizer
            6. Log Out
            """)
            ch = input("Enter your choice: ").strip()

            if ch == '1':
                self.add_event()
            elif ch == '2':
                self.view_event()
            elif ch == '3':
                self.delete_event()
            elif ch == '4':
                self.add_organizer()
            elif ch == '5':
                self.view_organizers()
            elif ch == '6':
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == '__main__':
    Admin().admin_menu()
