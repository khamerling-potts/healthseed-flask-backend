import json

# Remote library imports
from flask import request, session, make_response
from flask_restful import Resource
import phonenumbers

# Local imports
from config import app, db, api

# Model imports
from models.user import User
from models.condition import Condition
from models.provider import Provider
from models.instruction import Instruction
from models.medication import Medication
from models.routine import Routine
from models.appointment import Appointment


# ONLY used to clear the database in development
class ResetDB(Resource):
    def get(self):
        # Instruction.query.delete()
        # Medication.query.delete()
        db.session.commit()
        return {"message": "200 - Successfully cleared instructions"}, 200

@app.before_request
def check_logged_in():
    if request.endpoint not in ['login', 'users', 'reset']:
        print('checking logged in')
        if not session.get('user_id'):
            return {'error': 'Unauthorized'}, 401
        
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict(), 200


class Login(Resource):
    def post(self):
        data = request.get_json()
        [username, password] = [data.get('username'), data.get('password')]
        user = User.query.filter_by(username=username.lower()).first()
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': '401 - Unauthorized'}, 401
    
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return users, 200
    
    def post(self):
        data = request.get_json()
        [username, password, name, birthday] = [data.get('username'), data.get('password'), data.get('name'), data.get('birthday')]
        try:
            new_user = User(username=username, name=name, birthday=birthday)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(), 200
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        

class Conditions(Resource):
    def get(self):
        user_id = session.get('user_id')
        conditions = [condition.to_dict() for condition in Condition.query.filter_by(user_id=user_id)]
        return conditions, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        description = data.get('description')
        try:
            new_condition = Condition(description=description, user_id=user_id)
            print(new_condition)
            db.session.add(new_condition)
            db.session.commit()
            print('here')
            return new_condition.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        

class ConditionByID(Resource):
    def patch(self, id):
        data = request.get_json()
        try:
            condition = Condition.query.filter_by(id=id).first()
            for attr in data:
                setattr(condition, attr, data.get(attr))
            db.session.add(condition)
            db.session.commit()
            return condition.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        
    def delete(self, id):
        try:
            condition = Condition.query.filter_by(id=id).first()
            db.session.delete(condition)
            db.session.commit()
            return {"message": "condition successfully deleted"}, 204
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404


        
class Providers(Resource):
    def get(self):
        user_id = session.get('user_id')
        providers = [provider.to_dict() for provider in Provider.query.filter_by(user_id=user_id)]
        return providers, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        [name, phone, address] = [data.get('name'), data.get('phone'), data.get('address')]
        try:
            new_provider = Provider(name=name, phone=phone, address=address, user_id=user_id)
            print(new_provider.phone)
            db.session.add(new_provider)
            db.session.commit()
            return new_provider.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        

class ProviderByID(Resource):
    def patch(self, id):
        data = request.get_json()
        print(data)
        try:
            provider = Provider.query.filter_by(id=id).first()
            for attr in data:
                setattr(provider, attr, data.get(attr))
            db.session.add(provider)
            db.session.commit()
            return provider.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        
    def delete(self, id):
        try:
            provider = Provider.query.filter_by(id=id).first()
            db.session.delete(provider)
            db.session.commit()
            return {"message": "provider successfully deleted"}, 204
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404

class Medications(Resource):
    def get(self):
        user_id = session.get('user_id')
        medications = [medication.to_dict() for medication in Medication.query.filter_by(user_id=user_id)]
        return medications, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        [
            name, 
            time1, 
            dose1, 
            time2, 
            dose2, 
            time3, 
            dose3
        ] = [
                data.get('name'), 
                data.get('time1'), 
                data.get('dose1'), 
                data.get('time2'), 
                data.get('dose2'), 
                data.get('time3'), 
                data.get('dose3')
            ]
        try:
            new_medication = Medication(name=name, user_id=user_id)
            db.session.add(new_medication)
            db.session.commit()

            # Adding associated instruction objects if user specified them during medication creation
            if time1!='' and dose1!='':
                instruction = Instruction(time=time1, dose=dose1, medication_id = new_medication.id, user_id=user_id)
                db.session.add(instruction)
            if time2!='' and dose2!='':
                instruction = Instruction(time=time2, dose=dose2, medication_id = new_medication.id, user_id=user_id)
                db.session.add(instruction)
            if time3!='' and dose3!='':
                instruction = Instruction(time=time3, dose=dose3, medication_id = new_medication.id, user_id=user_id)
                db.session.add(instruction)
            db.session.commit()
            return new_medication.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        
class MedicationByID(Resource):
    def patch(self, id):
        data = request.get_json()
        print(data)
        try:
            medication = Medication.query.filter_by(id=id).first()
            setattr(medication, "name", data.get('name'))
            db.session.add(medication)
            db.session.commit()
            return medication.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        
    def delete(self, id):
        try:
            medication = Medication.query.filter_by(id=id).first()
            db.session.delete(medication)
            db.session.commit()
            return {"message": "medication successfully deleted"}, 204
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404
        


class Instructions(Resource):
    def get(self):
        user_id = session.get('user_id')
        instructions = [instruction.to_dict() for instruction in Instruction.query.filter_by(user_id=user_id)]
        return instructions, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        try:
            new_instruction = Instruction(time=data.get('time'), dose=data.get('dose'), medication_id=data.get('medication_id'), user_id=user_id)
            db.session.add(new_instruction)
            db.session.commit()
            medication = Medication.query.filter_by(id=new_instruction.medication_id).first()
            return medication.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable entity'}, 422

    
