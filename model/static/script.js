let lastStudentData = [];

function predict() {
    const data = {
        study_hours: study_hours.value,
        attendance: attendance.value,
        consistency: consistency.value,
        self_study: self_study.value,
        sleep: sleep.value,
        stress: stress.value,
        time_management: time_management.value,
        participation: participation.value,
        screen_time: screen_time.value,
        motivation: motivation.value
    };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("prediction").innerText =
            "Predicted CGPA: " + result.predicted_cgpa;

        lastStudentData = result.student;
        document.getElementById("feedback_box").style.display = "block";
    });
}

function submitFeedback() {
    const expected = document.getElementById("expected_cgpa").value;

    fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student: lastStudentData,
            expected_cgpa: expected
        })
    })
    .then(res => res.json())
    .then(msg => {
        document.getElementById("status").innerText = msg.message;
    });
}
