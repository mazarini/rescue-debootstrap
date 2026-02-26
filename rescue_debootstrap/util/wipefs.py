from rescue_debootstrap.util.command import CMD


class wipefs:
    def run(self, device: str, options: str) -> None:
        CMD.sh(f"wipefs {options} {device}")

    def all(self, device: str) -> None:
        self.run("--all", device)


WIPEFS = wipefs()
