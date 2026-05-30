"""
Utility Usage Prediction Tool
CodeVedX AI/ML Internship - Project 1
Author: [Your Name]
"""

from data_manager import DataManager
from model_trainer import ModelTrainer
from utils import clear_screen, print_header, get_float_input, get_month_input


def main():
    """Main function - runs the menu-driven application."""
    data_manager = DataManager()
    model_trainer = ModelTrainer()

    while True:
        clear_screen()
        print_header()

        print("\n  📋 MAIN MENU")
        print("  " + "─" * 35)
        print("  1. Add usage data")
        print("  2. View all records")
        print("  3. Update existing record")
        print("  4. Delete a record")
        print("  5. Train ML prediction model")
        print("  6. Predict next month usage")
        print("  7. Export data to CSV")
        print("  8. Load sample data (for testing)")
        print("  9. Exit")
        print("  " + "─" * 35)

        try:
            choice = input("\n  Enter your choice (1-9): ").strip()

            if choice == "1":
                add_data(data_manager)
            elif choice == "2":
                view_records(data_manager)
            elif choice == "3":
                update_record(data_manager)
            elif choice == "4":
                delete_record(data_manager)
            elif choice == "5":
                train_model(data_manager, model_trainer)
            elif choice == "6":
                predict_usage(data_manager, model_trainer)
            elif choice == "7":
                export_data(data_manager)
            elif choice == "8":
                load_sample(data_manager)
            elif choice == "9":
                print("\n  👋 Thank you for using Utility Predictor! Goodbye!\n")
                break
            else:
                print("\n  ❌ Invalid choice. Please enter a number between 1 and 9.")
                input("\n  Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n  👋 Exiting... Goodbye!\n")
            break


