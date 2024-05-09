import datetime

class User:
    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email

class Appointment:
    def __init__(self, date, time, user):
        self.date = date
        self.time = time
        self.user = user

class AppointmentBookingSystem:
    def __init__(self):
        self.available_slots = {}
        self.appointments = []
        self.users = {}

    def register_user(self, user_name, email):
        if user_name not in self.users:
            user = User(user_name, email)
            self.users[user_name] = user
            return True
        else:
            return False

    def display_available_slots(self, date):
        return self.available_slots.get(date, [])

    def book_appointment(self, date, time, user_name):
        if date in self.available_slots and time in self.available_slots[date]:
            if user_name in self.users:
                user = self.users[user_name]
                self.available_slots[date].remove(time)
                appointment = Appointment(date, time, user)
                self.appointments.append(appointment)
                return True
        return False

    def send_confirmation_email(self, user_name):
        if user_name in self.users:
            user = self.users[user_name]
            # Placeholder for sending confirmation email
            return f"Confirmation email sent to {user.user_name} at {user.email}"
        else:
            return "User not found."

    def get_user_appointments(self, user_name):
        if user_name in self.users:
            return [appointment for appointment in self.appointments if appointment.user.user_name == user_name]
        else:
            return []

    def cancel_appointment(self, date, time):
        appointment_to_cancel = None
        for appointment in self.appointments:
            if appointment.date == date and appointment.time == time:
                appointment_to_cancel = appointment
                break
        if appointment_to_cancel:
            self.appointments.remove(appointment_to_cancel)
            if date in self.available_slots:
                self.available_slots[date].append(time)
            else:
                self.available_slots[date] = [time]
            return True
        else:
            return False

    def add_available_slot(self, date, time):
        if date in self.available_slots:
            self.available_slots[date].append(time)
        else:
            self.available_slots[date] = [time]

    def remove_available_slot(self, date, time):
        if date in self.available_slots and time in self.available_slots[date]:
            self.available_slots[date].remove(time)
            if not self.available_slots[date]:
                del self.available_slots[date]

    def is_slot_available(self, date, time):
        return date in self.available_slots and time in self.available_slots[date]

    def get_available_dates(self):
        return list(self.available_slots.keys())

    def get_available_times(self, date):
        return self.available_slots.get(date, [])

    def get_next_available_slot(self, date):
        if date in self.available_slots:
            times = self.available_slots[date]
            if times:
                return times[0]
        return None

    def get_all_appointments(self):
        return self.appointments

    def get_upcoming_appointments(self, user_name):
        current_datetime = datetime.datetime.now()
        if user_name in self.users:
                    #print(datetime.datetime.strptime(appointment.date + " " + appointment.time, "%Y-%m-%d %H:%M"),">=", current_datetime)
            return [appointment for appointment in self.appointments if appointment.user.user_name == user_name and 
                    datetime.datetime.strptime(appointment.date + " " + appointment.time, "%Y-%m-%d %H:%M") >= current_datetime]
            
        else:
            return []

    def send_reminder_email(self, user_name):
        if user_name in self.users:
            user = self.users[user_name]
            # Placeholder for sending reminder email
            return f"Reminder email sent to {user.user_name} at {user.email}"
        else:
            return "User not found."

    def reschedule_appointment(self, old_date, old_time, new_date, user_name, new_time):
        if self.cancel_appointment(old_date, old_time):
            return self.book_appointment(new_date, new_time, user_name)
        return False
