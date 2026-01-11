from engine.loader import (
    load_crop_requirements,
    load_soil_thresholds,
    load_fertilizer_content
)
from engine.calculator import (
    classify_soil,
    calculate_deficit,
    convert_to_fertilizer
)
from engine.weather_adjustment import adjust_n_for_weather
from engine.optimizer import optimize_fertilizers


def get_recommendation(crop, soil_N, soil_P, soil_K, rain_mm):
    crop_df = load_crop_requirements()
    soil_df = load_soil_thresholds()
    fert_df = load_fertilizer_content()

    # 1. Get crop requirements
    row = crop_df[crop_df["crop"] == crop].iloc[0]
    req_N = row["N_required_kg_per_ha"]
    req_P = row["P_required_kg_per_ha"]
    req_K = row["K_required_kg_per_ha"]

    # 2. Classify soil
    P_class = classify_soil(soil_P, soil_df[soil_df["nutrient"] == "P_CAL"].iloc[0])
    K_class = classify_soil(soil_K, soil_df[soil_df["nutrient"] == "K_CAL"].iloc[0])
    Mg_class = classify_soil(soil_K, soil_df[soil_df["nutrient"] == "Mg_CaCl2"].iloc[0])

    # 3. Calculate deficits
    N_def = calculate_deficit(req_N, soil_N)
    P_def = calculate_deficit(req_P, soil_P)
    K_def = calculate_deficit(req_K, soil_K)

    # 4. Optimize fertilizer
    fert_plan = optimize_fertilizers(N_def, P_def, K_def, fert_df)

    # 5. Weather adjustment
    adjusted_N, weather_msg = adjust_n_for_weather(N_def, rain_mm)

    return {
        "soil_classes": {
            "P": P_class,
            "K": K_class,
            "Mg": Mg_class
        },
        "nutrient_deficit": {
            "N_deficit": N_def,
            "P_deficit": P_def,
            "K_deficit": K_def
        },
        "fertilizer_plan": fert_plan,
        "weather_message": weather_msg
    }

if __name__ == "__main__":
    result = get_recommendation(
        crop="wheat",
        soil_N=50,
        soil_P=2.0,
        soil_K=5.0,
        rain_mm=25
    )
    print(result)