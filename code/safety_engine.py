def classify_health(rul):
    if rul < 10:
        return "CRITICAL"
    elif rul < 30:
        return "WARNING"
    else:
        return "NORMAL"


def generate_alert(rul, sensor_values):
    alerts = []

    if rul < 10:
        alerts.append("Engine failure imminent. Immediate maintenance required.")
    elif rul < 30:
        alerts.append("Engine approaching failure window. Schedule inspection.")

    if 'sensor_7' in sensor_values and sensor_values['sensor_7'] > 50:
        alerts.append("Excessive vibration detected.")

    if not alerts:
        alerts.append("Engine operating within safe limits.")

    return alerts