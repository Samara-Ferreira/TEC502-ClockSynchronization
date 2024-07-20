
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
            sleep(self.clock.drift)
            if not self.is_sync:
                self.clock.tick()
                print("Horário atual:", self.clock.convert_time())

    def sync_clock(self, final_time: int) -> None:
        while self.clock.time < final_time:
            print("Sincronizando relógio... ", self.clock.time)
            print("Sync drift ", self.clock.sync_drift)
            sleep(self.clock.sync_drift)
            self.clock.tick()
        self.is_sync = False

    def get_time(self) -> int:
        self.is_sync = True
        return self.clock.get_time()


