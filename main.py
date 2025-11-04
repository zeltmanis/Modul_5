import time
from sender import Sender
from receiver import Receiver

def main():
    total_packets = 50
    loss_rate = 0.05
    ack_loss_rate = 0.1   # 10% chance ack is lost
    resend_delay = 0.5

    sender = Sender(total_packets)
    receiver = Receiver(loss_rate, ack_loss_rate)

    sender.generate_packets()
    print(f"\n📦 Generated {sender.total_packets} packets.\n")

    previous_ack = None

    for packet_id, data in sender.packets.items():
        while True:  # keep sending until ack received
            # Sender sends packet
            print(f"\nSender ({packet_id}) ---> Receiver", end="", flush=True)
            time.sleep(0.05)

            received = receiver.receive_packet(packet_id, data)

            if received:
                ack = receiver.get_acknowledgment(packet_id)
                time.sleep(0.02)
                if ack:
                    print(f" ✅")
                    print(f"    Sender <--- {ack} Receiver")  # indented for readability
                    sender.acknowledged.append(packet_id)
                    previous_ack = ack
                    break  # move to next packet
                else:
                    print(f" ❌ (ack lost)")
                    if previous_ack:
                        print(f"    Sender <--- {previous_ack} Receiver (delayed)")
                    time.sleep(resend_delay)
                    print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)
            else:
                print(f" ❌ (packet lost)")
                if previous_ack:
                    print(f"    Sender <--- {previous_ack} Receiver (delayed)")
                time.sleep(resend_delay)
                print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

        # Optional: print a small separator every 5 packets
        if int(packet_id[1:]) % 1 == 0:
            print("\n" + "-" * 50)

    # Summary
    print("\n📊 Transmission Summary")
    print(f"Packets sent: {sender.total_packets}")
    print(f"Acknowledged: {len(sender.acknowledged)}")
    print(f"Lost: {len(sender.lost)}")

    reliability = len(sender.acknowledged) / sender.total_packets
    print(f"Overall reliability: {reliability:.2%}\n")

    print("Receiver summary:")
    receiver.summary()


if __name__ == "__main__":
    main()