import numpy as np
import matplotlib.pyplot as plt

# define params
niter = 60
internalCamWidth = 1152
internalCamHeight = 648

# define function that rotates a 2D vector theta radians CCW about the origin
def rotate(vector, theta_radians):
    vec = vector.copy()
    c = np.cos(theta_radians)
    s = np.sin(theta_radians)
    rotation_matrix = np.array([[c, -s],
                                [s, c]])
    return rotation_matrix @ vector

# find the CCW angle from fistVec to fistVec_rotated
def find_angle(fistVec_rotated, fistVec):
    # # calculate angle 
    # dot_prod = np.dot(a, b)
    # mag_a = np.linalg.norm(a)
    # mag_b = np.linalg.norm(b)
    # cos_theta = dot_prod / (mag_a * mag_b)
    # theta = np.arccos(cos_theta)

    # # the above calculations only find the smaller angle which can be the CW angle
    # # we only want to CCW angle, so add pi to the angle if we find that 
    # # the two vectors are in opposite quadrants 
    # # a_angle_from_X_axis = np.arctan2(a[1], a[0]) # the signed angle with the x-axis
    # # b_angle_from_X_axis = np.arctan2(b[1], b[0])
    # # if (np.sign(a_angle_from_X_axis) != np.sign(b_angle_from_X_axis)):
    # #     theta = np.pi + theta

    # calculate CCW angle 
    angle = np.arctan2(fistVec_rotated[1], fistVec_rotated[0]) - np.arctan2(fistVec[1], fistVec[0])
    if (angle < 0): angle += 2 * np.pi 

    return angle 

# iterate through random roll, x, and y coordinates to assess
# the error range of the rotation and normalization techniques 
# note that floating point errors can introduce minor mismatches
errors = []
success_rate = []
success_rolls = []
fail_rolls = []

for i in range(niter):
    # get random roll and (x, y) for building fistVec
    rand_roll = np.random.uniform(0, np.pi) # CCW angle in radians
    rand_x = np.random.uniform(-internalCamWidth, internalCamWidth)
    rand_y = np.random.uniform(internalCamHeight, internalCamHeight)

    # prevent errors with zero vectors 
    while (rand_x-internalCamWidth/2 == 0 and internalCamHeight/2-rand_y ==0):
        rand_x = np.random.uniform(-internalCamWidth, internalCamWidth)
        rand_y = np.random.uniform(internalCamHeight, internalCamHeight)

    # center and normalize vector for ease of computation 
    fistVec = np.array([rand_x-internalCamWidth/2, 
                        internalCamHeight/2-rand_y])
    fistVec = fistVec/np.linalg.norm(fistVec)

    # rotate fistVec to align with roll 
    fistVec_rotated = rotate(fistVec, rand_roll)

    # evaluate method 
    angle_diff = find_angle(fistVec_rotated, fistVec)
    angle_error = rand_roll - angle_diff
    rounded_diff = np.round(np.abs(angle_error),5)
    is_success = rounded_diff==0
    errors.append(angle_error)
    success_rate.append(is_success)
    if is_success: success_rolls.append(rand_roll)
    else: fail_rolls.append(rand_roll)

    # print values for debugging:
    print(f"before: {fistVec}\nroll: {np.degrees(rand_roll)} degrees\nrotated: {fistVec_rotated}\nangle: {np.degrees(angle_diff)} degrees\nangle error: {np.degrees(angle_error)} degree\nsuccess: {is_success}\n------------------------------------------------------")

# print accuracy rates
print(f"AVERAGE ERROR: {np.degrees(np.array(errors).mean())} degrees\nSUCCESS RATE: {np.round(np.array(success_rate).mean(),1)*100}%")

# # print performance stats for debugging
# print("Printing performance stats...")
# plt.hist(success_rolls, color = 'g', label="successful", alpha=0.3)
# plt.hist(fail_rolls, color = 'r', label="failed", alpha=0.3)
# plt.title("successful vs failed roll values")
# plt.xlabel("roll values")
# plt.ylabel("count")
# plt.legend()
# plt.show()