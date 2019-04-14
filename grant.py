from card import GrantCard


class Grant:
    def __init__(self, card: GrantCard, flower):
        self.card = card
        self.flower = flower

    def reduce(self):
        self.flower -= 1

    def __str__(self):
        return '{}: {}'.format(self.card.name, self.flower)
