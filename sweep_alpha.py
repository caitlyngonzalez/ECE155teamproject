import csv

input_file = "danehy_estimated.csv"

rows = []
with open(input_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            "time_s": float(row["time_s"]),
            "distance_m": float(row["distance_m"]),
            "elevation_true_m": float(row["elevation_true_m"]),
            "baro_grade_pct": float(row["baro_grade_pct"]),
            "imu_grade_pct": float(row["imu_grade_pct"]),
        })

def compute_mae(alpha):
    errors = []

    for i in range(1, len(rows)):
        dd = rows[i]["distance_m"] - rows[i - 1]["distance_m"]
        dh = rows[i]["elevation_true_m"] - rows[i - 1]["elevation_true_m"]

        if dd == 0:
            true_grade = 0.0
        else:
            true_grade = 100.0 * dh / dd

        fused_grade = alpha * rows[i]["baro_grade_pct"] + (1.0 - alpha) * rows[i]["imu_grade_pct"]
        errors.append(abs(fused_grade - true_grade))

    return sum(errors) / len(errors)

best_alpha = None
best_mae = None

for alpha_tenths in range(0, 11):
    alpha = alpha_tenths / 10.0
    mae = compute_mae(alpha)
    print(f"alpha={alpha:.1f}  mae={mae:.3f}% grade")

    if best_mae is None or mae < best_mae:
        best_mae = mae
        best_alpha = alpha

print()
print(f"Best alpha: {best_alpha:.1f}")
print(f"Best MAE: {best_mae:.3f}% grade")