class InstructionByID(Resource):

    # returns the updated medication associated with this instruction
    def patch(self, id):
        # user_id = session.get('user_id')
        data = request.get_json()
        try:
            instruction = Instruction.query.filter_by(id=id).first()
            for attr in data:
                if attr != 'medication_id':
                    setattr(instruction, attr, data.get(attr))
            db.session.add(instruction)
            db.session.commit()

            medication = Medication.query.filter_by(id=instruction.medication_id).first()
            return medication.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        
    def delete(self, id):
        try:
            instruction = Instruction.query.filter_by(id=id).first()
            medication_id = instruction.medication_id
            db.session.delete(instruction)
            db.session.commit()
            medication = Medication.query.filter_by(id=medication_id).first()

            return medication.to_dict(), 200
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404
        


class Routines(Resource):
    def get(self):
        user_id = session.get('user_id')
        routines = [routine.to_dict() for routine in Routine.query.filter_by(user_id=user_id)]
        return routines, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        [title, notes, instruction_ids, times] = [data.get('title'), data.get('notes'), data.get('instruction_ids'), data.get('times')]
        try:
            new_routine = Routine(title=title, notes=notes, times=times, user_id=user_id)
            db.session.add(new_routine)
            db.session.commit()

            # assign this routine to every instruction that the user selects for this routine
            for instruction_id in instruction_ids:
                instruction = Instruction.query.filter_by(id=instruction_id).first()
                instruction.routine_id = new_routine.id
                db.session.add(instruction)
                db.session.commit()
           
            return new_routine.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        
class RoutineByID(Resource):
    def patch(self, id):
        data = request.get_json()
        try:
            routine = Routine.query.filter_by(id=id).first()
            # First, remove routine_ids from all previously associated instructions
            for instruction in routine.instructions:
                instruction.routine_id = None
                db.session.add(instruction)

            # Update all attributes besides instructions
            for attr in data:
                if attr != 'instruction_ids':
                    setattr(routine, attr, data.get(attr))

            # Reassign this routine's id to current instructions
            instruction_ids = data.get('instruction_ids')
            for instruction_id in instruction_ids:
                instruction = Instruction.query.filter_by(id=instruction_id).first()
                instruction.routine_id = routine.id
                db.session.add(instruction)
                db.session.commit()

            db.session.add(routine)
            db.session.commit()
            return routine.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        
    def delete(self, id):
        try:
            routine = Routine.query.filter_by(id=id).first()

            # manually delete routine_ids from instructions bc I don't want the whole instruction deleted
            for instruction in routine.instructions:
                instruction.routine_id = None
                db.session.add(instruction)

            db.session.delete(routine)
            db.session.commit()

            # returning updated instructions to make state update easy on the front end
            instructions = [instruction.to_dict() for instruction in Instruction.query.all()] 
            return instructions, 200
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404
        

class Appointments(Resource):
    def get(self):
        user_id = session.get('user_id')
        appointments = [appointment.to_dict() for appointment in Appointment.query.filter_by(user_id=user_id)]
        return appointments, 200
    
    def post(self):
        user_id = session.get('user_id')
        data = request.get_json()
        [category, location, datetime, user_id] = [data.get('category'), data.get('location'), data.get('datetime'), data.get('user_id')]
        try:
            new_appointment = Appointment(category=category, location=location, datetime=datetime, user_id=user_id)
            if provider_id := data.get('provider_id'):
                setattr(new_appointment, 'provider_id', provider_id)
            print(new_appointment)
            db.session.add(new_appointment)
            db.session.commit()
            return new_appointment.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': "422 - Unprocessable Entity"}, 422
        

class AppointmentByID(Resource):
    def patch(self, id):
        data = request.get_json()
        try:
            condition = Condition.query.filter_by(id=id).first()
            for attr in data:
                setattr(condition, attr, data.get(attr))
            db.session.add(condition)
            db.session.commit()
            return condition.to_dict(), 201
        except Exception as exc:
            print(exc)
            return {'error': '422 - Unprocessable Entity'}, 422
        
    def delete(self, id):
        try:
            condition = Condition.query.filter_by(id=id).first()
            db.session.delete(condition)
            db.session.commit()
            return {"message": "condition successfully deleted"}, 204
        except Exception as exc:
            print(exc)
            return {'error': '404 - Not found'}, 404



api.add_resource(ResetDB, "/reset", endpoint="reset")
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Users, "/users", endpoint="users")
api.add_resource(Conditions, '/conditions', endpoint='conditions')
api.add_resource(ConditionByID, '/conditions/<int:id>', endpoint='conditions/<int:id>')
api.add_resource(Providers, '/providers', endpoint='providers')
api.add_resource(ProviderByID, '/providers/<int:id>', endpoint="providers/<int:id>")
api.add_resource(Medications, '/medications', endpoint='medications')
api.add_resource(MedicationByID, '/medications/<int:id>', endpoint="medications/<int:id>")
api.add_resource(Instructions, '/instructions', endpoint='instructions')
api.add_resource(InstructionByID, '/instructions/<int:id>', endpoint="instructions/<int:id>")
api.add_resource(Routines, '/routines', endpoint='routines')
api.add_resource(RoutineByID, '/routines/<int:id>', endpoint="routines/<int:id>")
api.add_resource(Appointments, '/appointments', endpoint='appointments')
api.add_resource(AppointmentByID, '/appointments/<int:id>', endpoint='appointments/<int:id>')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
