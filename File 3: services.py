# services.py
from models import Patient, Doctor, Appointment
from storage import Storage
from datetime import datetime

class HospitalService:
    def __init__(self):
        self.storage = Storage()
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.load_data()
    
    def load_data(self):
        # Load patients
        patient_data = self.storage.load('patients')
        self.patients = [Patient.from_dict(p) for p in patient_data]
        
        # Load doctors
        doctor_data = self.storage.load('doctors')
        self.doctors = [Doctor.from_dict(d) for d in doctor_data]
        
        # Load appointments
        appointment_data = self.storage.load('appointments')
        self.appointments = [Appointment.from_dict(a) for a in appointment_data]
    
    def save_data(self):
        self.storage.save_all('patients', [p.to_dict() for p in self.patients])
        self.storage.save_all('doctors', [d.to_dict() for d in self.doctors])
        self.storage.save_all('appointments', [a.to_dict() for a in self.appointments])
    
    # Patient Management
    def register_patient(self, name, age, gender, contact, address, medical_history=None):
        patient = Patient(name, age, gender, contact, address, medical_history)
        self.patients.append(patient)
        self.save_data()
        return patient
    
    def get_all_patients(self):
        return self.patients
    
    def get_patient(self, patient_id):
        for patient in self.patients:
            if patient.id == patient_id:
                return patient
        return None
    
    # Doctor Management
    def add_doctor(self, name, age, gender, contact, specialization, experience):
        doctor = Doctor(name, age, gender, contact, specialization, experience)
        self.doctors.append(doctor)
        self.save_data()
        return doctor
    
    def get_all_doctors(self):
        return self.doctors
    
    def get_doctor(self, doctor_id):
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                return doctor
        return None
    
    def get_available_doctors(self):
        return [d for d in self.doctors if d.availability]
    
    # Appointment Management
    def book_appointment(self, patient_id, doctor_id, date_time, reason):
        # Check if doctor is available
        doctor = self.get_doctor(doctor_id)
        if not doctor or not doctor.availability:
            return None
        
        appointment = Appointment(patient_id, doctor_id, date_time, reason)
        self.appointments.append(appointment)
        self.save_data()
        return appointment
    
    def cancel_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.status = 'Cancelled'
                self.save_data()
                return True
        return False
    
    def complete_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.status = 'Completed'
                self.save_data()
                return True
        return False
    
    def get_patient_appointments(self, patient_id):
        return [a for a in self.appointments if a.patient_id == patient_id]
    
    def get_doctor_appointments(self, doctor_id):
        return [a for a in self.appointments if a.doctor_id == doctor_id]
    
    # Billing (Simple)
    def generate_bill(self, patient_id, amount, description):
        # Simple bill generation - returns formatted bill string
        bill = {
            'patient_id': patient_id,
            'date': datetime.now().isoformat(),
            'amount': amount,
            'description': description,
            'status': 'Pending'
        }
        # In real system, save to bills.json
        return bill
