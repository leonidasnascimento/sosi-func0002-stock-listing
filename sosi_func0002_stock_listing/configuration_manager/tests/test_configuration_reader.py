import unittest
from configuration_manager.reader import reader

class test_configuration_reader(unittest.TestCase):
    def test_should_read_configuration_successfully(self):
        json_path = "configuration_manager\\tests\\test.configreader.settings.json"
        config_reader = reader(json_path, "real_value")
        val = config_reader.get_value("web_site_name", None)
        self.assertEqual(str(val).lower(), "sosi-ms001-stockmktlisting")

if __name__ == "__main__":
    unittest.main()