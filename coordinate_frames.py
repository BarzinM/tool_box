from numpy import sin, cos, array, dot, pi, sqrt, cross, arccos, insert


# Frame->rotate->translate = frame
#

# quaternion to euler


# euler to quaternion
def generateQuaternion(axis, angle):
    axis = normalize(axis)
    half_angle = angle / 2
    sin_half_angle = sin(half_angle)
    real = cos(half_angle)
    i_part = axis[0] * sin_half_angle
    j_part = axis[1] * sin_half_angle
    k_part = axis[2] * sin_half_angle
    return (real, i_part, j_part, k_part)


def quaternionToAxisAngle(quaternion):
    real, right_quaternion = quaternion[0], quaternion[1:]
    theta = arccos(real) * 2
    return normalize(right_quaternion), theta


# euler rotation
def rotationEuler(point, vector):
    x, y, z = point
    roll, pitch, yaw = vector
    rotation_x = [[1, 0, 0], [0, cos(roll), -sin(roll)], [0, sin(roll), cos(roll)]]
    rotation_y = [[cos(pitch), 0, -sin(pitch)], [0, 1, 0], [sin(pitch), 0, cos(pitch)]]
    rotation_z = [[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]]
    new_point = dot(dot(rotation_x, rotation_y), dot(rotation_z, [x, y, z]))
    return new_point


# quaternion rotation
def rotatationQuaternion(quaternion, point):
    # point = (0.0,)+point
    point = insert(point, 0, 0.0)
    new_vector = productQuaternion(productQuaternion(quaternion, point), conjugateQuaternion(quaternion))
    return new_vector[1:]


# translation
def translate(point, vector):
    x, y, z = point
    u, v, w = vector
    return x + u, y + v, z + w


# quaternion inverse
def inverseQuaternion(quaternion):
    numerator = conjugateQuaternion(quaternion)
    inverse = changeNorm(numerator)
    return inverse


# change magnitude
def changeNorm(quaternion, magnitude=1):
    magnitude = magnitude / norm(quaternion)
    return scale(quaternion, magnitude)


# scale
def scale(quaternion, scale):
    return tuple(value * scale for value in quaternion)


# normalize
def normalize(quaternion, tolerance=0.00001):
    squared_value = squared(quaternion)
    if abs(squared_value - 1) <= tolerance:
        return quaternion
    else:
        return scale(quaternion, 1 / sqrt(squared_value))


# product
def productQuaternion(quaternion_1, quaternion_2):
    a_1, b_1, c_1, d_1 = quaternion_1
    a_2, b_2, c_2, d_2 = quaternion_2
    real = a_1 * a_2 - b_1 * b_2 - c_1 * c_2 - d_1 * d_2
    i_part = a_1 * b_2 + b_1 * a_2 + c_1 * d_2 - d_1 * c_2
    j_part = a_1 * c_2 - b_1 * d_2 + c_1 * a_2 + d_1 * b_2
    k_part = a_1 * d_2 + b_1 * c_2 - c_1 * b_2 + d_1 * a_2
    return (real, i_part, j_part, k_part)


def productQuaternion2(quaternion_1, quaternion_2):
    temp_real = quaternion_1[0] * quaternion_2[0] - dot(quaternion_1[1:], quaternion_2[1:])
    right_quat = quaternion_1[0] * quaternion_2[1:] + quaternion_2[0] * quaternion_1[1:] + cross(quaternion_1[1:], quaternion_2[1:])
    return insert(right_quat, 0, temp_real)


# conjugate quaternion
def conjugateQuaternion(quaternion):
    real, i_part, j_part, k_part = quaternion
    return array([real, -i_part, -j_part, -k_part])


# squared
def squared(numbers):
    return sum(number**2 for number in numbers)


# norm
def norm(numbers):
    return sqrt(squared(numbers))


# Quaternion interpolation
def interpolateQuaternions(quaternion_1, quaternion_2):
    # Spherical Linear intERPolation
    print 'THIS FUNCTION HAS NOT BEEN IMPLEMENTED YET'


if __name__ == "__main__":
    # q_1 = (1, 2, 3, 4)
    # q_2 = (4, 5, 4, 5)
    # print inverseQuaternion(q_1)
    # print productQuaternion(q_1, q_2)
    # # print norm(3, 4)
    # print '=================='
    # print rotatationQuaternion([1, 0, 0], q_1)
    # print '--------------'
    x_axis_unit = (1, 0, 0)
    y_axis_unit = (0, 1, 0)
    z_axis_unit = (0, 0, 1)
    r1 = generateQuaternion(x_axis_unit, pi / 2)
    r2 = generateQuaternion(y_axis_unit, pi / 2)
    r3 = generateQuaternion(z_axis_unit, pi / 2)

    v = rotatationQuaternion(r1, z_axis_unit)
    print v
    v = rotatationQuaternion(r2, v)
    print v
    v = rotatationQuaternion(r3, v)
    print v
    import numpy
    n = 100000
    v = numpy.random.random((n, 3))
    # print v
    # print v[0]
    q = numpy.random.random((n, 4))
    # print q
    import time
    t0 = time.time()
    for i in range(n):
        quaternion = array(q[i])
        vector = array(v[i])
        rotatationQuaternion(quaternion, vector)
    t1 = time.time()
    print 'it took', t1 - t0
