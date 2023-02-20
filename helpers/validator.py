import re

class Validator():
    def __init__(self, value):
        self.__value = value.strip()
        self.errors = []

    def not_empty(self):
        if (self.__value):
            return self
        self.errors.append('Требуется указать значение')
        return self
    
    def min_length(self, number):
        if (len(self.__value) > number):
            return self
        self.errors.append(f'Значение должно быть больше {str(number)} символов')
        return self
    
    def max_length(self, number):
        if (len(self.__value) < number):
            return self
        self.errors.append(f'Значение должно быть меньше {str(number)} символов')
        return self

    def valid_login(self):
        if (re.search(r'^[\da-z_\s]+$', self.__value, re.I or re.M)):
            return self
        self.errors.append('Логин должно содержать только буквы, цифры, пробел или «_»')
        return self

    def valid_password(self):
        if (re.search(r'^[\da-z_&$*]+$', self.__value, re.I or re.M)):
            return self
        self.errors.append('Пароль должен содержать только буквы, цифры, «_», «&», «$» или «*»')
        return self

    def valid_characters(self):
        if (re.search(r'^[\da-zа-яё\s]+$', self.__value, re.I or re.M)):
            return self
        self.errors.append('Значение должно содержать только буквы, цифры или пробел')
        return self
