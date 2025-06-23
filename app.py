# app.py
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_me'

# In-memory storage
jobs = [
    {'id': 1, 'title': 'Java Developer', 'description': 'Build enterprise Java apps.', 'vacancies': 3},
    {'id': 2, 'title': 'C++ Developer', 'description': 'Develop high-performance modules.', 'vacancies': 2}
]
candidates = []

class ApplyForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit Application')

@app.route('/')
def home():
    return render_template('index.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['GET','POST'])
def apply(job_id):
    job = next((j for j in jobs if j['id'] == job_id), None)
    form = ApplyForm()
    if form.validate_on_submit() and job:
        candidates.append({'name': form.name.data, 'email': form.email.data, 'job_id': job_id})
        return redirect(url_for('home'))
    return render_template('apply.html', job=job, form=form)

@app.route('/admin')
def admin():
    total_jobs = len(jobs)
    total_cands = len(candidates)
    # attach job title
    for c in candidates:
        c['job'] = next(j for j in jobs if j['id']==c['job_id'])
    return render_template('admin.html', total_jobs=total_jobs, total_cands=total_cands, cands=candidates)

if __name__ == '__main__':
    app.run(debug=True)
