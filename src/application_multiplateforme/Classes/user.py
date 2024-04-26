class User:
    def __init__(self, user_id, username, idPersonType, encodings):
        self._user_id = user_id
        self._username = username
        self._idPersonType = idPersonType
        self._encodings = encodings

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value 

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value 

    @property
    def idPersonType(self):
        return self._idPersonType

    @idPersonType.setter
    def idPersonType(self, value):
        self._idPersonType = value 

    @property
    def encodings(self):
        return self._encodings

    @encodings.setter
    def encodings(self, value):
        if isinstance(value, list): 
            self._encodings = value
        else:
            raise ValueError("Encodings must be a list")

    def __str__(self):
        return f"User(ID: {self._user_id}, Username: '{self._username}', Type de personne: {self._idPersonType}"
