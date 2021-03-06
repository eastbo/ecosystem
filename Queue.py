class queue:
    def __init__(self):
        self.q = []

    def add(self, item):
        self.q.insert(0, item)

    def get_q(self):
        return self.q

    def de_q(self):
        try:
            return self.q.pop()
        except IndexError as e:
            return None

    def get_last(self):
        return self.q[-1]

    def set(self, ls):
        self.q = ls

if __name__ == '__main__':
    q = queue()
