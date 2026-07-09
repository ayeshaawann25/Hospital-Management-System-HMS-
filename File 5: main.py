# main.py
from services import HospitalService
from utils import display_table, get_valid_input, validate_contact, validate_date, format_date
from datetime import datetime

class HospitalManagementSystem:
    def __init__(self):
        self.service = HospitalService()
        self.current_user = None
    
    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                self.billing_menu()
            elif choice == '5':
                print("Thank you for using Hospital Management System!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def show_main_menu(self):
        print("\n" + "="*50)
        print("🏥 HOSPITAL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Billing")
        print("5. Exit")
        print("="*50)
    
    def patient_menu(self):
        while True:
            print("\n--- Patient Management ---")
            print("1. Register New Patient")
            print("2. View All Patients")
            print("3. Search Patient")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.search_patient()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
    
    def register_patient(self):
        print("\n--- Register New Patient ---")
        name = input("Full Name: ")
        age = input("Age: ")
        gender = input("Gender (M/F/Other): ")
        contact = get_valid_input("Phone Number: ", validate_contact, "Invalid phone number!")
        address = input("Address: ")
        medical_history = input("Medical History (comma separated, optional): ")
        medical_history_list = [h.strip() for h in medical_history.split(',')] if medical_history else []
        
        patient = self.service.register_patient(name, age, gender, contact, address, medical_history_list)
        print(f"✅ Patient registered successfully! ID: {patient.id}")
    
    def view_patients(self):
        patients = self.service.get_all_patients()
        if not patients:
            print("No patients found.")
            return
        
        headers = ['ID', 'Name', 'Age', 'Gender', 'Contact', 'Address']
        rows = [[p.id, p.name, p.age, p.gender, p.contact, p.address[:20] + '...' if len(p.address) > 20 else p.address] 
                for p in patients]
        display_table(headers, rows)
    
    def search_patient(self):
        patient_id = input("Enter Patient ID: ")
        patient = self.service.get_patient(patient_id)
        if patient:
            print("\n--- Patient Details ---")
            print(f"ID: {patient.id}")
            print(f"Name: {patient.name}")
            print(f"Age: {patient.age}")
            print(f"Gender: {patient.gender}")
            print(f"Contact: {patient.contact}")
            print(f"Address: {patient.address}")
            print(f"Registered: {format_date(patient.registered_date)}")
            print(f"Medical History: {', '.join(patient.medical_history) if patient.medical_history else 'None'}")
        else:
            print("❌ Patient not found!")
    
    def doctor_menu(self):
        while True:
            print("\n--- Doctor Management ---")
            print("1. Add New Doctor")
            print("2. View All Doctors")
            print("3. View Available Doctors")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_doctors()
            elif choice == '3':
                self.view_available_doctors()
            elif choice == '4':
                break
            else:
                print("Invalid choice!")
    
    def add_doctor(self):
        print("\n--- Add New Doctor ---")
        name = input("Full Name: ")
        age = input("Age: ")
        gender = input("Gender (M/F/Other): ")
        contact = get_valid_input("Phone Number: ", validate_contact, "Invalid phone number!")
        specialization = input("Specialization: ")
        experience = input("Years of Experience: ")
        
        doctor = self.service.add_doctor(name, age, gender, contact, specialization, experience)
        print(f"✅ Doctor added successfully! ID: {doctor.id}")
    
    def view_doctors(self):
        doctors = self.service.get_all_doctors()
        if not doctors:
            print("No doctors found.")
            return
        
        headers = ['ID', 'Name', 'Specialization', 'Experience', 'Available']
        rows = [[d.id, d.name, d.specialization, d.experience, '✅' if d.availability else '❌'] 
                for d in doctors]
        display_table(headers, rows)
    
    def view_available_doctors(self):
        doctors = self.service.get_available_doctors()
        if not doctors:
            print("No doctors available.")
            return
        
        headers = ['ID', 'Name', 'Specialization', 'Experience']
        rows = [[d.id, d.name, d.specialization, d.experience] for d in doctors]
        display_table(headers, rows)
    
    def appointment_menu(self):
        while True:
            print("\n--- Appointment Management ---")
            print("1. Book Appointment")
            print("2. View All Appointments")
            print("3. View Patient Appointments")
            print("4. Cancel Appointment")
            print("5. Complete Appointment")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.book_appointment()
            elif choice == '2':
                self.view_appointments()
            elif choice == '3':
                self.view_patient_appointments()
            elif choice == '4':
                self.cancel_appointment()
            elif choice == '5':
                self.complete_appointment()
            elif choice == '6':
                break
            else:
                print("Invalid choice!")
    
    def book_appointment(self):
        print("\n--- Book Appointment ---")
        
        # Show patients
        patients = self.service.get_all_patients()
        if not patients:
            print("❌ No patients registered. Please register a patient first.")
            return
        
        print("\nPatients:")
        for p in patients:
            print(f"  {p.id}: {p.name}")
        patient_id = input("Enter Patient ID: ")
        if not self.service.get_patient(patient_id):
            print("❌ Patient not found!")
            return
        
        # Show available doctors
        available_doctors = self.service.get_available_doctors()
        if not available_doctors:
            print("❌ No doctors available!")
            return
        
        print("\nAvailable Doctors:")
        for d in available_doctors:
            print(f"  {d.id}: {d.name} - {d.specialization}")
        doctor_id = input("Enter Doctor ID: ")
        if not self.service.get_doctor(doctor_id):
            print("❌ Doctor not found!")
            return
        
        date_time = input("Enter Date & Time (YYYY-MM-DD HH:MM): ")
        if not validate_date(date_time):
            print("❌ Invalid date format!")
            return
        
        reason = input("Reason for appointment: ")
        
        appointment = self.service.book_appointment(patient_id, doctor_id, date_time, reason)
        if appointment:
            print(f"✅ Appointment booked! ID: {appointment.id}")
        else:
            print("❌ Failed to book appointment.")
    
    def view_appointments(self):
        appointments = self.service.appointments
        if not appointments:
            print("No appointments found.")
            return
        
        headers = ['ID', 'Patient', 'Doctor', 'Date/Time', 'Status']
        rows = []
        for a in appointments:
            patient = self.service.get_patient(a.patient_id)
            doctor = self.service.get_doctor(a.doctor_id)
            patient_name = patient.name if patient else 'Unknown'
            doctor_name = doctor.name if doctor else 'Unknown'
            rows.append([a.id, patient_name, doctor_name, format_date(a.date_time), a.status])
        
        display_table(headers, rows)
    
    def view_patient_appointments(self):
        patient_id = input("Enter Patient ID: ")
        appointments = self.service.get_patient_appointments(patient_id)
        if not appointments:
            print("No appointments found for this patient.")
            return
        
        headers = ['ID', 'Doctor', 'Date/Time', 'Status']
        rows = []
        for a in appointments:
            doctor = self.service.get_doctor(a.doctor_id)
            doctor_name = doctor.name if doctor else 'Unknown'
            rows.append([a.id, doctor_name, format_date(a.date_time), a.status])
        
        display_table(headers, rows)
    
    def cancel_appointment(self):
        appointment_id = input("Enter Appointment ID to cancel: ")
        if self.service.cancel_appointment(appointment_id):
            print("✅ Appointment cancelled.")
        else:
            print("❌ Appointment not found!")
    
    def complete_appointment(self):
        appointment_id = input("Enter Appointment ID to mark as complete: ")
        if self.service.complete_appointment(appointment_id):
            print("✅ Appointment marked as completed.")
        else:
            print("❌ Appointment not found!")
    
    def billing_menu(self):
        print("\n--- Billing ---")
        patient_id = input("Enter Patient ID: ")
        patient = self.service.get_patient(patient_id)
        if not patient:
            print("❌ Patient not found!")
            return
        
        amount = input("Enter Bill Amount: ")
        description = input("Enter Description: ")
        
        bill = self.service.generate_bill(patient_id, amount, description)
        print("\n" + "="*50)
        print("🧾 BILL DETAILS")
        print("="*50)
        print(f"Patient: {patient.name}")
        print(f"Date: {format_date(bill['date'])}")
        print(f"Amount: ${amount}")
        print(f"Description: {description}")
        print(f"Status: {bill['status']}")
        print("="*50)
        print("Thank you!")

if __name__ == "__main__":
    system = HospitalManagementSystem()
    system.run()
