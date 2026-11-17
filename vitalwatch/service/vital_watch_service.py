from vitalwatch.model.patient import Patient
from vitalwatch.model.vital_record import VitalRecord

class VitalWatchService:
    # Demo/project thresholds only; not clinical decision limits.
    PULSE_MIN, PULSE_MAX = 60, 100
    TEMP_MIN, TEMP_MAX = 36.1, 37.5
    OXYGEN_MIN = 95
    SYS_MIN, SYS_MAX = 90, 140
    DIA_MIN, DIA_MAX = 60, 90

    def __init__(self):
        self.patients = {}

    def add_patient(self, pid, name, age):
        self.patients[pid] = Patient(pid, name, age)

    def patient_exists(self, pid):
        return pid in self.patients

    def record_vitals(self, pid, bp, pulse, temp, oxygen):
        patient = self.patients[pid]
        record = VitalRecord(bp, pulse, temp, oxygen)
        patient.records.append(record)
        patient.active_alerts = self.check_alerts(record)
        return patient.active_alerts

    def check_alerts(self, r):
        alerts = []
        try:
            sys, dia = map(int, r.blood_pressure.replace(" ", "").split("/"))
            if sys < self.SYS_MIN or sys > self.SYS_MAX:
                alerts.append("Blood pressure systolic value is outside normal range.")
            if dia < self.DIA_MIN or dia > self.DIA_MAX:
                alerts.append("Blood pressure diastolic value is outside normal range.")
        except ValueError:
            alerts.append("Invalid blood pressure format. Use systolic/diastolic.")

        if r.pulse < self.PULSE_MIN or r.pulse > self.PULSE_MAX:
            alerts.append("Pulse is outside normal range.")
        if r.temperature < self.TEMP_MIN or r.temperature > self.TEMP_MAX:
            alerts.append("Temperature is outside normal range.")
        if r.oxygen < self.OXYGEN_MIN:
            alerts.append("Oxygen saturation is below normal range.")
        return alerts

    def abnormal_score(self, r):
        return len(self.check_alerts(r))

    def show_patient_vitals(self, pid):
        p = self.patients.get(pid)
        if not p:
            print("Patient not found."); return
        print(f"\nPatient: {p.name} | ID: {p.patient_id} | Age: {p.age}")
        if not p.records:
            print("No vitals recorded."); return
        for i, r in enumerate(p.records, 1):
            print(f"{i}. {r}")

    def show_trend(self, pid):
        p = self.patients.get(pid)
        if not p:
            print("Patient not found."); return
        if len(p.records) < 3:
            print("At least 3 readings are required to show a trend."); return
        last = p.records[-3:]
        scores = [self.abnormal_score(r) for r in last]
        print(f"\nTrend for {p.name} (last 3 readings):")
        for r in last: print(r)
        print(f"Abnormal-value score: {scores[0]} -> {scores[1]} -> {scores[2]}")
        if scores[-1] < scores[0]: trend = "IMPROVING"
        elif scores[-1] > scores[0]: trend = "WORSENING"
        else: trend = "STABLE"
        print("Overall trend:", trend)

    def show_active_alerts(self):
        print("\n===== ACTIVE ALERTS =====")
        found = False
        for p in self.patients.values():
            if p.active_alerts:
                found = True
                print(f"\n{p.patient_id} - {p.name}")
                for a in p.active_alerts: print("-", a)
        if not found: print("No patients currently have active alerts.")

    def shift_handover_summary(self):
        print("\n===== SHIFT HANDOVER SUMMARY =====")
        if not self.patients:
            print("No patients registered."); return
        for p in self.patients.values():
            print(f"\nPatient: {p.name} | ID: {p.patient_id} | Age: {p.age}")
            if not p.records:
                print("No vitals recorded."); continue
            print("Latest:", p.records[-1])
            print("Status:", "ALERT" if p.active_alerts else "Stable")
            for a in p.active_alerts: print(" -", a)
            if len(p.records) >= 3:
                scores = [self.abnormal_score(r) for r in p.records[-3:]]
                trend = "Improving" if scores[-1] < scores[0] else "Worsening" if scores[-1] > scores[0] else "Stable"
                print("3-reading trend:", trend)
            else:
                print("3-reading trend: Not enough readings")

    def search_patient(self, text):
        text = text.lower()
        matches = [p for p in self.patients.values()
                   if text in p.patient_id.lower() or text in p.name.lower()]
        if not matches:
            print("No matching patient found."); return
        for p in matches:
            print(f"ID: {p.patient_id} | Name: {p.name} | Age: {p.age}")
