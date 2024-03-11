
import time
import subprocess
from dronekit import connect, VehicleMode
from pymavlink import mavutil

# Connect to the vehicle
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
vehicle.mode = VehicleMode("GUIDED")

# Define search parameters --> change these according to the tests
search_altitude = 10
search_step = 5
search_radius = 50

def target_detected():
    # get image detection code and put it here
    return True  # Assume target is always detected for this example

# Perform search
search_direction = 1
search_iteration = 0

while True:
    # Calculate search position
    search_position = (search_iteration * search_step) * search_direction

    # Move the drone to the search position
    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_relative_frame.lat + search_position / 111111, vehicle.location.global_relative_frame.lon, search_altitude))

    # Increment search iteration
    search_iteration += 1

    # Check if the target is detected
    if target_detected():
        print("Target detected! Returning to main code...")
        #go to edge_6 code using subprocess
        subprocess.call(['python', 'edge_6.py'])
        break

    # Check if the search radius is reached
    if abs(search_position) >= search_radius:
        # Change search direction and reset search iteration
        search_direction *= -1
        search_iteration = 0
        # Increase altitude for next search iteration
        search_altitude += search_step

    # Add a short delay to avoid overwhelming the system
    time.sleep(1)

# Close connection and terminate
vehicle.close()
exit()