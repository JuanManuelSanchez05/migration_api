#%%
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Employee, Department, Job
from config import Config
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)  

db = SQLAlchemy(app)

#Contrataciones por puesto y departamento trimestrales en 2021
@app.route('/hires-by-job-department', methods=['GET'])
def hires_by_job_department():
    query = db.session.query(
        Employee.datetime, Department.department, Job.job
    ).join(Department, Employee.department_id == Department.id)\
     .join(Job, Employee.job_id == Job.id)\
     .filter(db.extract('year', Employee.datetime) == 2021).all()

    df = pd.DataFrame(query, columns=['datetime', 'department', 'job'])
    df['quarter'] = df['datetime'].dt.to_period('Q').astype(str)

    pivot_df = df.pivot_table(index=['department', 'job'], columns='quarter', aggfunc='size', fill_value=0)
    result = pivot_df.reset_index().sort_values(['department', 'job']).to_dict(orient='records')

    return jsonify(result)

#Departamentos con contrataciones por encima de la media
@app.route('/departments-above-average', methods=['GET'])
def departments_above_average():
    query = db.session.query(
        Employee.datetime, Department.department
    ).join(Department, Employee.department_id == Department.id)\
     .filter(db.extract('year', Employee.datetime) == 2021).all()

    df = pd.DataFrame(query, columns=['datetime', 'department'])

    hires_per_department = df.groupby('department').size().reset_index(name='hired')
    mean_hires = hires_per_department['hired'].mean()
    above_avg = hires_per_department[hires_per_department['hired'] > mean_hires]
    result = above_avg.sort_values(by='hired', ascending=False).to_dict(orient='records')

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)