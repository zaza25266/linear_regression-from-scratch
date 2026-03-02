import statistics as st
import pandas as pd

# load data
data_set = pd.read_excel("student_data.xlsx")
cgpa = data_set["cgpa"].tolist()
data = data_set.drop(columns="cgpa").values.tolist()

def normalize(column):
    min_val = min(column)
    max_val = max(column)
    return [min(max((v - min_val) / (max_val - min_val), 0), 1) for v in column]

def correlation_weight(norm_data, norm_cgpa):
    weights = []
    for parameter in norm_data:
        try:
            w = abs(st.correlation(parameter, norm_cgpa))
        except:
            w = 0
        weights.append(w)
    total = sum(weights)
    return [w / total for w in weights]

# preprocessing
data_columns = list(zip(*data))
norm_data = [normalize(col) for col in data_columns]
norm_cgpa = normalize(cgpa)

weights = correlation_weight(norm_data, norm_cgpa)
weights[8] = -weights[8]
weights[5] = -weights[5]/2

comb_parameter = [
    sum(weights[i] * norm_data[i][j] for i in range(len(weights)))
    for j in range(len(data))
]

slope, intercept = st.linear_regression(comb_parameter, norm_cgpa)

#  MAIN FUNCTION FLASK WILL CALL
def predict_cgpa(student):
    norm_student = [
        min(
            max(
                (student[i] - min(data_columns[i])) /
                (max(data_columns[i]) - min(data_columns[i])),
                0
            ),
            1
        )
        for i in range(len(student))
    ]

    comb_student = sum(weights[i] * norm_student[i] for i in range(len(weights)))
    comb_student = min(max(comb_student, 0), 1)

    predicted_norm_cgpa = slope * comb_student + intercept
    predicted_norm_cgpa = min(max(predicted_norm_cgpa, 0), 1)

    return round(predicted_norm_cgpa * 4, 2)
