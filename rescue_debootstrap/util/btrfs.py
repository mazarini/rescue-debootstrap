from rescue_debootstrap.model.btrfs_group import BtrfsGroup
from rescue_debootstrap.model.btrfs_node import BtrfsNode
from rescue_debootstrap.model.partition_registry import REGISTRY
from rescue_debootstrap.util.command import CMD
from rescue_debootstrap.util.config_util import CONFIG
from rescue_debootstrap.util.mount import MOUNT
from rescue_debootstrap.util.umount import UMOUNT


class BtrfsUtil:
    def create_fs(self, label: str, raid: str, devices: str):
        CMD.sh(
            f'mkfs.btrfs -f -L "{label}" {raid} --csum xxhash64 --nodesize 32768 {devices}'
        )

    def create_btrfs_groups(self, groups: list[BtrfsGroup]):
        print(f"\nCreating {len(groups)} btrfs groups...")
        for group in groups:
            self.mkfs(group)
            print(
                f"Mounting group {group.label} to create {len(group.tree)} volumes..."
            )
            MOUNT.device(REGISTRY.get(group.label), CONFIG.host.mountpoint)

            for volume in group.tree:
                self.mk_volume(group.label, volume)
            UMOUNT.all()

    def mkfs(self, group: BtrfsGroup):
        devices = ""
        for device in group.devices:
            print(f"Adding device {device.label} to group {group.label}")
            devices += " " + REGISTRY.get(device.label)
        print(
            f"Creating btrfs filesystem for group {group.label} with devices: {devices}"
        )
        type = "" if len(devices) == 1 else f"-m {group.type} -d {group.type}"
        self.create_fs(group.label, type, devices)
        REGISTRY.add(group.label, REGISTRY.get(group.devices[0].label))

    def mk_volume(self, label: str, volume: BtrfsNode):
        if volume.type == "path":
            CMD.sh(f"mkdir -p {CONFIG.host.mountpoint}/{volume.name}")
        else:
            CMD.sh(f"btrfs subvolume create {CONFIG.host.mountpoint}/{volume.name}")
            REGISTRY.add(volume.name, REGISTRY.get(label))


BTRFS = BtrfsUtil()
