# class BMP390:
#     def __init__(self, i2c_bus=None, address=0x77):
#         self.i2c_bus = i2c_bus
#         self.address = address
#         self.initialized = False

#     def initialize(self):
#         """
#         Set up the BMP390 sensor.
#         Later this will configure oversampling, filter settings,
#         and measurement mode over I2C.
#         """
#         self.initialized = True

#     def read_pressure_pa(self):
#         """
#         Return pressure in pascals.
#         Replace this placeholder with a real I2C register read later.
#         """
#         if not self.initialized:
#             raise RuntimeError("BMP390 not initialized")
#         return 101325.0

#     def read_temperature_c(self):
#         """
#         Return temperature in degrees C.
#         Replace this placeholder with a real sensor read later.
#         """
#         if not self.initialized:
#             raise RuntimeError("BMP390 not initialized")
#         return 25.0

#     def estimate_altitude_m(self, sea_level_pressure_pa=101325.0):
#         """
#         Estimate altitude from pressure using a standard barometric formula.
#         """
#         pressure_pa = self.read_pressure_pa()
#         altitude_m = 44330.0 * (1.0 - (pressure_pa / sea_level_pressure_pa) ** 0.1903)
#         return altitude_m


# class MPU6050:
#     def __init__(self, i2c_bus=None, address=0x68):
#         self.i2c_bus = i2c_bus
#         self.address = address
#         self.initialized = False

#     def initialize(self):
#         """
#         Set up the MPU-6050 sensor.
#         Later this will wake the chip, set accel/gyro ranges,
#         and configure sample rate over I2C.
#         """
#         self.initialized = True

#     def read_accel_mps2(self):
#         """
#         Return acceleration as a dictionary in m/s^2.
#         Replace this placeholder with converted raw accelerometer data later.
#         """
#         if not self.initialized:
#             raise RuntimeError("MPU6050 not initialized")
#         return {
#             "ax": 0.0,
#             "ay": 0.0,
#             "az": 9.81,
#         }

#     def read_gyro_dps(self):
#         """
#         Return angular velocity as a dictionary in deg/s.
#         Replace this placeholder with converted raw gyro data later.
#         """
#         if not self.initialized:
#             raise RuntimeError("MPU6050 not initialized")
#         return {
#             "gx": 0.0,
#             "gy": 0.0,
#             "gz": 0.0,
#         }

#     def estimate_pitch_deg(self):
#         """
#         Estimate pitch angle from accelerometer data only.
#         This is a simple placeholder formula for now.
#         """
#         accel = self.read_accel_mps2()
#         ax = accel["ax"]
#         ay = accel["ay"]
#         az = accel["az"]

#         import math
#         pitch_rad = math.atan2(ax, (ay ** 2 + az ** 2) ** 0.5)
#         pitch_deg = math.degrees(pitch_rad)
#         return pitch_deg


# if __name__ == "__main__":
#     bmp = BMP390()
#     mpu = MPU6050()

#     bmp.initialize()
#     mpu.initialize()

#     print("BMP390 test")
#     print("Pressure (Pa):", bmp.read_pressure_pa())
#     print("Temperature (C):", bmp.read_temperature_c())
#     print("Estimated altitude (m):", bmp.estimate_altitude_m())

#     print()
#     print("MPU6050 test")
#     print("Accel (m/s^2):", mpu.read_accel_mps2())
#     print("Gyro (deg/s):", mpu.read_gyro_dps())
#     print("Estimated pitch (deg):", mpu.estimate_pitch_deg())


import math
import time
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class BMP390Reading:
    timestamp_s: float
    pressure_pa: float
    temperature_c: float
    altitude_m: float


@dataclass
class MPU6050Reading:
    timestamp_s: float
    accel_mps2: Dict[str, float]
    gyro_dps: Dict[str, float]
    pitch_deg: float


@dataclass
class CombinedSensorSample:
    timestamp_s: float
    pressure_pa: float
    temperature_c: float
    altitude_m: float
    accel_mps2: Dict[str, float]
    gyro_dps: Dict[str, float]
    pitch_deg: float


class MockBMP390Backend:
    """
    DEMO BACKEND SO THIS FILE RUNS TONIGHT WITHOUT HARDWARE.
    LATER YOU CAN REPLACE THIS WITH A REAL I2C BACKEND.
    """

    def __init__(self):
        self.start_time = time.time()

    def initialize(self):
        return True

    def read_pressure_pa(self):
        elapsed = time.time() - self.start_time
        return 101325.0 - 8.0 * math.sin(elapsed / 4.0)

    def read_temperature_c(self):
        elapsed = time.time() - self.start_time
        return 24.5 + 0.3 * math.sin(elapsed / 10.0)


