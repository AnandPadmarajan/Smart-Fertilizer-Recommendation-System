from fastapi import FastAPI
from pydantic import BaseModel

from engine.loader import (
    load_crop_requirements,
    load_soil_thresholds,
    load_fertilizer_content
)
from engine.calculator import (
    classify_soil,
    calculate_deficit
)
from engine.weather_adjustment import adjust_n_for_weather
from engine.optimizer import optimize_fertilizers

app = FastAPI(title="Fertilizer Recommendation API")


# -------------------------
# Request Model
# -------------------------
class SoilInput(BaseModel):
    crop: str
    soil_N: float
    soil_P: float
    soil_K: float
    rain_mm: float


# -------------------------
# API Endpoint
# -------------------------
@app.post("/recommend")
def recommend(data: SoilInput):

    crop_df = load_crop_requirements()
    soil_df = load_soil_thresholds()
    fert_df = load_fertilizer_content()

    # 1. Crop requirements
    row = crop_df[crop_df["crop"] == data.crop].iloc[0]
    req_N = row["N_required_kg_per_ha"]
    req_P = row["P_required_kg_per_ha"]
    req_K = row["K_required_kg_per_ha"]

    # 2. Soil classes
    P_class = classify_soil(data.soil_P, soil_df[soil_df["nutrient"] == "P_CAL"].iloc[0])
    K_class = classify_soil(data.soil_K, soil_df[soil_df["nutrient"] == "K_CAL"].iloc[0])
    Mg_class = classify_soil(data.soil_K, soil_df[soil_df["nutrient"] == "Mg_CaCl2"].iloc[0])

    # 3. Deficits
    N_def = calculate_deficit(req_N, data.soil_N)
    P_def = calculate_deficit(req_P, data.soil_P)
    K_def = calculate_deficit(req_K, data.soil_K)

    # 4. Optimized fertilizer plan
    fert_plan = optimize_fertilizers(N_def, P_def, K_def, fert_df)

    # 5. Weather adjustment
    adjusted_N, weather_msg = adjust_n_for_weather(N_def, data.rain_mm)

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