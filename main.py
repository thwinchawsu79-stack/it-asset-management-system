
import json
import csv
from asset_functions import (
    is_asset_assigned,
    assign_asset,
    unassign_asset,
    asset_summary,
    filter_assets,
    search_asset,
    delete_asset,
    update_asset
)


def load_assets():
    try:
        with open("assets.json", "r") as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Asset data must be a list.")

            return data

    except FileNotFoundError:
        print("No asset file found. Starting with an empty inventory.")
        return []

    except (json.JSONDecodeError, ValueError) as error:
        print("Error loading asset data:", error)
        raise SystemExit("Program stopped to protect your asset data.")


assets = load_assets()


def save_assets():
    with open("assets.json", "w") as file:
        json.dump(assets, file, indent=4)


def register_asset():
    print("\n--- REGISTER NEW ASSET ---")

    asset_id = input("Enter Asset ID: ").strip().upper()

    if asset_id == "":
        print("Error: Asset ID cannot be empty!")
        return

    for asset in assets:
        if asset["asset_id"] == asset_id:
            print("Error: Asset ID already exists!")
            return
    device_name = input("Enter Device Name: ").strip()

    if device_name == "":
        print("Error: Device Name cannot be empty!")
        return

    print("\nSelect Asset Category:")
    print("1. Laptop")
    print("2. Desktop")
    print("3. Monitor")
    print("4. Printer")
    print("5. Network Equipment")
    print("6. Other")

    category_choice = input("Choose category (1-6): ")

    if category_choice == "1":
        category = "Laptop"
    elif category_choice == "2":
        category = "Desktop"
    elif category_choice == "3":
        category = "Monitor"
    elif category_choice == "4":
        category = "Printer"
    elif category_choice == "5":
        category = "Network Equipment"
    elif category_choice == "6":
        category = "Other"
    else:
        print("Invalid category selection!")
        return

    brand = input("Enter Brand: ").strip()
    if brand == "":
        print("Error: Brand cannot be empty!")
        return

    print("\nSelect Asset Status:")
    print("1. Available")
    print("2. In Use")
    print("3. Under Maintenance")
    print("4. Retired")

    status_choice = input("Choose status (1-4): ")

    if status_choice == "1":
        status = "Available"
    elif status_choice == "2":
        status = "In Use"
    elif status_choice == "3":
        status = "Under Maintenance"
    elif status_choice == "4":
        status = "Retired"
    else:
        print("Invalid status selection!")
        return
    if status == "":
        print("Error: Status cannot be empty!")
        return

    new_asset = {
        "asset_id": asset_id,
        "device_name": device_name,
        "category": category,
        "brand": brand,
        "status": status,
        "assigned_to": "Unassigned"
    }

    assets.append(new_asset)
    save_assets()

    print("\nAsset registered successfully!")


def view_assets():
    print("\n--- REGISTERED ASSETS ---")

    if len(assets) == 0:
        print("No assets registered yet.")
    else:
        for asset in assets:
            print("--------------------------")
            print("Asset ID:", asset["asset_id"])
            print("Device:", asset["device_name"])
            print("Category:", asset.get("category", "Not specified"))
            print("Brand:", asset["brand"])
            print("Assigned To:", asset.get("assigned_to", "Unassigned"))
            print("Status:", asset["status"])

        print("--------------------------")
        print("Total Assets:", len(assets))


def export_assets():
    print("\n--- EXPORT ASSETS ---")

    if len(assets) == 0:
        print("No assets available to export.")
        return

    with open("assets_export.csv", "w", newline="") as file:
        fieldnames = [
            "asset_id",
            "device_name",
            "category",
            "brand",
            "status",
            "assigned_to"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(assets)

    print("Assets exported successfully!")
    print("File name: assets_export.csv")


def main():
    while True:
        print("\n==========================")
        print("IT ASSET MANAGEMENT SYSTEM")
        print("==========================")
        print("1. Register New Asset")
        print("2. View All Assets")
        print("3. Search Asset")
        print("4. Update Asset")
        print("5. Delete Asset")
        print("6. Filter Assets by Category")
        print("7. Assign Asset to Employee")
        print("8. Unassign / Return Asset")
        print("9. Asset Summary")
        print("10. Export Assets to CSV")
        print("11. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register_asset()
        elif choice == "2":
            view_assets()
        elif choice == "3":
            search_id = input("Enter Asset ID to search: ")
            search_asset(assets, search_id)
        elif choice == "4":
            update_id = input("Enter Asset ID to update: ")

            print("\nSelect New Status:")
            print("1. Available")
            print("2. In Use")
            print("3. Under Maintenance")
            print("4. Retired")

            status_choice = input("Choose status (1-4): ")

            employee = ""

            if status_choice == "2":
                employee = input("Enter employee name: ")

            update_asset(
                assets,
                update_id,
                status_choice,
                save_assets,
                employee
            )
        elif choice == "5":
            delete_id = input("Enter Asset ID to delete: ")
            confirm = input(
                "Are you sure you want to delete? (yes/no): "
            )
            delete_asset(assets, delete_id, confirm, save_assets)
        elif choice == "6":
            category = input("Enter category: ")
            filter_assets(assets, category)
        elif choice == "7":
            asset_id = input("Enter Asset ID: ")
            employee = input("Enter employee name: ")
            assign_asset(assets, asset_id, employee, save_assets)
        elif choice == "8":
            asset_id == input("Enter Asset ID: ")
            unassign_asset(assets, asset_id, save_assets)
        elif choice == "9":
            asset_summary(assets)
        elif choice == "10":
            export_assets()
        elif choice == "11":
            print("Thank you for using ITAMS!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
