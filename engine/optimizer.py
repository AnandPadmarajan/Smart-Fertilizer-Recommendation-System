def optimize_fertilizers(N_def, P_def, K_def, fert_df):
    """
    Creates a realistic fertilizer plan using:
    - DAP for P (and some N)
    - Urea for remaining N
    - MOP for K
    """

    plan = {}

    # ---------------------------
    # 1. Use DAP to satisfy P
    # ---------------------------
    dap = fert_df[fert_df["fertilizer_name"] == "dap"].iloc[0]
    dap_P = dap["P_percent"] / 100
    dap_N = dap["N_percent"] / 100

    if P_def > 0:
        dap_needed = round(P_def / dap_P, 2)
        plan["DAP_kg"] = dap_needed

        # N supplied by DAP
        N_from_dap = dap_needed * dap_N
        N_def = max(N_def - N_from_dap, 0)
    else:
        plan["DAP_kg"] = 0

    # ---------------------------
    # 2. Use Urea for remaining N
    # ---------------------------
    urea = fert_df[fert_df["fertilizer_name"] == "urea"].iloc[0]
    urea_N = urea["N_percent"] / 100

    if N_def > 0:
        urea_needed = round(N_def / urea_N, 2)
        plan["Urea_kg"] = urea_needed
    else:
        plan["Urea_kg"] = 0

    # ---------------------------
    # 3. Use MOP for K
    # ---------------------------
    mop = fert_df[fert_df["fertilizer_name"] == "mop"].iloc[0]
    mop_K = mop["K_percent"] / 100

    if K_def > 0:
        mop_needed = round(K_def / mop_K, 2)
        plan["MOP_kg"] = mop_needed
    else:
        plan["MOP_kg"] = 0

    return plan