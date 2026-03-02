# import dependencies
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
# load data
data_set = pd.read_excel("student_data.xlsx")
# separate features and target
cgpa = data_set["cgpa"].values
data = data_set.drop(columns = "cgpa").values
# normalize data between 0-1
scaler = MinMaxScaler()
data_norm = scaler.fit_transform(data)
# train multivalue regression
model = LinearRegression()
model.fit(data_norm, cgpa)
# get student input
def student_input():
    return [
        float(input("Study Hours per week(0-25): ")),
        float(input("Attendance(0-100): ")),
        float(input("Academic Consistency(0-10): ")),
        float(input("Self Study(0-10): ")),
        float(input("Sleep Hours(0-10): ")),
        float(input("Study Stress(0-10): ")),
        float(input("Time Management(0-10): ")),
        float(input("Class Participation(0-10): ")),
        float(input("Screen Time(0-10): ")),
        float(input("Motivation Level(0-10): "))
    ]
student = student_input()
# normalize student data using training
student_norm = scaler.transform([student])
# predicted cgpa
predicted_cgpa = model.predict(student_norm)[0]
predicted_cgpa = min(max(predicted_cgpa, 0), 4)
print(f"predicted cgpa: {predicted_cgpa:.2f}")

