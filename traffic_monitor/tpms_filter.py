# traffic_monitor/tpms_filter.py

class TPMSFilter:
    @staticmethod
    def is_tpms_message(message):
        """
        Check if the given message is a TPMS message.
        :param message: dict
        :return: bool
        """
        return message.get("type") == "TPMS"


    @staticmethod
    def extract_data(message):
        if TPMSFilter.is_tpms_message(message):
            extracted_data = {}

            # Only include keys that exist in the message
            for key in ['id', 'model', 'time', 'temperature_C']:
                if key in message:
                    extracted_data[key] = message[key]


            # Handle temperature in various units
            if "temperature_C" in message:
                extracted_data["temperature"] = message["temperature_C"]
            elif "temperature_F" in message:
                # Convert Fahrenheit to Celsius
                extracted_data["temperature"] = (message["temperature_F"] - 32) * 5 / 9
            elif "temperature_K" in message:
                # Convert Kelvin to Celsius
                extracted_data["temperature"] = message["temperature_K"] - 273.15


            # Handle pressure
            if "pressure_PSI" in message:
                extracted_data["pressure"] = f"{message['pressure_PSI']} PSI"
            elif "pressure_kPa" in message:
                extracted_data["pressure"] = f"{message['pressure_kPa']} kPa"

            # Handle additional fields
            additional_fields = ['moving', 'learn', 'code', 'flags']
            for field in additional_fields:
                if field in message:
                    extracted_data[field] = message[field]

            return extracted_data
        return {}
