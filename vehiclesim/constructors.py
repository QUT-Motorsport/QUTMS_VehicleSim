from vehiclesim import *
import pickle


def plotMassLapSim(mat_file, crv_name, window_w, window_h, g, m, P, p, A, Cd, mu, Cl):
    offset, crv_array, array_length, x_array, start_position, end_position, offset, crv = fetch_data(mat_file, crv_name)
    lat_velocity, peak_loc = lateral_velocity(g, m, P, p, A, Cd, mu, Cl, array_length, crv_array)
    accel_velocity, accel_a_long, accel_a_lat = acceleration(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length)
    brake_velocity, brake_a_long, brake_a_lat = braking(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length)
    velocity = calculate_velocity(accel_velocity, brake_velocity)

    fastest_lap = lap_time(velocity, x_array)
    max_speed = calculate_max_speed(velocity)
    min_speed = calculate_min_speed(velocity)

    a_lat, a_long = lat_long(accel_a_lat, accel_a_long, brake_a_lat, brake_a_long, accel_velocity, velocity, crv)

    graph_html, fig_all = plot_MassLap_all_html(window_w, window_h, x_array, crv, velocity, a_lat, a_long)

    #pickle the 'image' to be called later to download
    pickle.dump(fig_all, open("graph_all.p", "wb"))

    return graph_html, fastest_lap, min_speed, max_speed

def plotMassGG(mat_file, crv_name, window_w, window_h, g, m, P, p, A, Cd, mu, Cl):
    offset, crv_array, array_length, x_array, start_position, end_position, offset, crv = fetch_data(mat_file, crv_name)
    lat_velocity, peak_loc = lateral_velocity(g, m, P, p, A, Cd, mu, Cl, array_length, crv_array)
    accel_velocity, accel_a_long, accel_a_lat = acceleration(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length)
    brake_velocity, brake_a_long, brake_a_lat = braking(g, m, P, p, A, Cd, mu, Cl, peak_loc, x_array, lat_velocity, crv_array, start_position, end_position, offset, array_length)
    velocity = calculate_velocity(accel_velocity, brake_velocity)

    fastest_lap = lap_time(velocity, x_array)
    max_speed = calculate_max_speed(velocity)
    min_speed = calculate_min_speed(velocity)

    a_lat, a_long = lat_long(accel_a_lat, accel_a_long, brake_a_lat, brake_a_long, accel_velocity, velocity, crv)

    graph_html, fig_gg = plot_MassLap_gg_html(window_w, window_h, x_array, crv, velocity, a_lat, a_long)

    #pickle the 'image' to be called later to download
    pickle.dump(fig_gg, open("graph_gg.p", "wb"))

    return graph_html, fastest_lap, min_speed, max_speed