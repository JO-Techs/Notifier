class MockSMSService:
    def __init__(self, from_number: str):
        self.from_number = from_number

    def send_sms(self, to_number, message):
        # Dummmmmmmmmmmmy
        print(f"Mock SMS sent from {self.from_number} to {to_number}: {message}")
        return "mock_message_sid"