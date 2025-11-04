import random

class Receiver:
    def __init__(self, loss_rate=0.05, ack_loss_rate=0.02):
        """
        :param loss_rate: Probability that a packet is lost.
        :param ack_loss_rate: Probability that an acknowledgment is lost.
        """
        self.loss_rate = loss_rate
        self.ack_loss_rate = ack_loss_rate
        self.received_packets = {}   # store packet_id -> data
        self.lost_packets = []       # keep track of lost packet IDs

    def receive_packet(self, packet_id, data):
        """
        Simulate receiving a packet.
        Returns True if received successfully, False if lost.
        """
        chance = random.random()
        if chance < self.loss_rate:
            self.lost_packets.append(packet_id)
            return False
        else:
            self.received_packets[packet_id] = data
            return True

    def get_acknowledgment(self, packet_id):
        """
        Simulate sending acknowledgment.
        Returns None if ack is lost, otherwise returns ack string.
        """
        if packet_id in self.received_packets:
            chance = random.random()
            if chance < self.ack_loss_rate:
                return None  # Ack lost
            else:
                return f"Ack({packet_id})"
        return None

    def summary(self):
        """
        Print statistics about received and lost packets.
        """
        total = len(self.received_packets) + len(self.lost_packets)
        reliability = len(self.received_packets) / total if total > 0 else 0
        print(f"Total packets processed: {total}")
        print(f"Received: {len(self.received_packets)}")
        print(f"Lost: {len(self.lost_packets)}")
        print(f"Reliability: {reliability:.2%}")
