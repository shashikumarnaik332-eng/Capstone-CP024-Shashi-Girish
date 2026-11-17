# CP-024 VitalWatch

**VitalWatch: Patient Vitals Monitoring and Early-Alert System**

Python console implementation of the five compulsory features in CP-024.

## Features
1. Record blood pressure, pulse, temperature, oxygen saturation and time.
2. Raise an alert when a value is outside the project's demo range.
3. Show the trend over the last 3 readings: Improving, Stable or Worsening.
4. List patients with an active alert.
5. Print a shift handover summary.

Additional features: add patient, view readings and search patient.

## Run
```bash
python main.py
```

## Structure
```text
VitalWatch/
├── main.py
├── README.md
└── vitalwatch/
    ├── model/
    │   ├── patient.py
    │   └── vital_record.py
    └── service/
        └── vital_watch_service.py
```

**Important:** Thresholds are for this student/demo project only and are not clinical decision limits.
