def suggest_agri(rain_pred):
    if rain_pred > 5:
        return "Rain expected – delay irrigation!"
    elif rain_pred < 1:
        return "No rain forecast – irrigate manually."
    else:
        return "Possibility of light rain – monitor and adjust."

def suggest_energy(pred_usage):
    if pred_usage > 400:
        return "High demand predicted – shift usage to night hours."
    elif pred_usage < 250:
        return "Energy usage optimal."
    else:
        return "Consider using efficient appliances."

def sustainability_score(rainfall, energy_usage):
    score = 100
    if rainfall < 1:
        score -= 20
    if energy_usage > 400:
        score -= 30
    return max(score, 0)
