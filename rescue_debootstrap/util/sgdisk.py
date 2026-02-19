from rescue_debootstrap.util.command import CMD


class sgdisk:
    def run(self, device: str, options: str) -> None:
        CMD.sh(f"sgdisk {options} {device}")

    def zap_all(self, device: str) -> None:
        self.run("--zap-all", device)


SGDISK = sgdisk()
