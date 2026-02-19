class PartitionRegistry:
    def __init__(self):
        self.partitions = []

    def add(self, label: str, device: str):
        self.partitions.append({"label": label, "device": device})

    def get(self, label: str) -> str:
        for partition in self.partitions:
            if partition["label"] == label:
                return partition["device"]
        self.print()
        print("\n")
        raise ValueError(f"Partition with label '{label}' not found")

    def print(self):
        print("\nRegistered partitions:")
        for partition in self.partitions:
            print(f"\n  {partition['label']} <=> {partition['device']}")


REGISTRY = PartitionRegistry()
