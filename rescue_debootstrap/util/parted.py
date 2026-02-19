from rescue_debootstrap.util.command import CMD


class parted:
    def run(self, device: str, command: str, options: str) -> None:
        CMD.sh(f"parted {device} -s {command} {options}")

    def mklabel(
        self,
        device: str,
        label: str = "gpt",
    ) -> None:
        PARTED.run(device, "mklabel", label)

    def mkpart(
        self,
        device: str,
        type: str,
        start: int,
        end: int,
        unit: str = "s",
    ) -> None:
        self.run(device, "mkpart", f"primary {type} {start}{unit} {end}{unit}")

    def name(
        self,
        device: str,
        number: str,
        name: str,
    ) -> None:
        self.run(device, "name", f"{number} {name}")

    def set_esp(self, device: str, number: int) -> None:
        self.run(device, "set", f"{number} esp on")


PARTED = parted()
