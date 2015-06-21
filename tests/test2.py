import math
from Math import Vector3, Quaternion

def smoothRotation(src, dest, dt, maxSpeed, zeroZone):
    """
    :type src: Vector3
    :type dest: Vector3
    :type dt: float
    :type maxSpeed: float
    :type zeroZone: float
    :rtype: Vector3
    """
    destAngle = src.angle(dest)
    norm = min(1.0, destAngle / zeroZone)
    angle = min(destAngle, maxSpeed * dt * math.sqrt(norm))

    axis = src.cross(dest)
    if destAngle > math.radians(90.0):
        norm = dest - src
        axis = Vector3(0, math.copysign(1, axis.y), 0).projectOntoPlane(norm)
        axis.normalise()
    tempQuat = Quaternion()
    tempQuat.fromAngleAxis(angle, axis)
    return tempQuat.rotateVec(src)