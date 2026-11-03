class BMP390:
    def __init__(self, i2c_bus=None, address=0x77):
        self.i2c_bus = i2c_bus
        self.address = address
        self.initialized = False

    def initialize(self):
        """
        Set up the BMP390 sensor.
        Later this will configure oversampling, filter settings,
        and measurement mode over I2C.
        """
        self.initialized = True

    def read_pressure_pa(self):
        """
        Return pressure in pascals.
        Replace this placeholder with a real I2C register read later.
        """
        if not self.initialized:
            raise RuntimeError("BMP390 not initialized")
        return 101325.0

    def read_temperature_c(self):
        """
        Return temperature in degrees C.
        Replace this placeholder with a real sensor read later.
        """
        if not self.initialized:
            raise RuntimeError("BMP390 not initialized")
        return 25.0

    def estimate_altitude_m(self, sea_level_pressure_pa=101325.0):
        """
        Estimate altitude from pressure using a standard barometric formula.
        """
        pressure_pa = self.read_pressure_pa()
        altitude_m = 44330.0 * (1.0 - (pressure_pa / sea_level_pressure_pa) ** 0.1903)
        return altitude_m


class MPU6050:
    def __init__(self, i2c_bus=None, address=0x68):
        self.i2c_bus = i2c_bus
        self.address = address
        self.initialized = False

    def initialize(self):
        """
        Set up the MPU-6050 sensor.
        Later this will wake the chip, set accel/gyro ranges,
        and configure sample rate over I2C.
        """
        self.initialized = True

    def read_accel_mps2(self):
        """
        Return acceleration as a dictionary in m/s^2.
        Replace this placeholder with converted raw accelerometer data later.
        """
        if not self.initialized:
            raise RuntimeError("MPU6050 not initialized")
        return {
            "ax": 0.0,
            "ay": 0.0,
            "az": 9.81,
        }

    def read_gyro_dps(self):
        """
        Return angular velocity as a dictionary in deg/s.
        Replace this placeholder with converted raw gyro data later.
        """
        if not self.initialized:
            raise RuntimeError("MPU6050 not initialized")
        return {
            "gx": 0.0,
            "gy": 0.0,
            "gz": 0.0,
        }

    def estimate_pitch_deg(self):
        """
        Estimate pitch angle from accelerometer data only.
        This is a simple placeholder formula for now.
        """
        accel = self.read_accel_mps2()
        ax = accel["ax"]
        ay = accel["ay"]
        az = accel["az"]

        import math
        pitch_rad = math.atan2(ax, (ay ** 2 + az ** 2) ** 0.5)
        pitch_deg = math.degrees(pitch_rad)
        return pitch_deg


if __name__ == "__main__":
    bmp = BMP390()
    mpu = MPU6050()

    bmp.initialize()
    mpu.initialize()

    print("BMP390 test")
    print("Pressure (Pa):", bmp.read_pressure_pa())
    print("Temperature (C):", bmp.read_temperature_c())
    print("Estimated altitude (m):", bmp.estimate_altitude_m())

    print()
    print("MPU6050 test")
    print("Accel (m/s^2):", mpu.read_accel_mps2())
    print("Gyro (deg/s):", mpu.read_gyro_dps())
    print("Estimated pitch (deg):", mpu.estimate_pitch_deg())


