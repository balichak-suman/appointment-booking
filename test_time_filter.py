from datetime import datetime

# Test filtering past times
current_time = datetime.now()
print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M')}")
print()

# Simulate available slots
all_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00"]
current_time_str = current_time.strftime("%H:%M")

print(f"All slots: {all_slots}")
print(f"Current time: {current_time_str}")
print()

# Filter past slots
future_slots = [slot for slot in all_slots if slot > current_time_str]
print(f"Available slots (future only): {future_slots}")
print(f"Filtered out {len(all_slots) - len(future_slots)} past slots")
