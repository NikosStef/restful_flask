import sys
class Note(object):
    def __init__(self, id, context, archived, ownerEmail):
        self.id = id
        self.context = context
        self.archived = archived,
        self.ownerEmail = ownerEmail

    def set_id(self, id):
        setattr(self, 'id', id)

    def to_dict(self):
        note = {
            'id' : self.id,
            'context' : self.context,
            'archived' : self.archived,
            'ownerEmail' : self.ownerEmail
        }
        return note

    @classmethod
    def from_dict(cls, data):
        if 'id' in data:
            note = cls(data['id'], data['context'], data['archived'][0], data['ownerEmail'])
            return note
        else:
            print(data['archived'], file=sys.stderr)
            return cls(None, data['context'], data['archived'], data['ownerEmail'])

    @classmethod
    def from_tuple(cls, data):
        return cls(*data)


class User(object):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def set_id(self, id):
        setattr(self, 'id', id)

    def to_dict(self):
        user = {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'email' : self.email
        }
        return user

    @classmethod
    def from_dict(cls, data):
        if 'id' in data:
            user = cls(data['id'], data['username'], data['password'], data['email'])
            return user
        else:
            return cls(None, data['username'], data['password'], data['email'])


    @classmethod
    def from_tuple(cls, data):
        return cls(*data)
