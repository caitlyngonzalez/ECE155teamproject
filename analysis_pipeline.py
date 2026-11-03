import csv

input_file = "fake_bike_log.csv"

rows = []
with open(input_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            "time_s": float(row["time_s"]),
            "distance_m": float(row["distance_m"]),
            "speed_mps": float(row["speed_mps"]),
            "voltage_v": float(row["voltage_v"]),
            "current_a": float(row["current_a"]),
            "throttle_cmd": float(row["throttle_cmd"]),
            "estimated_grade_pct": float(row["estimated_grade_pct"]),
        })

total_energy_j = 0.0
peak_current_a = 0.0
peak_power_w = 0.0
max_speed_mps = 0.0

for i in range(len(rows)):
    power_w = rows[i]["voltage_v"] * rows[i]["current_a"]
    rows[i]["power_w"] = power_w

    if power_w > peak_power_w:
        peak_power_w = power_w

    if rows[i]["current_a"] > peak_current_a:
        peak_current_a = rows[i]["current_a"]

    if rows[i]["speed_mps"] > max_speed_mps:
        max_speed_mps = rows[i]["speed_mps"]

    if i > 0:
        dt = rows[i]["time_s"] - rows[i - 1]["time_s"]
        total_energy_j += power_w * dt

total_energy_wh = total_energy_j / 3600.0
total_distance_km = rows[-1]["distance_m"] / 1000.0

if total_distance_km > 0:
    wh_per_km = total_energy_wh / total_distance_km
else:
    wh_per_km = 0.0

avg_speed_mps = rows[-1]["distance_m"] / rows[-1]["time_s"]
avg_speed_kph = avg_speed_mps * 3.6
max_speed_kph = max_speed_mps * 3.6

final_speed = rows[-1]["speed_mps"]
target_90 = 0.9 * final_speed
rise_time_s = None

for row in rows:
    if row["speed_mps"] >= target_90:
        rise_time_s = row["time_s"]
        break

overshoot_mps = max_speed_mps - final_speed
if final_speed > 0:
    overshoot_pct = 100.0 * overshoot_mps / final_speed
else:
    overshoot_pct = 0.0

print("Bike Log Analysis")
print("-----------------")
print(f"Total distance: {total_distance_km:.3f} km")
print(f"Total energy: {total_energy_wh:.3f} Wh")
print(f"Efficiency: {wh_per_km:.3f} Wh/km")
print(f"Peak current: {peak_current_a:.2f} A")
print(f"Peak power: {peak_power_w:.2f} W")
print(f"Average speed: {avg_speed_kph:.2f} km/h")
print(f"Max speed: {max_speed_kph:.2f} km/h")

if rise_time_s is not None:
    print(f"Rise time to 90% of final speed: {rise_time_s:.2f} s")
else:
    print("Rise time to 90% of final speed: not reached")

print(f"Overshoot: {overshoot_pct:.2f}%")
#This script gives the following:
#Total distance
#Total energy
#Wh/km
#Peak current
#Peak power
#Average speed
#Max speed
#Rise time
#Overshoot

#remember csv can not have comments.
"""
but csv does this -->
bike starts from rest,
ramps up assist, 
climbs a hill, 
peaks in grade, 
then hill flattens,
 and the assist reduces.

 and run in terminal:
 
 python3 analysis_pipeline.py


"""

