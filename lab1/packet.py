class Packet:
    def __init__(self, generated_tick: int):
        self.generated_tick = generated_tick
        self.served_tick = 0
