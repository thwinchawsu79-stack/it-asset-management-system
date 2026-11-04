def is_asset_assigned(asset):
    employee = asset.get("assigned_to", "Unassigned")
    return employee != "Unassigned"


def assign_asset(assets, asset_id, employee, save_assets):
    print("\n--- ASSIGN ASSET ---")

    asset_id = asset_id.strip().upper()
    employee = employee.strip()

    for asset in assets:
        if asset["asset_id"] == asset_id:

            print("Device:", asset.get("device_name", "Not specified"))
            print("Current Status:", asset["status"])
            print("Current Assignment:",
                  asset.get("assigned_to", "Unassigned"))

            if asset["status"] != "Available":
                print("Cannot assign this asset!")
                print("Only available assets can be assigned.")
                return False

            if employee == "":
                print("Error: Employee name cannot be empty!")
                return False

            asset["assigned_to"] = employee
            asset["status"] = "In Use"

            save_assets()

            print("Asset assigned successfully!")
            return True

    print("Asset not found.")
    return False


def unassign_asset(assets, asset_id, save_assets):
    print("\n--- UNASSIGN ASSET ---")

    asset_id = asset_id.strip().upper()

    for asset in assets:
        if asset["asset_id"] == asset_id:

            current_employee = asset.get("assigned_to", "Unassigned")

            print("Currently Assigned To:", current_employee)

            if current_employee == "Unassigned":
                print("This asset is not assigned to anyone.")
                return False

            asset["assigned_to"] = "Unassigned"
            asset["status"] = "Available"

            save_assets()

            print("Asset returned successfully!")
            return True

    print("Asset not found.")
    return False


def asset_summary(assets):
    print("\n--- ASSET SUMMARY ---")

    total_assets = len(assets)
    available = 0
    in_use = 0
    maintenance = 0
    retired = 0

    for asset in assets:
        if asset["status"] == "Available":
            available += 1
        elif asset["status"] == "In Use":
            in_use += 1
        elif asset["status"] == "Under Maintenance":
            maintenance += 1
        elif asset["status"] == "Retired":
            retired += 1

    print("Total Assets:", total_assets)
    print("Available:", available)
    print("In Use:", in_use)
    print("Under Maintenance:", maintenance)
    print("Retired:", retired)

    return {
        "total": total_assets,
        "available": available,
        "in_use": in_use,
        "maintenance": maintenance,
        "retired": retired
    }


def filter_assets(assets, category):
    print("\n--- FILTER ASSETS BY CATEGORY ---")

    category = category.strip()

    filtered_assets = []

    for asset in assets:
        if asset.get("category", "").lower() == category.lower():
            print("--------------------------")
            print("Asset ID:", asset["asset_id"])
            print("Device:", asset.get("device_name", "Not specified"))
            print("Category:", asset.get("category", "Not specified"))
            print("Brand:", asset.get("brand", "Not specified"))
            print("Status:", asset.get("status", "Not specified"))

            filtered_assets.append(asset)

    if not filtered_assets:
        print("No assets found in this category.")

    return filtered_assets


def search_asset(assets, search_id):
    print("\n--- SEARCH ASSET ---")

    search_id = search_id.strip().upper()
    found = False

    for asset in assets:
        if asset["asset_id"] == search_id:
            print("\nAsset Found!")
            print("Asset ID:", asset["asset_id"])
            print("Device:", asset["device_name"])
            print("Category:", asset.get("category", "Not specified"))
            print("Brand:", asset["brand"])
            print("Status:", asset["status"])
            found = True
            break

    if not found:
        print("\nAsset not found.")


def delete_asset(assets, delete_id, confirm, save_assets):
    print("\n--- DELETE ASSET ---")

    delete_id = delete_id.strip().upper()
    confirm = confirm.strip().lower()

    for asset in assets:
        if asset["asset_id"] == delete_id:
            print("Asset:", asset["device_name"])

            if confirm == "yes":
                assets.remove(asset)
                save_assets()
                print("\nAsset deleted successfully!")
            else:
                print("\nDeletion cancelled.")

            return True

    print("\nAsset not found.")
    return False


def update_asset(assets, update_id, status_choice, save_assets, employee=""):
    print("\n--- UPDATE ASSET ---")

    update_id = update_id.strip().upper()
    employee = employee.strip()

    for asset in assets:
        if asset["asset_id"] == update_id:

            print("Current Status:", asset["status"])
            print("Current Assignment:",
                  asset.get("assigned_to", "Unassigned"))

            current_employee = asset.get("assigned_to", "Unassigned")

            if status_choice == "1":
                if is_asset_assigned(asset):
                    print("This asset is assigned to:", current_employee)
                    print("Please return the asset before changing its status.")
                    return False

                new_status = "Available"

            elif status_choice == "2":
                if current_employee != "Unassigned":
                    print("This asset is already assigned to:", current_employee)
                    print("Please return the asset before assigning it again.")
                    return False

                if employee == "":
                    print("Employee name cannot be empty!")
                    return False

                asset["assigned_to"] = employee
                new_status = "In Use"

            elif status_choice == "3":
                if current_employee != "Unassigned":
                    print("This asset is assigned to:", current_employee)
                    print("Please return the asset first.")
                    return False

                new_status = "Under Maintenance"
                asset["assigned_to"] = "Unassigned"

            elif status_choice == "4":
                if current_employee != "Unassigned":
                    print("This asset is assigned to:", current_employee)
                    print("Please return the asset first.")
                    return False

                new_status = "Retired"
                asset["assigned_to"] = "Unassigned"

            else:
                print("Invalid status selection!")
                return False

            if new_status == "Available":
                asset["assigned_to"] = "Unassigned"

            asset["status"] = new_status
            save_assets()

            print("\nAsset updated successfully!")
            print("New Status:", asset["status"])
            print("New Assignment:", asset["assigned_to"])

            return True

    print("\nAsset not found.")
    return False
