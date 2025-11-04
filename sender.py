import random

class Sender:
    def __init__(self, total_packets=200):
        self.total_packets = total_packets
        self.packets = {}          # store packet_id -> data
        self.sent_count = 0
        self.acknowledged = []
        self.lost = []

    def generate_packets(self):
        """Create packets with random numeric data."""
        for i in range(1, self.total_packets + 1):
            packet_id = f"S{i}"
            data = [random.randint(1, 10) for _ in range(3)]  # random 3 numbers
            self.packets[packet_id] = data

    def show_packets(self, count=5):
        """Print a few sample packets to verify generation."""
        print(f"Showing {count} of {len(self.packets)} packets:")
        for i, (pid, data) in enumerate(self.packets.items()):
            print(pid, ":", data)
            if i + 1 >= count:
                break