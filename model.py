def predict_risk(rainfall):
    # LOW value = heavy rain

    if rainfall < 300:
        return "High Risk", 90
    elif rainfall < 600:
        return "Risk", 60
    else:
        return "Normal", 20