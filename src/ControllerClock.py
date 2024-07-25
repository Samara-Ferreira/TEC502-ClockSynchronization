"""Módulo para controlar o relógio."""

from time import sleep, perf_counter
from Clock import Clock
from threading import Thread


class ControllerClock:
    def __init__(self) -> None:
        """Construtor da classe ControllerClock."""

        self.clock: Clock = Clock()
        self.is_sync: bool = False
        self.dict_clocks: dict = {}
        Thread(target=self.count_clock).start()

    def count_clock(self) -> None:
        """Método para incrementar o relógio."""

        while True:
            if not self.is_sync:
                sleep(self.clock.drift)
            if not self.is_sync:
                self.clock.tick()
                print("Horário atual:", self.clock.convert_time())

    def precise_sleep(self, duration):
        """Método para fazer um sleep preciso."""
        start = perf_counter()
        while (perf_counter() - start) < duration:
            pass

    def sync_clock(self, final_time: int) -> None:
        """Método para sincronizar o relógio."""

        print("Sincronizando relógio...")
        print("| Tempo Final: ", final_time, " e drift de sincronização: ", self.clock.sync_drift, "\n")

        while self.clock.time < final_time and self.is_sync:
            print("Horário atual sincronizando: ", self.clock.time)
            # sleep(self.clock.sync_drift)
            self.precise_sleep(self.clock.sync_drift)
            self.clock.tick()

        print("\nRelógio sincronizado!\n")
        print("Horário atual: ", self.clock.time)
        self.is_sync = False

    def get_time(self) -> int:
        """Método para retornar o horário atual."""

        self.is_sync = True
        return self.clock.get_time()

    def set_is_sync(self) -> None:
        """Método para mudar a flag de sincronização."""

        self.is_sync = False
