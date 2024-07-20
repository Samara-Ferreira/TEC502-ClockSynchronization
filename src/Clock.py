

class Clock:
    def __init__(self):
        self.time: int = 0
        self.drift: float = 1
        self.sync_drift: int = 0

    # Método para incrementar o tempo
    def tick(self) -> None:
        # Quando chegar no tempo limite de 24 horas, reinicia o relógio
        if self.time == 86400:
            self.time = 0
        else:
            self.time += 1

    # Método para mudar o tempo
    def set_time(self, new_time: int) -> None:
        self.time = new_time

    # Método para mudar o drift
    def set_drift(self, new_drift: int) -> None:
        self.drift = new_drift

    # Método para mudar o drift da sincronização
    def set_sync_drift(self, new_sync_drift: int) -> None:
        self.sync_drift = new_sync_drift

    # Método para retornar o tempo
    def get_time(self) -> int:
        return self.time

    # Método para converter o tempo de segundos para horas, minutos e segundos
    def convert_time(self) -> str:
        hours = self.time // 3600
        minutes = (self.time % 3600) // 60
        seconds = self.time % 60
        return f"{hours}:{minutes}:{seconds}"
