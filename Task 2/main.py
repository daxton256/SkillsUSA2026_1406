from collections import deque

def simulate_seating(n, arr):
    # build queue as (original_index, preferred_seat)
    queue = deque(enumerate(arr))
    
    occupied = set()
    result = [0] * n
    
    while queue:
        person, seat = queue.popleft()
        
        if seat not in occupied:
            occupied.add(seat)
            result[person] = seat
        else:
            queue.append((person, seat + 1))  # try next seat
    
    return result

print("Task 2 - Seating Arrangement Simulation")

n = int(input("Number of people: "))
arr = list(map(int, input("Preferred seats (space-separated): ").split()))
final_seating = simulate_seating(n, arr)

print("Final seating arrangement (person index: seat number):")
for i, seat in enumerate(final_seating):
    print(f"Person {i}: Seat {seat}")