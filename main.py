import time
from sender import Sender
from receiver import Receiver

def run_once(total_packets, loss_rate, ack_loss_rate, resend_delay):
    sender = Sender(total_packets)
    receiver = Receiver(loss_rate, ack_loss_rate)

    sender.generate_packets()
    print(f"\n📦 Generated {sender.total_packets} packets.\n")

    packet_stats = {}
    overall_start = time.perf_counter()

    for packet_id, data in sender.packets.items():
        attempts = 0
        packet_data_sent = 0
        packet_start = time.perf_counter()

        while True:
            attempts += 1
            packet_data_sent += len(data)

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
                    print(f" ❌ (ACK lost)")
                    time.sleep(resend_delay)
                    print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

            else:
                print(f" ❌ (packet lost)")
                time.sleep(resend_delay)
                print(f"🔁 Resending {packet_id} ..........>", end="", flush=True)

        packet_time = time.perf_counter() - packet_start
        packet_stats[packet_id] = {
            "attempts": attempts,
            "time": packet_time,
            "data_sent": packet_data_sent,
            "acks_sent": attempts
        }

    overall_time = time.perf_counter() - overall_start

    total_attempts = sum(s["attempts"] for s in packet_stats.values())
    total_data_sent = sum(s["data_sent"] for s in packet_stats.values())
    extra_data = total_data_sent - total_packets * 3  # 3 numbers per packet

    print("\n" + "=" * 60)
    print("📊 Transmission Summary Report")
    print("=" * 60)
    print(f"Total transmission time: {overall_time:.2f} s")
    print(f"Average time per packet: {overall_time/total_packets:.3f} s")
    print(f"Total attempts (including resends): {total_attempts}")
    print(f"Average attempts per packet: {total_attempts/total_packets:.2f}")
    print(f"Total data sent (units): {total_data_sent}")
    print(f"Extra data (units) due to resends: {extra_data}")
    print(f"Total ACK messages sent: {total_attempts}")  # 1 ACK per attempt

    print("\nReceiver summary:")
    receiver.summary()
    print("=" * 60)

    lost_packets = len(receiver.lost_packets)
    return {
        "time": overall_time,
        "lost": lost_packets,
        "extra_data": extra_data
    }


def main():
    try:
        runs = int(input("🔁 How many times to run the simulation? (1–20): ").strip())
        if not 1 <= runs <= 20:
            print("⚠️ Please enter a number between 1 and 20.")
            return
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return

    total_packets = 50
    loss_rate = 0.05
    ack_loss_rate = 0.05
    resend_delay = 0.5

    all_results = []

    for i in range(1, runs + 1):
        print(f"\n--- Run {i} ---")
        result = run_once(total_packets, loss_rate, ack_loss_rate, resend_delay)
        all_results.append(result)
        print(f"✅ Run {i} finished | Lost packets: {result['lost']} | Extra data due to resends: {result['extra_data']} | Time: {result['time']:.2f}s")

    if runs > 1:
        avg_lost = sum(r["lost"] for r in all_results) / runs
        max_lost = max(all_results, key=lambda x: x["lost"])
        min_lost = min(all_results, key=lambda x: x["lost"])
        avg_extra = sum(r["extra_data"] for r in all_results) / runs
        max_extra = max(all_results, key=lambda x: x["extra_data"])
        min_extra = min(all_results, key=lambda x: x["extra_data"])

        print("\n" + "=" * 60)
        print("📊 Multi-run Summary Report")
        print("=" * 60)
        print(f"Total runs: {runs}")
        print(f"Average lost packets: {avg_lost:.2f}")
        print(f"Run with most lost packets: {max_lost['lost']}")
        print(f"Run with least lost packets: {min_lost['lost']}")
        print(f"Average extra data (units) due to resends: {avg_extra:.2f}")
        print(f"Run with most extra data due to resends: {max_extra['extra_data']}")
        print(f"Run with least extra data due to resends: {min_extra['extra_data']}")
        print("=" * 60)


if __name__ == "__main__":
    main()