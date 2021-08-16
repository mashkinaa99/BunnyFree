from black_database import BlackDataBase


class RecordingDataBase:

    def __init__(self, names: list, test: str):
        self.names = names
        self.test = test

    def recording_base(self):
        black = BlackDataBase('black_database.db', 'blacktable')
        for name in self.names:
            black.recording(name, self.test)
            black.commit()
