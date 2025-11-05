import time
from sender import Sender
from receiver import Receiver

def main():
    total_packets = 50
    loss_rate = 0.05
    ack_loss_rate = 0.05
    resend_delay = 0.5

    sender = Sender(total_packets)
    receiver = Receiver(loss_rate, ack_loss_rate)

    sender.generate_packets()
    print(f"\n📦 Generated {sender.total_packets} packets.\n")

    packet_stats = {}  # track per-packet statistics
    overall_start = time.perf_counter()

    for packet_id, data in sender.packets.items():
        attempts = 0
        packet_data_sent = 0
        packet_start = time.perf_counter()

        while True:
            attempts += 1
            packet_data_sent += len(data)

            # Send packet
            print(f"Sender ({packet_id}) ---> Receiver", end="", flush=True)
            time.sleep(0.05)

            received = receiver.receive_packet(packet_id, data)

            if received:
                ack = receiver.get_acknowledgment(packet_id)
                time.sleep(0.02)

                if ack:
                    print(f" ✅")
                    print(f"    Sender <--- {ack} Receiver")
                    sender.acknowledged.append(packet_id)
                    break
                else:
                    # ACK lost
                    print(f" ❌ (ACK lost)")
                    time.sleep(resend_delay)
                    print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

            else:
                # Packet lost
                print(f" ❌ (packet lost)")
                time.sleep(resend_delay)
                print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

        # Record per-packet stats
        packet_time = time.perf_counter() - packet_start
        packet_stats[packet_id] = {
            "attempts": attempts,
            "time": packet_time,
            "data_sent": packet_data_sent,
            "acks_sent": attempts
        }

    overall_time = time.perf_counter() - overall_start

    # --- Summary Report ---
    print("\n" + "=" * 60)
    print("📊 Transmission Summary Report")
    print("=" * 60)

    total_attempts = sum(s["attempts"] for s in packet_stats.values())
    total_data_sent = sum(s["data_sent"] for s in packet_stats.values())
    total_acks = sum(s["acks_sent"] for s in packet_stats.values())
    extra_data = total_data_sent - total_packets * 3  # 3 numbers per packet

   # print(f"Total packets: {total_packets}")
   # print(f"Packets acknowledged: {len(sender.acknowledged)}")
   # print(f"Overall reliability: {len(sender.acknowledged)/total_packets:.2%}")
    print(f"Total transmission time: {overall_time:.2f} s")
    print(f"Average time per packet: {overall_time/total_packets:.3f} s")
    print(f"Total attempts (including resends): {total_attempts}")
    print(f"Average attempts per packet: {total_attempts/total_packets:.2f}")
    print(f"Total data sent (units): {total_data_sent}")
    print(f"Extra data (units) due to resends: {extra_data}")
    print(f"Total ACK messages sent: {total_acks}")

    print("\nReceiver summary:")
    receiver.summary()
    print("=" * 60)


if __name__ == "__main__":
    main()