class MockMPU6050Backend:
    """
    DEMO BACKEND SO THIS FILE RUNS TONIGHT WITHOUT HARDWARE.
    LATER YOU CAN REPLACE THIS WITH A REAL I2C BACKEND.
    """

    def __init__(self):
        self.start_time = time.time()

    def initialize(self):
        return True

    def read_accel_mps2(self):
        elapsed = time.time() - self.start_time
        pitch_deg = 5.0 * math.sin(elapsed / 3.0)
        pitch_rad = math.radians(pitch_deg)

        ax = 9.81 * math.sin(pitch_rad)
        ay = 0.0
        az = 9.81 * math.cos(pitch_rad)

        return {
            "ax": ax,
            "ay": ay,
            "az": az,
        }

    def read_gyro_dps(self):
        elapsed = time.time() - self.start_time
        return {
            "gx": 1.2 * math.cos(elapsed / 3.0),
            "gy": 0.2 * math.sin(elapsed / 5.0),
            "gz": 0.1 * math.sin(elapsed / 7.0),
        }


class BMP390Driver:
    """
    PYTHON-SIDE DRIVER INTERFACE FOR BMP390.

    THIS IS NEAR-FINAL STRUCTURE, BUT THE REAL HARDWARE ACCESS
    STILL DEPENDS ON WHAT SENSOR BREAKOUT THE TEAM ACTUALLY USES.
    """

    DEFAULT_ADDRESS_1 = 0x76
    DEFAULT_ADDRESS_2 = 0x77

    def __init__(
        self,
        backend=None,
        address=DEFAULT_ADDRESS_1,
        sea_level_pressure_pa=101325.0,
    ):
        self.backend = backend if backend is not None else MockBMP390Backend()
        self.address = address
        self.sea_level_pressure_pa = sea_level_pressure_pa
        self.initialized = False

        # CONFIRM WITH TEAM WHICH BMP390 BREAKOUT IS ORDERED
        # AND WHETHER ITS DEFAULT ADDRESS IS 0x76 OR 0x77.

        # CONFIRM WITH TEAM WHETHER THIS SENSOR SHARES THE MAIN ESP32
        # I2C BUS ON GPIO 21/22 OR IF A DIFFERENT BUS/PIN MAP IS USED.

    def initialize(self):
        self.backend.initialize()
        self.initialized = True
        return True

    def read_pressure_pa(self):
        self._require_initialized()
        return float(self.backend.read_pressure_pa())

    def read_temperature_c(self):
        self._require_initialized()
        return float(self.backend.read_temperature_c())

    def estimate_altitude_m(self, pressure_pa: Optional[float] = None):
        self._require_initialized()

        if pressure_pa is None:
            pressure_pa = self.read_pressure_pa()

        altitude_m = 44330.0 * (
            1.0 - (pressure_pa / self.sea_level_pressure_pa) ** 0.1903
        )
        return altitude_m

    def read(self):
        self._require_initialized()

        timestamp_s = time.time()
        pressure_pa = self.read_pressure_pa()
        temperature_c = self.read_temperature_c()
        altitude_m = self.estimate_altitude_m(pressure_pa)

        return BMP390Reading(
            timestamp_s=timestamp_s,
            pressure_pa=pressure_pa,
            temperature_c=temperature_c,
            altitude_m=altitude_m,
        )

    def _require_initialized(self):
        if not self.initialized:
            raise RuntimeError("BMP390Driver not initialized")


