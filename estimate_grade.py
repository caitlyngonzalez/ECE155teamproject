import csv
import math

input_file = "danehy_synthetic.csv"
output_file = "danehy_estimated.csv"

rows = []

with open(input_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            "time_s": float(row["time_s"]),
            "distance_m": float(row["distance_m"]),
            "elevation_true_m": float(row["elevation_true_m"]),
            "baro_altitude_m": float(row["baro_altitude_m"]),
            "pitch_deg_imu": float(row["pitch_deg_imu"]),
            "speed_mps": float(row["speed_mps"]),
        })

for i in range(len(rows)):
    if i == 0:
        rows[i]["baro_grade_pct"] = 0.0
        rows[i]["imu_grade_pct"] = 100.0 * math.tan(math.radians(rows[i]["pitch_deg_imu"]))
        rows[i]["fused_grade_pct"] = rows[i]["imu_grade_pct"]
        continue

    dh_baro = rows[i]["baro_altitude_m"] - rows[i - 1]["baro_altitude_m"]
    dd = rows[i]["distance_m"] - rows[i - 1]["distance_m"]

    if dd == 0:
        baro_grade = 0.0
    else:
        baro_grade = 100.0 * dh_baro / dd

    imu_grade = 100.0 * math.tan(math.radians(rows[i]["pitch_deg_imu"]))

    alpha = 0.7
    fused_grade = alpha * baro_grade + (1.0 - alpha) * imu_grade

    rows[i]["baro_grade_pct"] = baro_grade
    rows[i]["imu_grade_pct"] = imu_grade
    rows[i]["fused_grade_pct"] = fused_grade

with open(output_file, "w", newline="") as f:
    fieldnames = [
        "time_s",
        "distance_m",
        "elevation_true_m",
        "baro_altitude_m",
        "pitch_deg_imu",
        "speed_mps",
        "baro_grade_pct",
        "imu_grade_pct",
        "fused_grade_pct",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Wrote", output_file)
print()
print("First few rows:")
for row in rows[:8]:
    print(
        f't={row["time_s"]:>5.1f}s, '
        f'd={row["distance_m"]:>6.1f}m, '
        f'baro_grade={row["baro_grade_pct"]:>7.2f}%, '
        f'imu_grade={row["imu_grade_pct"]:>7.2f}%, '
        f'fused_grade={row["fused_grade_pct"]:>7.2f}%'
    )
