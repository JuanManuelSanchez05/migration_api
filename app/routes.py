from flask import request, jsonify
from app import app, db
from app.models import Department, Job, Employee
import pandas as pd
from datetime import datetime
import math

#Dejamos una fecha por defecto para valore snulos
FECHA_DEFECTO = datetime(1900, 1, 1)

def get_int_value(val, default=-1):
    """Convierte a entero o retorna default si es nulo o no convertible."""
    try:
        if pd.isnull(val) or str(val).strip() == "":
            return default
        return int(val)
    except Exception:
        return default

def get_str_value(val, default="sin_nombre"):
    """Retorna el valor de cadena o default si es nulo o vacio."""
    if pd.isnull(val) or str(val).strip() == "":
        return default
    return str(val).strip()

def get_date_value(date_str, default=FECHA_DEFECTO):
    """Convierte la cadena de fecha al formato datetime o retorna default."""
    try:
        if pd.isnull(date_str) or str(date_str).strip() == "":
            return default
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except Exception:
        return default

@app.route('/')
def home():
    return jsonify({"message": "API funcionando correctamente"}), 200


@app.route('/upload/<string:file_type>', methods=['POST'])
def upload_csv(file_type):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = pd.read_csv(file, header=None)
    except Exception as e:
        return jsonify({"error": f"Error al leer el CSV: {str(e)}"}), 400

    if file_type == 'hired_employees':
        #0: id, 1: nombre, 2: fecha, 3: department_id, 4: job_id
        for index, row in df.iterrows():
            try:
                #Agregamos valores por defecto si los campos estan vacios
                emp_id = get_int_value(row[0], default=-1)
                name = get_str_value(row[1], default="sin_nombre")
                emp_date = get_date_value(row[2], default=FECHA_DEFECTO)
                dept_id = get_int_value(row[3], default=-1)
                job_id = get_int_value(row[4], default=-1)

                #Imprimimos mensaje advertencia
                if emp_id == -1:
                    print(f"Fila {index}: id vacío. Se asigna -1.")
                if name == "sin_nombre":
                    print(f"Fila {index}: nombre vacío. Se asigna 'sin_nombre'.")
                if emp_date == FECHA_DEFECTO:
                    print(f"Fila {index}: fecha vacía o inválida. Se asigna fecha por defecto.")
                if dept_id == -1:
                    print(f"Fila {index}: id de departamento vacío. Se asigna -1.")
                if job_id == -1:
                    print(f"Fila {index}: id de trabajo vacío. Se asigna -1.")

                #Verificar que existan el departamento y el puesto de trabajo
                department = Department.query.get(dept_id)
                job = Job.query.get(job_id)
                if not department:
                    print(f"Fila {index}: Departamento con id {dept_id} no encontrado. Se asigna 'sin_departamento'.")
                    
                    department = Department(id=dept_id, department="sin_departamento")
                    db.session.add(department)
                if not job:
                    print(f"Fila {index}: Job con id {job_id} no encontrado. Se asigna 'sin_trabajo'.")
                    
                    job = Job(id=job_id, job="sin_trabajo")
                    db.session.add(job)

                #Buscamos duplicados. Si ya existe un empleado con ese id, se omite.
                if Employee.query.get(emp_id):
                    print(f"Empleado con id {emp_id} ya existe. Fila {index}")
                    continue

                employee = Employee(
                    id=emp_id,
                    name=name,
                    datetime=emp_date,
                    department_id=dept_id,
                    job_id=job_id
                )
                db.session.add(employee)
            except Exception as e:
                print(f"Error procesando empleado en la fila {index}: {e}")

    elif file_type == 'departments':
        
        for index, row in df.iterrows():
            try:
                dept_id = get_int_value(row[0], default=-1)
                dept_name = get_str_value(row[1], default="sin_departamento")
                if not Department.query.get(dept_id):
                    department = Department(id=dept_id, department=dept_name)
                    db.session.add(department)
            except Exception as e:
                print(f"Error procesando departamento en la fila {index}: {e}")

    elif file_type == 'jobs':
        
        for index, row in df.iterrows():
            try:
                job_id = get_int_value(row[0], default=-1)
                job_name = get_str_value(row[1], default="sin_trabajo")
                if not Job.query.get(job_id):
                    job = Job(id=job_id, job=job_name)
                    db.session.add(job)
            except Exception as e:
                print(f"Error procesando job en la fila {index}: {e}")
    else:
        return jsonify({"error": "Tipo de archivo no reconocido. Use 'departments', 'jobs' o 'hired_employees'"}), 400

    try:
        db.session.commit()
    except Exception as commit_error:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar en la base de datos: {commit_error}"}), 500

    return jsonify({"message": "File uploaded and processed successfully"}), 200


