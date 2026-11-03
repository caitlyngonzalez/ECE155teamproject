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
            "fused_grade_pct": float(row["fused_grade_pct"]),
        })

abs_errors = []

print("time_s, true_grade_pct, fused_grade_pct, abs_error_pct")
for i in range(1, len(rows)):
    dd = rows[i]["distance_m"] - rows[i - 1]["distance_m"]
    dh = rows[i]["elevation_true_m"] - rows[i - 1]["elevation_true_m"]

    if dd == 0:
        true_grade = 0.0
    else:
        true_grade = 100.0 * dh / dd

    fused_grade = rows[i]["fused_grade_pct"]
    abs_error = abs(fused_grade - true_grade)
    abs_errors.append(abs_error)

    print(
        f'{rows[i]["time_s"]:.1f}, '
        f'{true_grade:.2f}, '
        f'{fused_grade:.2f}, '
        f'{abs_error:.2f}'
    )

mae = sum(abs_errors) / len(abs_errors)
print()
print(f"Mean absolute error: {mae:.2f}% grade")
