# models.py
from datetime import datetime
import uuid

class Person:
    def __init__(self, name, age, gender, contact):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'contact': self.contact
        }
    
    @classmethod
    def from_dict(cls, data):
        person = cls(data['name'], data['age'], data['gender'], data['contact'])
        person.id = data['id']
        return person

class Patient(Person):
    def __init__(self, name, age, gender, contact, address, medical_history=None):
        super().__init__(name, age, gender, contact)
        self.address = address
        self.medical_history = medical_history or []
        self.registered_date = datetime.now().isoformat()
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'address': self.address,
            'medical_history': self.medical_history,
            'registered_date': self.registered_date
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        patient = cls(data['name'], data['age'], data['gender'], 
                     data['contact'], data['address'], data['medical_history'])
        patient.id = data['id']
        patient.registered_date = data['registered_date']
        return patient

class Doctor(Person):
    def __init__(self, name, age, gender, contact, specialization, experience):
        super().__init__(name, age, gender, contact)
        self.specialization = specialization
        self.experience = experience
        self.availability = True
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'specialization': self.specialization,
            'experience': self.experience,
            'availability': self.availability
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        doctor = cls(data['name'], data['age'], data['gender'], 
                    data['contact'], data['specialization'], data['experience'])
        doctor.id = data['id']
        doctor.availability = data['availability']
        return doctor

class Appointment:
    def __init__(self, patient_id, doctor_id, date_time, reason):
        self.id = str(uuid.uuid4())[:8]
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.reason = reason
        self.status = 'Scheduled'  # Scheduled, Completed, Cancelled
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date_time': self.date_time,
            'reason': self.reason,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        appointment = cls(data['patient_id'], data['doctor_id'], 
                         data['date_time'], data['reason'])
        appointment.id = data['id']
        appointment.status = data['status']
        return appointment
