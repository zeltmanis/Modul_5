import random
import time

class Sender:
    def __init__(self, total_packets=200, timeout=0.5):
        self.total_packets = total_packets
        self.packets = {}          # packet_id -> data
        self.acknowledged = []     # list of acknowledged packet IDs
        self.lost = []             # list of lost packet IDs
        self.timeout = timeout     # time to wait before resending

    def generate_packets(self):
        """Create packets with random numeric data."""
        for i in range(1, self.total_packets + 1):
            packet_id = f"S{i}"
            data = [random.randint(1, 10) for _ in range(3)]
            self.packets[packet_id] = data

    # def show_packets(self, count=5):
    #     """Print a few sample packets to verify generation."""
    #     print(f"Showing {count} of {len(self.packets)} packets:")
    #     for i, (pid, data) in enumerate(self.packets.items()):
    #         print(pid, ":", data)
    #         if i + 1 >= count:
    #             break

    def send_packets(self, receiver):
        """Send all packets to receiver using stop-and-wait logic."""
        previous_ack = None

        for packet_id, data in self.packets.items():
            while True:
                # Send packet
                print(f"Sender ({packet_id}) ---> Receiver", end="", flush=True)
                time.sleep(0.05)  # simulate network delay

                received = receiver.receive_packet(packet_id, data)

                if received:
                    ack = receiver.get_acknowledgment(packet_id)
                    time.sleep(0.02)  # simulate ACK travel time

                    if ack:
                        print(f" ✅")
                        print(f"Sender <--- {ack} Receiver")
                        self.acknowledged.append(packet_id)
                        previous_ack = ack
                        break  # move to next packet
                    else:
                        # ACK lost
                        print(f" ❌ (ACK lost)")
                        if previous_ack:
                            print(f"Sender <--- {previous_ack} Receiver (delayed)")
                        time.sleep(self.timeout)
                        print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

                else:
                    # Packet lost
                    print(f" ❌ (packet lost)")
                    self.lost.append(packet_id)
                    if previous_ack:
                        print(f"Sender <--- {previous_ack} Receiver (delayed)")
                    time.sleep(self.timeout)
                    print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)
