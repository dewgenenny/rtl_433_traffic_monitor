# tests/test_tpms_filter.py
import pytest
from traffic_monitor.tpms_filter import TPMSFilter

def test_filter_tpms_message():
    # Example TPMS and non-TPMS messages
    tpms_message = {"type": "TPMS", "id": "f15e3929", "pressure_PSI": 32.25, "temperature_C": 23.0}
    non_tpms_message = {"type": "Other", "id": "12345678"}

    # Test TPMS message filtering
    assert TPMSFilter.is_tpms_message(tpms_message) == True
    assert TPMSFilter.is_tpms_message(non_tpms_message) == False

def test_extract_tpms_data():
    tpms_message = {"type": "TPMS", "id": "f15e3929", "pressure_PSI": 32.25, "temperature_C": 23.0}
    extracted_data = TPMSFilter.extract_data(tpms_message)
    expected_data = {"id": "f15e3929", "pressure": "32.25 PSI", "temperature_C": 23.0}
    assert extracted_data == expected_data, f"Expected: {expected_data}, but got: {extracted_data}"


def test_extract_tpms_data_with_psi_pressure():
    tpms_message_psi = {"type": "TPMS", "id": "f15e3929", "pressure_PSI": 32.25, "temperature_C": 23.0}
    extracted_data_psi = TPMSFilter.extract_data(tpms_message_psi)
    expected_data = {"id": "f15e3929", "pressure": "32.25 PSI", "temperature_C": 23.0}
    assert extracted_data_psi == expected_data, f"Expected: {expected_data}, but got: {extracted_data_psi}"



def test_extract_tpms_data_with_kpa_pressure():
    # TPMS message with pressure in kPa
    tpms_message_kpa = {"type": "TPMS", "id": "b05755", "pressure_kPa": 219.75, "temperature_C": 21.0}
    extracted_data_kpa = TPMSFilter.extract_data(tpms_message_kpa)
    assert extracted_data_kpa == {"id": "b05755", "pressure": "219.75 kPa", "temperature_C": 21.0}

def test_extract_tpms_data_with_additional_fields():
    tpms_message_additional = {
        "type": "TPMS",
        "id": "31fffb79",
        "pressure_PSI": 35.25,
        "moving": 1,
        "learn": 0,
        "code": "8dc146"
        # ... include other fields if they are handled in your TPMSFilter implementation ...
    }
    extracted_data_additional = TPMSFilter.extract_data(tpms_message_additional)
    expected_data = {
        "id": "31fffb79",
        "pressure": "35.25 PSI",
        "moving": 1,
        "learn": 0,
        "code": "8dc146"
        # ... include other fields if they are handled in your TPMSFilter implementation ...
    }
    assert extracted_data_additional == expected_data, f"Expected: {expected_data}, but got: {extracted_data_additional}"


