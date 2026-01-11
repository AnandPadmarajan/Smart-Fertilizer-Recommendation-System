import pandas as pd

def classify_soil(value, thresholds):
    """
    thresholds = row from soil_thresholds.csv
    value = soil test value (mg/100g)
    """
    for cls in ["class_A", "class_B", "class_C", "class_D", "class_E"]:
        rng = thresholds[cls]

        if "<=" in rng:
            limit = float(rng.replace("<=", ""))
            if value <= limit:
                return cls[-1]  # returns A/B/C/D/E

        elif ">" in rng and "-" not in rng:
            limit = float(rng.replace(">", ""))
            if value > limit:
                return cls[-1]

        else:
            low, high = rng.split("-")
            if float(low) <= value <= float(high):
                return cls[-1]

    return "C"  # fallback


def calculate_deficit(required, available):
    return max(required - available, 0)


def convert_to_fertilizer(n_def, p_def, k_def, fert_df):
    """
    Converts nutrient deficits into fertilizer kg/ha.
    """
    result = {}

    for _, row in fert_df.iterrows():
        name = row["fertilizer_name"]
        Np = row["N_percent"] / 100
        Pp = row["P_percent"] / 100
        Kp = row["K_percent"] / 100

        # Avoid division by zero
        if Np > 0:
            result[f"{name}_kg_for_N"] = round(n_def / Np, 2)
        if Pp > 0:
            result[f"{name}_kg_for_P"] = round(p_def / Pp, 2)
        if Kp > 0:
            result[f"{name}_kg_for_K"] = round(k_def / Kp, 2)

    return result