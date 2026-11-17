from vitalwatch.service.vital_watch_service import VitalWatchService

def num(prompt, integer=False):
    while True:
        try:
            return int(input(prompt)) if integer else float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def main():
    app = VitalWatchService()
    while True:
        print("\n===== VITALWATCH =====")
        print("1. Add Patient")
        print("2. Record Vitals")
        print("3. View Patient Vitals")
        print("4. Show Patient Trend")
        print("5. Show Active Alerts")
        print("6. Shift Handover Summary")
        print("7. Search Patient")
        print("8. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            pid = input("Patient ID: ").strip()
            name = input("Patient name: ").strip()
            age = num("Age: ", True)
            app.add_patient(pid, name, age)
            print("Patient added successfully.")
        elif choice == "2":
            pid = input("Patient ID: ").strip()
            if not app.patient_exists(pid):
                print("Patient not found.")
                continue
            bp = input("Blood pressure (systolic/diastolic): ").strip()
            pulse = num("Pulse (bpm): ", True)
            temp = num("Temperature (°C): ")
            oxygen = num("Oxygen saturation (%): ")
            alerts = app.record_vitals(pid, bp, pulse, temp, oxygen)
            print("Vitals recorded successfully.")
            if alerts:
                print("ALERTS:")
                for a in alerts:
                    print("-", a)
            else:
                print("No abnormal values detected.")
        elif choice == "3":
            app.show_patient_vitals(input("Patient ID: ").strip())
        elif choice == "4":
            app.show_trend(input("Patient ID: ").strip())
        elif choice == "5":
            app.show_active_alerts()
        elif choice == "6":
            app.shift_handover_summary()
        elif choice == "7":
            app.search_patient(input("Name or ID: ").strip())
        elif choice == "8":
            print("Thank you for using VitalWatch.")
            break
        else:
            print("Invalid choice. Please select 1-8.")

if __name__ == "__main__":
    main()