class MPU6050Driver:
    """
    PYTHON-SIDE DRIVER INTERFACE FOR MPU-6050.

    THIS IS NEAR-FINAL STRUCTURE, BUT THE REAL HARDWARE ACCESS
    STILL DEPENDS ON THE EXACT BREAKOUT, ADDRESS, AND PLATFORM.
    """

    DEFAULT_ADDRESS_LOW = 0x68
    DEFAULT_ADDRESS_HIGH = 0x69

    def __init__(self, backend=None, address=DEFAULT_ADDRESS_LOW):
        self.backend = backend if backend is not None else MockMPU6050Backend()
        self.address = address
        self.initialized = False

        self.accel_bias = {"ax": 0.0, "ay": 0.0, "az": 0.0}
        self.gyro_bias = {"gx": 0.0, "gy": 0.0, "gz": 0.0}

        # CONFIRM WITH TEAM WHETHER MPU-6050 AD0 IS TIED LOW OR HIGH.
        # LOW TYPICALLY MEANS 0x68, HIGH TYPICALLY MEANS 0x69.

        # CONFIRM WITH TEAM WHETHER THE FINAL IMU IS REALLY MPU-6050
        # OR A DIFFERENT IMU BREAKOUT BEFORE HARDWARE TEST DAY.

    def initialize(self):
        self.backend.initialize()
        self.initialized = True
        return True

    def read_accel_mps2(self):
        self._require_initialized()

        raw = self.backend.read_accel_mps2()
        return {
            "ax": float(raw["ax"]) - self.accel_bias["ax"],
            "ay": float(raw["ay"]) - self.accel_bias["ay"],
            "az": float(raw["az"]) - self.accel_bias["az"],
        }

    def read_gyro_dps(self):
        self._require_initialized()

        raw = self.backend.read_gyro_dps()
        return {
            "gx": float(raw["gx"]) - self.gyro_bias["gx"],
            "gy": float(raw["gy"]) - self.gyro_bias["gy"],
            "gz": float(raw["gz"]) - self.gyro_bias["gz"],
        }

    def estimate_pitch_deg(self, accel_mps2: Optional[Dict[str, float]] = None):
        self._require_initialized()

        if accel_mps2 is None:
            accel_mps2 = self.read_accel_mps2()

        ax = accel_mps2["ax"]
        ay = accel_mps2["ay"]
        az = accel_mps2["az"]

        pitch_rad = math.atan2(ax, math.sqrt(ay ** 2 + az ** 2))
        return math.degrees(pitch_rad)

    def calibrate_biases_from_stationary_data(self, samples=50, delay_s=0.01):
        """
        SIMPLE STATIONARY CALIBRATION.
        PLACE SENSOR STILL ON A TABLE.
        FOR AZ, WE REMOVE 1g SO THE BIAS REPRESENTS OFFSET, NOT GRAVITY.
        """
        self._require_initialized()

        accel_sum = {"ax": 0.0, "ay": 0.0, "az": 0.0}
        gyro_sum = {"gx": 0.0, "gy": 0.0, "gz": 0.0}

        for _ in range(samples):
            accel = self.backend.read_accel_mps2()
            gyro = self.backend.read_gyro_dps()

            accel_sum["ax"] += accel["ax"]
            accel_sum["ay"] += accel["ay"]
            accel_sum["az"] += accel["az"] - 9.81

            gyro_sum["gx"] += gyro["gx"]
            gyro_sum["gy"] += gyro["gy"]
            gyro_sum["gz"] += gyro["gz"]

            time.sleep(delay_s)

        self.accel_bias = {
            "ax": accel_sum["ax"] / samples,
            "ay": accel_sum["ay"] / samples,
            "az": accel_sum["az"] / samples,
        }

        self.gyro_bias = {
            "gx": gyro_sum["gx"] / samples,
            "gy": gyro_sum["gy"] / samples,
            "gz": gyro_sum["gz"] / samples,
        }

        return {
            "accel_bias": self.accel_bias,
            "gyro_bias": self.gyro_bias,
        }

    def read(self):
        self._require_initialized()

        timestamp_s = time.time()
        accel_mps2 = self.read_accel_mps2()
        gyro_dps = self.read_gyro_dps()
        pitch_deg = self.estimate_pitch_deg(accel_mps2)

        return MPU6050Reading(
            timestamp_s=timestamp_s,
            accel_mps2=accel_mps2,
            gyro_dps=gyro_dps,
            pitch_deg=pitch_deg,
        )

    def _require_initialized(self):
        if not self.initialized:
            raise RuntimeError("MPU6050Driver not initialized")


class GradeSensorSuite:
    """
    COMBINES BMP390 + MPU-6050 INTO ONE SAMPLE STREAM.
    THIS IS THE MAIN THING YOUR FUTURE GRADE-ESTIMATION CODE CAN CALL.
    """

    def __init__(self, bmp390: BMP390Driver, mpu6050: MPU6050Driver):
        self.bmp390 = bmp390
        self.mpu6050 = mpu6050

        # CONFIRM WITH TEAM WHAT FINAL CSV COLUMN NAMES SHOULD BE
        # SO THESE KEYS MATCH THE SHARED LOG FORMAT.

    def initialize(self):
        self.bmp390.initialize()
        self.mpu6050.initialize()

    def read_sample(self):
        bmp = self.bmp390.read()
        imu = self.mpu6050.read()

        return CombinedSensorSample(
            timestamp_s=time.time(),
            pressure_pa=bmp.pressure_pa,
            temperature_c=bmp.temperature_c,
            altitude_m=bmp.altitude_m,
            accel_mps2=imu.accel_mps2,
            gyro_dps=imu.gyro_dps,
            pitch_deg=imu.pitch_deg,
        )

    def read_sample_dict(self):
        sample = self.read_sample()

        return {
            "timestamp_s": sample.timestamp_s,
            "pressure_pa": sample.pressure_pa,
            "temperature_c": sample.temperature_c,
            "altitude_m": sample.altitude_m,
            "ax_mps2": sample.accel_mps2["ax"],
            "ay_mps2": sample.accel_mps2["ay"],
            "az_mps2": sample.accel_mps2["az"],
            "gx_dps": sample.gyro_dps["gx"],
            "gy_dps": sample.gyro_dps["gy"],
            "gz_dps": sample.gyro_dps["gz"],
            "pitch_deg": sample.pitch_deg,
        }


if __name__ == "__main__":
    bmp = BMP390Driver()
    imu = MPU6050Driver()
    suite = GradeSensorSuite(bmp, imu)

    suite.initialize()

    print("RUNNING SENSOR DRIVER SELF-TEST IN MOCK MODE")
    print("IF YOU SEE NUMBERS CHANGING, THE INTERFACES ARE WORKING.\n")

    calibration = imu.calibrate_biases_from_stationary_data(samples=10, delay_s=0.01)
    print("IMU CALIBRATION:")
    print(calibration)
    print()

    for i in range(5):
        sample = suite.read_sample_dict()
        print(f"SAMPLE {i + 1}")
        for key, value in sample.items():
            print(f"  {key}: {value}")
        print()
        time.sleep(0.5)
