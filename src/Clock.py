"""Módulo para a classe Clock."""


class Clock:
    def __init__(self) -> None:
        """Construtor da classe Clock."""

        self.time: int = 0
        self.drift: float = 1.1
        self.sync_drift: int = 0

    def tick(self) -> None:
        """Método para incrementar o tempo."""
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
    def convert_time(self):
        seconds = self.time
        days = seconds // 86_400
        seconds %= 86_400
        hours = seconds // 3_600
        seconds %= 3_600
        minutes = seconds // 60
        seconds %= 60
        return days, f"{hours:02}:{minutes:02}:{seconds:02}"
