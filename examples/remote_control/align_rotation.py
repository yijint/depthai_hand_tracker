import numpy as np

# define params
niter = 10
internalCamWidth = 1152
internalCamHeight = 648

# iterate through random roll, x, and y coordinates to assess
# the error range of the rotation and normalization techniques 
# note that floating point errors can introduce minor mismatches
errors = []
for i in range(niter):
    # get random roll and (x, y) for building fistVec
    rand_roll = np.random.uniform(0, 2*np.pi) # CCW angle
    rand_x = np.random.uniform(-internalCamWidth, internalCamWidth)
    rand_y = np.random.uniform(internalCamHeight, internalCamHeight)

    # prevent errors with zero vectors 
    while (rand_x-internalCamWidth/2 == 0 and internalCamHeight/2-rand_y ==0):
        rand_x = np.random.uniform(-internalCamWidth, internalCamWidth)
        rand_y = np.random.uniform(internalCamHeight, internalCamHeight)

    # center and normalize vector for ease of computation 
    fistVec = [rand_x-internalCamWidth/2, 
               internalCamHeight/2-rand_y]
    fistVec = fistVec/np.linalg.norm(fistVec)

    # rotate fistVec to align with roll 
    c, s = np.round(np.cos(rand_roll),12), np.round(np.sin(rand_roll),12)
    rotation_matrix = [[c,-s], [s,c]]
    fistVec_rotated = rotation_matrix @ fistVec 

    # evaluate method 
    angle_diff = np.arccos(np.clip(np.dot(fistVec, fistVec_rotated), -1.0, 1.0))
    angle_error = rand_roll - angle_diff
    errors.append(angle_error)

    # print values for debugging:
    print(f"before: {fistVec}\nroll: {rand_roll}\nrotation_matrix: {rotation_matrix}\nrotated: {fistVec_rotated}\ndifferences: {angle_error}\nrounded differences: {np.round(np.abs(angle_error),5)}\nsuccess: {np.round(np.abs(angle_error),5)==0}\n------------------------------------------------------")

# evaluate overall error
print(f"OVERALL ERROR PER ROTATION: {np.degrees(np.array(errors).mean())} degrees")

# get random roll and (x, y) for building fistVec
rand_roll = np.pi/4 # CCW angle

# center and normalize vector for ease of computation 
fistVec = [1,0]
fistVec = fistVec/np.linalg.norm(fistVec)

# rotate fistVec to align with roll 
c, s = np.round(np.cos(rand_roll),12), np.round(np.sin(rand_roll),12)
rotation_matrix = [[c,-s], [s,c]]
fistVec_rotated = rotation_matrix @ fistVec 

# evaluate method 
angle_diff = np.arccos(np.clip(np.dot(fistVec, fistVec_rotated), -1.0, 1.0))
angle_error = rand_roll - angle_diff
errors.append(angle_error)

# print values for debugging:
print(f"before: {fistVec}\nroll: {rand_roll}\nrotation_matrix: {rotation_matrix}\nrotated: {fistVec_rotated}\ndifferences: {angle_error}\nrounded differences: {np.round(np.abs(angle_error),5)}\nsuccess: {np.round(np.abs(angle_error),5)==0}\n------------------------------------------------------")
