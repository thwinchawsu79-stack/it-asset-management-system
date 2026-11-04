from unittest.mock import patch

import unittest
import main


class TestITAMS(unittest.TestCase):

    def test_asset_data(self):
        asset = {
            "asset_id": "LAP001",
            "device_name": "Dell Latitude",
            "category": "Laptop",
            "brand": "Dell",
            "status": "Available",
            "assigned_to": "Unassigned"
        }

        self.assertEqual(asset["asset_id"], "LAP001")
        self.assertEqual(asset["category"], "Laptop")
        self.assertEqual(asset["status"], "Available")

    def test_empty_asset_id(self):
        asset = {
            "asset_id": "",
            "device_name": "Dell Latitude",
            "status": "Available"
        }

        self.assertEqual(asset["asset_id"], "")

    def test_asset_status(self):
        valid_statuses = [
            "Available",
            "In Use",
            "Under Maintenance",
            "Retired"
        ]

        asset = {
            "asset_id": "LAP002",
            "status": "Under Maintenance"
        }

        self.assertIn(asset["status"], valid_statuses)

    def test_asset_summary(self):
        original_assets = main.assets

        main.assets = [
            {"asset_id": "LAP001", "status": "Available"},
            {"asset_id": "LAP002", "status": "In Use"},
            {"asset_id": "PRN001", "status": "Under Maintenance"},
            {"asset_id": "LAP003", "status": "Retired"}
        ]

        result = main.asset_summary(main.assets)

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["available"], 1)
        self.assertEqual(result["in_use"], 1)
        self.assertEqual(result["maintenance"], 1)
        self.assertEqual(result["retired"], 1)

        main.assets = original_assets

    def test_filter_assets(self):
        original_assets = main.assets

        main.assets = [
            {"asset_id": "LAP001", "category": "Laptop"},
            {"asset_id": "PRN001", "category": "Printer"},
            {"asset_id": "LAP002", "category": "Laptop"}
        ]

        result = main.filter_assets(main.assets, "Laptop")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["asset_id"], "LAP001")
        self.assertEqual(result[1]["asset_id"], "LAP002")

        main.assets = original_assets

    def test_assign_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]
        with patch("main.save_assets"):
            result = main.assign_asset(
                main.assets,
                "LAP001",
                "Aung Aung",
                main.save_assets
            )

        self.assertTrue(result)
        self.assertEqual(main.assets[0]["assigned_to"], "Aung Aung")
        self.assertEqual(main.assets[0]["status"], "In Use")

        main.assets = original_assets

    def test_unassign_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "In Use",
                "assigned_to": "Alex"
            }
        ]

        with patch("main.save_assets"):
            result = main.unassign_asset(
                main.assets,
                "LAP001",
                main.save_assets
            )

        self.assertTrue(result)
        self.assertEqual(main.assets[0]["status"], "Available")
        self.assertEqual(main.assets[0]["assigned_to"], "Unassigned")

        main.assets = original_assets

    def test_assign_unavailable_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "In Use",
                "assigned_to": "Alex"
            }
        ]

        with patch("main.save_assets"):
            result = main.assign_asset(
                main.assets,
                "LAP001",
                "Mg Mg",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["assigned_to"], "Alex")

        main.assets = original_assets

    def test_assign_empty_employee(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.assign_asset(
                main.assets,
                "LAP001",
                " ",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["status"], "Available")
        self.assertEqual(main.assets[0]["assigned_to"], "Unassigned")

        main.assets = original_assets

    def test_unassign_already_unassigned_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.unassign_asset(
                main.assets,
                "LAP001",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["status"], "Available")
        self.assertEqual(main.assets[0]["assigned_to"], "Unassigned")

        main.assets = original_assets

    def test_search_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "category": "Laptop",
                "brand": "Dell",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("builtins.print") as mock_print:
            main.search_asset(main.assets, "LAP001")

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Asset Found!", printed_text)

        main.assets = original_assets

    def test_search_asset_not_found(self):
        original_assets = main.assets

        main.assets = []

        with patch("builtins.print") as mock_print:
            main.search_asset(main.assets, "XYZ999")

        printed_text = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Asset not found.", printed_text)

        main.assets = original_assets

    def test_delete_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available"
            }
        ]

        with patch("main.save_assets"):
            result = main.delete_asset(
                main.assets,
                "LAP001",
                "yes",
                main.save_assets
            )

        self.assertTrue(result)
        self.assertEqual(len(main.assets), 0)

        main.assets = original_assets

    def test_delete_asset_cancelled(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available"
            }
        ]

        with patch("main.save_assets"):
            result = main.delete_asset(
                main.assets,
                "LAP001",
                "no",
                main.save_assets
            )

        self.assertTrue(result)
        self.assertEqual(len(main.assets), 1)
        self.assertEqual(main.assets[0]["asset_id"], "LAP001")

        main.assets = original_assets

    def test_delete_asset_not_found(self):
        original_assets = main.assets

        main.assets = []

        with patch("main.save_assets"):
            result = main.delete_asset(
                main.assets,
                "XYZ999",
                "yes",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(len(main.assets), 0)

        main.assets = original_assets

    def test_update_asset_status(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.update_asset(
                main.assets,
                "LAP001",
                "3",
                main.save_assets
            )

        self.assertTrue(result)
        self.assertEqual(
            main.assets[0]["status"],
            "Under Maintenance"
        )
        self.assertEqual(
            main.assets[0]["assigned_to"],
            "Unassigned"
        )

        main.assets = original_assets

    def test_update_asset_assign_employee(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.update_asset(
                main.assets,
                "LAP001",
                "2",
                main.save_assets,
                "Aung Aung"
            )

        self.assertTrue(result)
        self.assertEqual(main.assets[0]["status"], "In Use")
        self.assertEqual(main.assets[0]["assigned_to"], "Aung Aung")

        main.assets = original_assets

    def test_update_asset_empty_employee(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.update_asset(
                main.assets,
                "LAP001",
                "2",
                main.save_assets,
                ""
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["status"], "Available")
        self.assertEqual(main.assets[0]["assigned_to"], "Unassigned")

        main.assets = original_assets

    def test_update_assigned_asset(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "In Use",
                "assigned_to": "Aung Aung"
            }
        ]

        with patch("main.save_assets"):
            result = main.update_asset(
                main.assets,
                "LAP001",
                "3",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["status"], "In Use")
        self.assertEqual(main.assets[0]["assigned_to"], "Aung Aung")

        main.assets = original_assets

    def test_update_asset_invalid_status(self):
        original_assets = main.assets

        main.assets = [
            {
                "asset_id": "LAP001",
                "device_name": "Dell Latitude",
                "status": "Available",
                "assigned_to": "Unassigned"
            }
        ]

        with patch("main.save_assets"):
            result = main.update_asset(
                main.assets,
                "LAP001",
                "9",
                main.save_assets
            )

        self.assertFalse(result)
        self.assertEqual(main.assets[0]["status"], "Available")

        main.assets = original_assets


if __name__ == "__main__":
    unittest.main()
