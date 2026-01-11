def adjust_n_for_weather(n_amount, rain_mm):
    """
    If rain > 20 mm in next 3 days → reduce N by 30%.
    """
    if rain_mm > 20:
        return round(n_amount * 0.7, 2), "Heavy rain expected — reduce N by 30%."
    return n_amount, "No weather adjustment needed."