def add_data(data_manager):
    """Add new monthly utility usage data."""
    clear_screen()
    print("\n  ➕ ADD USAGE DATA")
    print("  " + "─" * 35)

    try:
        month = get_month_input("  Enter month (YYYY-MM, e.g. 2024-05): ")

        # Check if record already exists
        if data_manager.record_exists(month):
            overwrite = input(f"\n  ⚠  Record for {month} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("\n  Operation cancelled.")
                input("\n  Press Enter to continue...")
                return

        electricity = get_float_input("  Electricity usage (units/kWh): ", min_val=0)
        water = get_float_input("  Water usage (liters): ", min_val=0)
        gas = get_float_input("  Gas usage (units): ", min_val=0)
        bill = get_float_input("  Total bill amount (₹): ", min_val=0)

        data_manager.add_record(month, electricity, water, gas, bill)
        print(f"\n  ✅ Record for {month} saved successfully!")

    except Exception as e:
        print(f"\n  ❌ Error: {e}")

    input("\n  Press Enter to continue...")


def view_records(data_manager):
    """Display all stored records in a formatted table."""
    clear_screen()
    print("\n  📊 ALL USAGE RECORDS")
    print("  " + "─" * 70)

    records = data_manager.get_all_records()

    if records.empty:
        print("\n  No records found. Please add some data first.")
    else:
        print(f"\n  {'Month':<12} {'Electricity':>12} {'Water':>12} {'Gas':>10} {'Bill (₹)':>10}")
        print("  " + "─" * 60)
        for _, row in records.iterrows():
            print(f"  {row['month']:<12} {row['electricity']:>10.1f} u  {row['water']:>10.1f} L  {row['gas']:>8.1f} u  {row['bill']:>9.2f}")
        print("  " + "─" * 60)
        print(f"\n  Total records: {len(records)}")

        # Show averages
        print(f"\n  📈 Averages:")
        print(f"  Electricity: {records['electricity'].mean():.1f} units/month")
        print(f"  Water:       {records['water'].mean():.1f} liters/month")
        print(f"  Bill:        ₹{records['bill'].mean():.2f}/month")

    input("\n  Press Enter to continue...")


def update_record(data_manager):
    """Update an existing monthly record."""
    clear_screen()
    print("\n  ✏  UPDATE RECORD")
    print("  " + "─" * 35)

    records = data_manager.get_all_records()
    if records.empty:
        print("\n  No records found. Please add data first.")
        input("\n  Press Enter to continue...")
        return

    month = get_month_input("  Enter month to update (YYYY-MM): ")

    if not data_manager.record_exists(month):
        print(f"\n  ❌ No record found for {month}.")
        input("\n  Press Enter to continue...")
        return

    print(f"\n  Enter new values for {month} (press Enter to keep current value):")
    row = data_manager.get_record(month)

    try:
        elec_in = input(f"  Electricity [{row['electricity']:.1f} units]: ").strip()
        water_in = input(f"  Water [{row['water']:.1f} liters]: ").strip()
        gas_in = input(f"  Gas [{row['gas']:.1f} units]: ").strip()
        bill_in = input(f"  Bill [₹{row['bill']:.2f}]: ").strip()

        electricity = float(elec_in) if elec_in else row['electricity']
        water = float(water_in) if water_in else row['water']
        gas = float(gas_in) if gas_in else row['gas']
        bill = float(bill_in) if bill_in else row['bill']

        data_manager.add_record(month, electricity, water, gas, bill)
        print(f"\n  ✅ Record for {month} updated successfully!")

    except ValueError:
        print("\n  ❌ Invalid input. Update cancelled.")

    input("\n  Press Enter to continue...")


def delete_record(data_manager):
    """Delete a specific monthly record."""
    clear_screen()
    print("\n  🗑  DELETE RECORD")
    print("  " + "─" * 35)

    month = get_month_input("  Enter month to delete (YYYY-MM): ")

    if not data_manager.record_exists(month):
        print(f"\n  ❌ No record found for {month}.")
    else:
        confirm = input(f"\n  ⚠  Delete record for {month}? This cannot be undone. (y/n): ").lower()
        if confirm == 'y':
            data_manager.delete_record(month)
            print(f"\n  ✅ Record for {month} deleted.")
        else:
            print("\n  Deletion cancelled.")

    input("\n  Press Enter to continue...")


def train_model(data_manager, model_trainer):
    """Train the ML prediction model on existing data."""
    clear_screen()
    print("\n  🤖 TRAIN ML MODEL")
    print("  " + "─" * 35)

    records = data_manager.get_all_records()

    if len(records) < 3:
        print(f"\n  ❌ Need at least 3 months of data to train. You have {len(records)} record(s).")
        input("\n  Press Enter to continue...")
        return

    print(f"\n  Training on {len(records)} months of data...")
    print("  Using: Linear Regression (scikit-learn)\n")

    results = model_trainer.train(records)

    print("  ✅ Model trained successfully!\n")
    print("  📊 Model Performance (R² Score):")
    print(f"  Electricity: {results['r2_electricity']:.4f} ({results['r2_electricity']*100:.1f}% accuracy)")
    print(f"  Water:       {results['r2_water']:.4f} ({results['r2_water']*100:.1f}% accuracy)")
    print(f"  Gas:         {results['r2_gas']:.4f} ({results['r2_gas']*100:.1f}% accuracy)")
    print(f"  Bill:        {results['r2_bill']:.4f} ({results['r2_bill']*100:.1f}% accuracy)")
    print(f"\n  Model saved to: models/utility_model.pkl")

    input("\n  Press Enter to continue...")


def predict_usage(data_manager, model_trainer):
    """Predict next month's utility usage."""
    clear_screen()
    print("\n  🔮 PREDICT NEXT MONTH USAGE")
    print("  " + "─" * 35)

    if not model_trainer.is_trained():
        print("\n  ❌ No trained model found. Please train the model first (Option 5).")
        input("\n  Press Enter to continue...")
        return

    records = data_manager.get_all_records()
    if records.empty:
        print("\n  ❌ No data available for prediction.")
        input("\n  Press Enter to continue...")
        return

    prediction = model_trainer.predict(records)

    print(f"\n  📅 Predicted usage for Month {len(records) + 1}:\n")
    print(f"  ⚡ Electricity:  {max(0, prediction['electricity']):.1f} units")
    print(f"  💧 Water:        {max(0, prediction['water']):.1f} liters")
    print(f"  🔥 Gas:          {max(0, prediction['gas']):.1f} units")
    print(f"  💰 Total Bill:   ₹{max(0, prediction['bill']):.2f}")

    print(f"\n  ℹ  Prediction based on {len(records)} months of historical data.")
    print("  Model: Linear Regression | Feature: Month index (time series)")

    input("\n  Press Enter to continue...")


def export_data(data_manager):
    """Export all data to CSV file."""
    clear_screen()
    print("\n  📤 EXPORT DATA")
    print("  " + "─" * 35)

    records = data_manager.get_all_records()

    if records.empty:
        print("\n  ❌ No data to export.")
    else:
        filename = input("  Enter export filename (default: exported_data.csv): ").strip()
        if not filename:
            filename = "exported_data.csv"
        if not filename.endswith('.csv'):
            filename += '.csv'

        records.to_csv(filename, index=False)
        print(f"\n  ✅ Data exported to: {filename}")
        print(f"  Records exported: {len(records)}")

    input("\n  Press Enter to continue...")


def load_sample(data_manager):
    """Load sample data for testing/demo purposes."""
    clear_screen()
    print("\n  📥 LOAD SAMPLE DATA")
    print("  " + "─" * 35)

    confirm = input("  This will add 6 months of sample data. Continue? (y/n): ").lower()
    if confirm != 'y':
        print("\n  Cancelled.")
        input("\n  Press Enter to continue...")
        return

    sample_data = [
        ("2024-01", 210, 7800, 11, 1650),
        ("2024-02", 195, 7200, 10, 1520),
        ("2024-03", 230, 8100, 12, 1780),
        ("2024-04", 250, 8500, 13, 1950),
        ("2024-05", 240, 8300, 12, 1870),
        ("2024-06", 265, 8900, 14, 2050),
    ]

    for month, elec, water, gas, bill in sample_data:
        data_manager.add_record(month, elec, water, gas, bill)

    print(f"\n  ✅ Loaded {len(sample_data)} sample records!")
    print("  You can now train the model (Option 5) and predict (Option 6).")

    input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
