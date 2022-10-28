from pendulum import DoublePendulum


class World:
    def __init__(self, pendulums: list[DoublePendulum]):
        self.pendulums = pendulums

    def update(self):
        for p in self.pendulums:
            p.update()
