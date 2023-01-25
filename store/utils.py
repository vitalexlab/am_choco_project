LIST_ALLOWED_CODES = {
    '+7': 'ru',
    '+380': 'ua',
    '+375': {'by': [29, 44, 33, 25]}
}


class ValidatePhone:

    def __init__(self, phone_number: str):
        self.region_operators = []
        self.phone = phone_number

    def _validate_operator(self, operator: str) -> bool:
        return int(operator) in self.region_operators

    def _validate_number(self) -> bool:
        number = self.phone[6:]
        return len(number) == 7 and number.isdigit()

    def _validate_phone_by(self, phone_operator):
        return self._validate_operator(
            phone_operator
        ) and self._validate_number()

    def _validate_phone_ru(self, phone_operator):
        return phone_operator.startswith('9') and self._validate_number()

    def _validate_phone_ua(self, phone_operator):
        return phone_operator.startswith('0') and self._validate_number()

    def validate(self):
        state = ''
        for code in LIST_ALLOWED_CODES.keys():
            if not self.phone.startswith(code):
                continue
            else:
                state = LIST_ALLOWED_CODES.get(code)
                break
        if not state:
            return False
        else:
            phone_operator = self.phone[4:6]
            if state.get('by'):
                list_operators = state.get('by')
                self.region_operators = list_operators
                return self._validate_phone_by(phone_operator)
            elif state.get('ru'):
                return self._validate_phone_ru(phone_operator)
            elif state.get('ua'):
                return self._validate_phone_ua(phone_operator)


if __name__ == '__main__':
     number = '+375296217433'
     val = ValidatePhone(number)
     print(val.validate())
