import json
import getpass


class Organizer:
    def __init__(self):
        self.events_path = r'D:\FBS Work\Python\Project\data\events.json'
        self.participant_path = r'D:\FBS Work\Python\Project\data\participants.json'
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

    def organizer_login(self):
        organizers = self.load_data(self.organizer_path)

        print("\n" + "=" * 40)
        print("           ORGANIZER LOGIN")
        print("=" * 40)

        for attempt in range(3):
            organizer_id = input("Enter Organizer ID: ").strip()
            organizer_name = input("Enter Organizer Name: ").strip()

            organizer = next(
                (o for o in organizers if o['id'] == organizer_id and o['name'] == organizer_name),
                None
            )

            if organizer:
                break
            else:
                print(f"Invalid credentials. Attempts left: {2 - attempt}")

        if not organizer:
            print("Failed to login. Returning to main menu.")
            return

        if not organizer.get('username') or not organizer.get('password'):
            print("\nFirst time login detected.")
            while True:
                username = input("Set Username: ").strip()
                if not username:
                    print("Username cannot be empty.")
                elif any(o['username'] == username for o in organizers if o['id'] != organizer_id):
                    print("Username already exists.")
                else:
                    organizer['username'] = username
                    break

            while True:
                password = input("Set Password: ").strip()
                if not password:
                    print("Password cannot be empty.")
                else:
                    organizer['password'] = password
                    break

            self.store_data(self.organizer_path, organizers)
            print("Username & Password created successfully! Please login now.")

        for attempt in range(3):
            username = input("Enter Username: ").strip()
            password = getpass.getpass("Enter Password: ").strip()

            if username == organizer['username'] and password == organizer['password']:
                print(f"\nWelcome, {organizer['name']}!")
                self.organizer_menu(organizer['id'])
                return
            else:
                print(f"Incorrect credentials. Attempts left: {2 - attempt}")

        print("Too many failed attempts. Returning to main menu.")

    def load_my_events(self, organizer_id):
        events = self.load_data(self.events_path)
        return [e for e in events if e.get('organizer_id') == organizer_id]

    def add_participant(self, organizer_id):
        events = self.load_my_events(organizer_id)
        participants = self.load_data(self.participant_path)

        if not events:
            print("No assigned events.")
            return

        print("\nYour Assigned Events:")
        for e in events:
            print(f" - {e['id']} : {e['name']}")

        event_id = input("Enter Event ID to add participant: ").strip()
        event = next((e for e in events if e['id'] == event_id), None)

        if not event:
            print("Event not found.")
            return

        p_id = input("Enter Participant ID: ").strip()
        p_name = input("Enter Participant Name: ").strip()

        if not p_id or not p_name:
            print("All fields are required.")
            return

        if any(p['id'] == p_id and p['event_id'] == event_id for p in participants):
            print("Participant already exists for this event.")
            return

        participants.append({
            'id': p_id,
            'name': p_name,
            'event_id': event_id,
            'event_name': event['name']
        })

        self.store_data(self.participant_path, participants)
        print("Participant added successfully.")

    def view_participants(self, organizer_id):
        events = self.load_my_events(organizer_id)
        participants = self.load_data(self.participant_path)

        my_event_ids = [e['id'] for e in events]
        my_participants = [p for p in participants if p['event_id'] in my_event_ids]

        if not my_participants:
            print("No participants found.")
            return

        print("\n" + "=" * 60)
        print(f"{'ID':<10}{'NAME':<20}{'EVENT NAME':<20}")
        print("-" * 60)
        for p in my_participants:
            print(f"{p['id']:<10}{p['name']:<20}{p['event_name']:<20}")
        print("=" * 60)

    def update_event_details(self, organizer_id):
        events = self.load_my_events(organizer_id)
        if not events:
            print("No events found.")
            return

        event_id = input("Enter Event ID to update: ").strip()
        event = next((e for e in events if e['id'] == event_id), None)

        if not event:
            print("Event not found.")
            return

        print("\nLeave blank to skip updating a field.")
        new_name = input("New Event Name: ").strip()
        new_date = input("New Date (YYYY-MM-DD): ").strip()
        new_time = input("New Time (HH:MM AM/PM): ").strip()
        new_location = input("New Location: ").strip()

        if new_name:
            event['name'] = new_name
        if new_date:
            event['date'] = new_date
        if new_time:
            event['time'] = new_time
        if new_location:
            event['location'] = new_location

        all_events = self.load_data(self.events_path)
        for i, e in enumerate(all_events):
            if e['id'] == event_id:
                all_events[i] = event
                break

        self.store_data(self.events_path, all_events)
        print("Event details updated successfully.")

    def organizer_menu(self, organizer_id):
        while True:
            print("\n" + "=" * 50)
            print("             ORGANIZER MENU")
            print("=" * 50)
            print("""
            1. Add Participant
            2. View Participants
            3. Update Event Details
            4. Log Out
            """)
            ch = input("Enter your choice: ").strip()

            if ch == '1':
                self.add_participant(organizer_id)
            elif ch == '2':
                self.view_participants(organizer_id)
            elif ch == '3':
                self.update_event_details(organizer_id)
            elif ch == '4':
                print("Logged out.")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    Organizer().organizer_login()
