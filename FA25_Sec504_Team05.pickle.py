# save_my_design.py
import numpy as np
import pickle

from subfunctions_Phase4 import (
    define_planet,
    define_edl_system,
    define_mission_events,
    define_chassis,
    define_motor,
    define_batt_pack,
    redefine_edl_system,
    simulate_edl,
    simulate_rover,
    get_cost_edl,
)

from define_experiment import experiment1

# ---------------------------------------------------------
# 1. Build planet, edl_system, mission & experiment structs
# ---------------------------------------------------------
planet = define_planet()
edl_system = define_edl_system()
mission_events = define_mission_events()
experiment, end_event = experiment1()

# ---------------------------------------------------------
# 2. Discrete design choices (YOUR TEAM'S FINAL DESIGN)
# ---------------------------------------------------------
edl_system = define_chassis(edl_system, "steel")
edl_system = define_motor(edl_system, "base")
edl_system = define_batt_pack(edl_system, "PbAcid-1", 4)

# ---------------------------------------------------------
# 3. Continuous design variables 
#    x = [D_parachute, R_wheel, m_chassis, d2, m_fuel]
# ---------------------------------------------------------
xbest = np.array([19.0, 0.7, 800.0, 0.09, 250.0])

edl_system["parachute"]["diameter"] = xbest[0]
edl_system["rover"]["wheel_assembly"]["wheel"]["radius"] = xbest[1]
edl_system["rover"]["chassis"]["mass"] = xbest[2]
edl_system["rover"]["wheel_assembly"]["speed_reducer"]["diam_gear"] = xbest[3]
edl_system["rocket"]["fuel_mass"] = xbest[4]
edl_system["rocket"]["initial_fuel_mass"] = xbest[4]

# Reset to standard initial conditions
edl_system = redefine_edl_system(edl_system)

# ---------------------------------------------------------
# 4. Run EDL, then rover simulations
# ---------------------------------------------------------
tmax = 5000
T_edl, Y_edl, edl_system = simulate_edl(edl_system, planet, mission_events, tmax, False)

time_edl = T_edl[-1]
landing_velocity = edl_system["velocity"]

# Rover simulation
edl_system["rover"] = simulate_rover(edl_system["rover"], planet, experiment, end_event)
rover = edl_system["rover"]

time_rover = rover["telemetry"]["completion_time"]
distance_traveled = rover["telemetry"]["distance_traveled"]
avg_vel = rover["telemetry"]["average_velocity"]
energy_per_m = rover["telemetry"]["energy_per_distance"]

total_time = time_edl + time_rover
total_cost = get_cost_edl(edl_system)

# ---------------------------------------------------------
# 5. Print numbers (matches report table)
# ---------------------------------------------------------
print("----------------------------------------")
print("Optimized parachute diameter   = {:.6f} [m]".format(xbest[0]))
print("Optimized fuel mass            = {:.6f} [kg]".format(xbest[4]))
print("Time to complete EDL mission   = {:.6f} [s]".format(time_edl))
print("Rover velocity at landing      = {:.6f} [m/s]".format(landing_velocity))
print("Optimized wheel radius         = {:.6f} [m]".format(xbest[1]))
print("Optimized d2                   = {:.6f} [m]".format(xbest[3]))
print("Optimized chassis mass         = {:.6f} [kg]".format(xbest[2]))
print("Time to complete rover mission = {:.6f} [s]".format(time_rover))
print("Time to complete mission       = {:.6f} [s]".format(total_time))
print("Average velocity               = {:.6f} [m/s]".format(avg_vel))
print("Distance traveled              = {:.6f} [m]".format(distance_traveled))
print("Battery energy per meter       = {:.6f} [J/m]".format(energy_per_m))
print("Total cost                     = {:.6f} [$]".format(total_cost))
print("----------------------------------------")

# ---------------------------------------------------------
# 6. Tag with correct team info & save pickle
# ---------------------------------------------------------
edl_system["team_name"] = "5(3)guys"
edl_system["team_number"] = 5
edl_system["section"] = 504

pickle_filename = "FA25_Sec504_Team05.pickle"

with open(pickle_filename, "wb") as f:
    pickle.dump(edl_system, f)

print(f"Saved design to {pickle_filename}")
print("----------------------------------------")
