
from Clock import Clock
from time import sleep
from threading import Thread


class ControllerClock:
    def __init__(self) -> None:
        self.clock: Clock = Clock()
        self.is_sync: bool = False
        self.dict_clocks: dict = {}
        Thread(target=self.count_clock).start()

    def count_clock(self) -> None:
        """Método para incrementar o relógio."""
        while True:
            # if self.is_sync:
            #     sleep(self.clock.sync_drift)
            #     if self.clock.sync_drift != 0:
            #         self.clock.tick()

            # else:
            if not self.is_sync:
                sleep(self.clock.drift)
            if not self.is_sync:
                self.clock.tick()
                print("Horário atual:", self.clock.convert_time())

    def sync_clock(self, final_time: int) -> None:
        """Método para sincronizar o relógio."""
        print("Sincronizando relógio...")
        print("Tempo Final: ", final_time, "Drift de sincronização: ",self.clock.sync_drift)
        print("\n")
        while self.clock.time < final_time:
            print("horario Atual Sincronizando: ", self.clock.time)
            sleep(self.clock.sync_drift)
            self.clock.tick()
        print('Relógio sincronizado!!!')
        print("horario Atual: ", self.clock.time)
        self.is_sync = False

    def get_time(self) -> int:
        self.is_sync = True
        return self.clock.get_time()


