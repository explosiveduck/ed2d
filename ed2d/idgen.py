class IdGenerator(object):
    def __init__(self):
        self.reusableIDs = []
        self.allocatedIds = 0
        self.idIncrement = 0

    def gen_id(self):

        self.allocatedIds += 1
        if self.reusableIDs:
            uid = self.reusableIDs.pop(0)
        else:
            self.idIncrement += 1
            uid = self.idIncrement

        return uid

    def del_id(self, uid):
        self.allocatedIds -= 1
        self.reusableIDs.append(uid)