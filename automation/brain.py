import time

TICK_TIME_SECONDS = 5


class Brain:

    def __init__(self, database_layer, lights_manager, switches_manager, settings):
        self.database_layer = database_layer
        self.lights_manager = lights_manager
        self.switches_manager = switches_manager
        self.settings = settings

    def control_automation(self):
        self.start_brain()
        print("The home is now running in automation mode.")
        starttime = time.time()
        while True:
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
            self.update()

    def start_brain(self):
        print("Preparing brain")
        self.database_layer.store_lights(self.lights_manager.get_lights())
        self.database_layer.store_switches(self.switches_manager.get_switches())

    def update(self):
        print("Brain is processing data.")
        self.__update_device_states()
        self.__log_data()
        self.__event_based_processing()

    def __update_device_states(self):
        self.lights_manager.update_lights()
        self.switches_manager.update_switches()

    def __log_data(self):
        if self.settings.should_log_data:
            self.database_layer.log_light_states(self.lights_manager.get_lights())

    def __event_based_processing(self):
        self.__process_switch_events()
        self.__process_light_events()

    def __process_light_events(self):
        for light in self.lights_manager.get_lights():
            if light.state_changed():
                print(light.unique_id, " Light changed to ", light.light_state.device_state, " was ", light.last_states[-2].device_state)
                if self.settings.alarm_active:
                    print("Calling the cops, lights should not change states while alarm is active.")

    def __process_switch_events(self):
        for switch in self.switches_manager.get_switches():
            if switch.state_changed():
                print(f"{switch.unique_id} switch state changed to {switch.switch_state.button_event} {switch.switch_state.last_updated} {switch.switch_state.button_pressed} {switch.switch_state.hold}  {switch.switch_state.release}  {switch.switch_state.release_hold}")
                if switch.switch_state.release_hold and switch.switch_state.button_pressed == 4:
                    self.settings.alarm_active = True
                    print("Turning alarm on")
                elif switch.switch_state.release_hold and switch.switch_state.button_pressed == 1:
                    self.settings.alarm_active = False
                    print("Turning alarm off")


