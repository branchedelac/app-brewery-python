from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL
import csv
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe Name", validators=[DataRequired()])
    location = URLField("Location", validators=[DataRequired(), URL()])
    open = StringField("Open", validators=[DataRequired()])
    close = StringField("Close", validators=[DataRequired()])
    coffee = SelectField("Coffee", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField("Wifi", choices=["✘", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power = SelectField("Power", choices=["✘", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField("Submit")

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    cafe_form = CafeForm()
    if cafe_form.validate_on_submit():
        with open('cafe-data.csv', "a", newline='', encoding='utf-8') as csv_file:
            new_row = ",".join([value for value in cafe_form.data.values()][:7])
            csv_file.write(f"\n{new_row}")
            return redirect("cafes")
    return render_template("add.html", form = cafe_form)



if __name__ == '__main__':
    app.run(debug=True)
