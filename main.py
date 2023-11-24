from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import math
app = Flask(__name__)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
def return_tdee(age,gender,height,weight,activity):
    activity_nums={'sedentary':1.2,'light':1.375,'moderate':1.55,'very_active':1.725,'extra_active':1.9}
    if gender=='male':
        bmr=math.ceil(66+float(weight)*13.7+5*float(height)-6.8*float(age))
    else:
        bmr=math.ceil(655+float(weight)*9.6+1.8*float(height)-4.7*float(age))
    tdee=math.ceil(bmr*activity_nums[activity])
    print(bmr)
    print(tdee)
    bmi=round(weight/((height/100)**2),2)
    if bmi < 18.5:
        bmi_range=bmi
        bmi_type="Underweight"
        color="yellow"
    elif bmi > 18.5 and bmi < 24.9:
        bmi_type ="Healthy"
        color="green"
    elif bmi > 25 and bmi < 29.9:
        bmi_type= " Overweight"
        color="red"
    else:
        bmi_type= " Obesity "
        color="darkred"
    result={"BMI":bmi,"BMI Type":bmi_type,'color':color,"TDEE":tdee,"Mid Weight Loss":int(float(tdee*0.9)) , 'Weight Loss' : int(float(tdee*0.79)),
            "Mid Weight Gain":int(float(tdee*1.1)),"Weight Gain":int(float(tdee*1.21)),"Fast Weight Gain":int(float(tdee*1.41)) }
    print(result)
    return result

@app.route('/data',methods=['POST','GET'])
def calculate():
    if request.method=='POST':
        age=request.form['age']
        gender=request.form.getlist('fav_language')[0]
        height=float(request.form['height'])
        weight=float(request.form['weight'])
        activity=request.form['activity']
    result=return_tdee(age,gender,height,weight,activity)
    return render_template('report.html',result=result)
if __name__ == "__main__":
    app.run(debug=True)
