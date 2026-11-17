from datetime import datetime

class VitalRecord:
    def __init__(self, blood_pressure, pulse, temperature, oxygen):
        self.blood_pressure = blood_pressure
        self.pulse = pulse
        self.temperature = temperature
        self.oxygen = oxygen
        self.time = datetime.now()

    def __str__(self):
        return (f"{self.time.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"BP: {self.blood_pressure} | Pulse: {self.pulse} bpm | "
                f"Temp: {self.temperature:.1f} °C | SpO2: {self.oxygen:.1f}%")
