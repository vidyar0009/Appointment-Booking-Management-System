import unittest
import datetime

from app import User, Appointment, AppointmentBookingSystem  # Replace 'your_module' with the actual module name where your classes are defined

class TestAppointmentBookingSystem(unittest.TestCase):

    def setUp(self):
        self.booking_system = AppointmentBookingSystem()
        self.assertTrue(self.booking_system.register_user("Alice", "alice@example.com"))
        self.assertFalse(self.booking_system.register_user("Alice", "another@example.com"))

    def test_register_user(self):
        self.assertTrue(self.booking_system.register_user("Bob", "bob@example.com"))
        self.assertFalse(self.booking_system.register_user("Bob", "another@example.com"))

    def test_display_available_slots(self):
        date = "2023-01-01"
        self.assertEqual(self.booking_system.display_available_slots(date), [])

    def test_book_appointment(self):
        date = "2023-01-01"
        time = "09:00"
        self.booking_system.add_available_slot(date, time)
        self.assertTrue(self.booking_system.book_appointment(date, time, "Alice"))
        self.assertFalse(self.booking_system.book_appointment(date, time, "Bob"))
        self.assertFalse(self.booking_system.book_appointment("2023-01-02", time, "Alice"))

    def test_send_confirmation_email(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        self.assertEqual(self.booking_system.send_confirmation_email("Alice"), "Confirmation email sent to Alice at alice@example.com")
        self.assertEqual(self.booking_system.send_confirmation_email("Bob"), "User not found.")

    def test_get_user_appointments(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.book_appointment("2023-01-01", "09:00", "Alice")
        appointments = self.booking_system.get_user_appointments("Alice")
        self.assertEqual(len(appointments), 1)

    def test_cancel_appointment(self):
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.book_appointment("2023-01-01", "09:00", "Alice")
        self.assertTrue(self.booking_system.cancel_appointment("2023-01-01", "09:00"))
        self.assertFalse(self.booking_system.cancel_appointment("2023-01-01", "09:00"))

    def test_add_available_slot(self):
        date = "2023-01-01"
        time = "09:00"
        self.booking_system.add_available_slot(date, time)
        self.assertTrue(self.booking_system.is_slot_available(date, time))

    def test_remove_available_slot(self):
        date = "2023-01-01"
        time = "09:00"
        self.booking_system.add_available_slot(date, time)
        self.booking_system.remove_available_slot(date, time)
        self.assertFalse(self.booking_system.is_slot_available(date, time))

    def test_is_slot_available(self):
        date = "2023-01-01"
        time = "09:00"
        self.booking_system.add_available_slot(date, time)
        self.assertTrue(self.booking_system.is_slot_available(date, time))
        self.assertFalse(self.booking_system.is_slot_available("2023-01-02", time))

    def test_get_available_dates(self):
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.add_available_slot("2023-01-02", "10:00")
        dates = self.booking_system.get_available_dates()
        self.assertIn("2023-01-01", dates)
        self.assertIn("2023-01-02", dates)

    def test_get_available_times(self):
        date = "2023-01-01"
        self.booking_system.add_available_slot(date, "09:00")
        self.booking_system.add_available_slot(date, "10:00")
        times = self.booking_system.get_available_times(date)
        self.assertIn("09:00", times)
        self.assertIn("10:00", times)

    def test_get_next_available_slot(self):
        date = "2023-01-01"
        self.booking_system.add_available_slot(date, "09:00")
        self.booking_system.add_available_slot(date, "10:00")
        next_slot = self.booking_system.get_next_available_slot(date)
        self.assertEqual(next_slot, "09:00")

    def test_get_all_appointments(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.book_appointment("2023-01-01", "09:00", "Alice")
        appointments = self.booking_system.get_all_appointments()
        self.assertEqual(len(appointments), 1)

    def test_get_upcoming_appointments(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        #print(self.booking_system.users)
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.add_available_slot("2023-01-02", "10:00")
        #print(self.booking_system.available_slots)
        self.booking_system.book_appointment("2023-01-01", "09:00", "Alice")
        self.booking_system.book_appointment("2023-01-02", "10:00", "Alice")
        appointments = self.booking_system.get_upcoming_appointments("Alice")
        #print(appointments)
        self.assertEqual(len(appointments), 0)

    def test_send_reminder_email(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        self.assertEqual(self.booking_system.send_reminder_email("Alice"), "Reminder email sent to Alice at alice@example.com")
        self.assertEqual(self.booking_system.send_reminder_email("Bob"), "User not found.")

    def test_reschedule_appointment(self):
        self.booking_system.register_user("Alice", "alice@example.com")
        self.booking_system.add_available_slot("2023-01-01", "09:00")
        self.booking_system.add_available_slot("2023-01-02", "10:00")
        self.booking_system.book_appointment("2023-01-01", "09:00", "Alice")
        self.assertTrue(self.booking_system.reschedule_appointment("2023-01-01", "09:00", "2023-01-02", "10:00", "Alice"))
        self.assertFalse(self.booking_system.reschedule_appointment("2023-01-01", "09:00", "2023-01-02", "10:00", "Bob"))

if __name__ == '__main__':
    unittest.main()
