from math import sin, cos

import math
import operator

class Quaternion(object):
    
    def __init__(self, *args):
        if len(args) == 0:
            self.__x = self.__y = self.__z = self.__w = 0.
        elif len(args) == 1:
            if isinstance(args[0], (Quaternion, Vector4)):
                self.__x = args[0].x
                self.__y = args[0].y
                self.__z = args[0].z
                self.__w = args[0].w
            else:
                self.__raiseTypeError(args)
        elif len(args) == 4:
            self.__x, self.__y, self.__z, self.__w = map(float, args)
        else:
            self.__raiseTypeError(args)
    
    def __raiseTypeError(self, args):
        raise TypeError("Quaternion({0}) not found".format(", ".join(map(lambda x : x.__class__.__name__, args))))
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def z(self):
        return self.__z
    
    @property
    def w(self):
        return self.__w
    
    def mulLeft(self, q):
        
        x1 = q.x
        y1 = q.y
        z1 = q.z
        w1 = q.w
        
        x2 = self.__x
        y2 = self.__y
        z2 = self.__z
        w2 = self.__w
        
        self.__w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        self.__x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        self.__y = w1*y2 + y1*w2 - x1*z2 + z1*x2
        self.__z = w1*z2 + z1*w2 + x1*y2 - y1*x2
    
    def fromEuler(self, roll, pitch, yaw):
        
        self.fromAngleAxis(roll, Vector3(0, 0, 1))
        
        qPitch = Quaternion()
        qPitch.fromAngleAxis(pitch, Vector3(1, 0, 0))
        self.mulLeft(qPitch)
        
        qYaw = Quaternion()
        qYaw.fromAngleAxis(yaw, Vector3(0, 1, 0))
        self.mulLeft(qYaw)
    
    def fromAngleAxis(self, angle, axis):
        theta = angle*0.5
        sinTheta = sin(theta)
        x, y, z = axis.getNormalized()
        self.__x = x*sinTheta
        self.__y = y*sinTheta
        self.__z = z*sinTheta
        self.__w = cos(theta)
    
    def rotateVec(self, v):
        ww = self.__w*self.__w
        xx = self.__x*self.__x
        yy = self.__y*self.__y
        zz = self.__z*self.__z
        wx = self.__w*self.__x
        wy = self.__w*self.__y
        wz = self.__w*self.__z
        xy = self.__x*self.__y
        xz = self.__x*self.__z
        yz = self.__y*self.__z
        return Vector3(
            ww*v.x + xx*v.x - yy*v.x - zz*v.x + 2*((xy - wz)*v.y + (xz + wy)*v.z),
            ww*v.y - xx*v.y + yy*v.y - zz*v.y + 2*((xy + wz)*v.x + (yz - wx)*v.z),
            ww*v.z - xx*v.z - yy*v.z + zz*v.z + 2*((xz - wy)*v.x + (yz + wx)*v.y))
    
    @property
    def lengthSquared(self):
        ww = self.__w*self.__w
        xx = self.__x*self.__x
        yy = self.__y*self.__y
        zz = self.__z*self.__z
        return xx + yy + zz + ww
    
    def invert(self):
        oodivisor = 1./self.lengthSquared
        self.__x *= -oodivisor
        self.__y *= -oodivisor
        self.__z *= -oodivisor
        self.__w *= oodivisor
    
    def toVec4(self):
        return Vector4(self.__x, self.__y, self.__z, self.__w)
    
    def getAxisX(self):
        ww = self.__w*self.__w
        xx = self.__x*self.__x
        yy = self.__y*self.__y
        zz = self.__z*self.__z
        wy = self.__w*self.__y
        wz = self.__w*self.__z
        xy = self.__x*self.__y
        xz = self.__x*self.__z
        return Vector3(ww + xx - yy - zz, 2*(xy + wz), 2*(xz - wy))
    
    def getAxisY(self):
        ww = self.__w*self.__w
        xx = self.__x*self.__x
        yy = self.__y*self.__y
        zz = self.__z*self.__z
        wx = self.__w*self.__x
        wz = self.__w*self.__z
        xy = self.__x*self.__y
        yz = self.__y*self.__z
        return Vector3(2*(xy - wz), ww - xx + yy - zz, 2*(yz + wx))
    
    def getAxisZ(self):
        ww = self.__w*self.__w
        xx = self.__x*self.__x
        yy = self.__y*self.__y
        zz = self.__z*self.__z
        wx = self.__w*self.__x
        wy = self.__w*self.__y
        xz = self.__x*self.__z
        yz = self.__y*self.__z
        return Vector3(2*(xz + wy), 2*(yz - wx), ww - xx - yy + zz)
    
    def dot(self, q):
        return self.__x*q.__x + self.__y*q.__y + self.__z*q.__z + self.__w*q.__w
    
    def slerp(self, qStart, qEnd, t):
        cosTheta = qStart.dot(qEnd)
        invert = False
        
        if cosTheta < 0:
            cosTheta = -cosTheta
            invert = True
        
        t2 = 1 - t
        
        if 1 - cosTheta > 0:
            theta = math.acos(clamp(-1, cosTheta, 1))
            t2  = sin(theta*t2)/sin(theta)
            t = sin(theta*t)/sin(theta)
        
        if invert:
            t = -t
        
        qs = Vector4(qStart.x, qStart.y, qStart.z, qStart.w)
        qe = Vector4(qEnd.x, qEnd.y, qEnd.z, qEnd.w)
        
        self.__x, self.__y, self.__z, self.__w = qs*t2 + qe*t
    
    def mul(self, q):
        return Quaternion(
            self.__w*q.__x + self.__x*q.__w + self.__y*q.__z - self.__z*q.__y, 
            self.__w*q.__y + self.__y*q.__w - self.__x*q.__z + self.__z*q.__x, 
            self.__w*q.__z + self.__z*q.__w + self.__x*q.__y - self.__y*q.__x, 
            self.__w*q.__w - self.__x*q.__x - self.__y*q.__y - self.__z*q.__z)
    
    @property
    def length(self):
        return math.sqrt(self.lengthSquared)
    
    def normalise(self):
        invLength = 1/self.length
        self.__x *= invLength
        self.__y *= invLength
        self.__z *= invLength
        self.__w *= invLength
    
    def getYaw(self):
        return math.atan2(2*(self.__w*self.__y + self.__x*self.__z), 1 - 2*(self.__x*self.__x + self.__y*self.__y))
    
    def getPitch(self):
        return math.asin(clamp(-1, 2*(self.__w*self.__x - self.__y*self.__z), 1))
    
    def getRoll(self):
        return math.atan2(2*(self.__x*self.__y + self.__w*self.__z), 1 - 2*(self.__x*self.__x + self.__z*self.__z))

    def angle(self, q):
        """
        :type q: Quaternion
        :rtype: float
        """
        return 0


class Vector3(list):
   
    def __init__(self, *args):
        if len(args) == 0:
            self.extend((0.,)*3)
        elif len(args) == 1:
            if isinstance(args[0], (Vector3, tuple, list)):
                self.extend(map(float, args[0]))
            else:
                self.__raiseTypeError(args)
        elif len(args) == 3:
            self.extend(map(float, args))
        else:
            self.__raiseTypeError(args)
    
    def __raiseTypeError(self, args):
        raise TypeError("Vector3({0}) not found".format(", ".join(map(lambda x : x.__class__.__name__, args))))
    
    def set(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vector3):
                self.x, self.y, self.z = args[0]
            else:
                self.__setRaiseTypeError(args)
        elif len(args) == 3:
            self.x, self.y, self.z = map(float, args)
        else:
            self.__setRaiseTypeError(args)
                
    def __setRaiseTypeError(self, args):
        raise TypeError("Vector3.set({0}) not found".format(", ".join(map(lambda x : x.__class__.__name__, args))))
    
    def __iadd__(self, v):
        self.x, self.y, self.z = map(operator.add, self, v)
        return self
    
    def __add__(self, v):
        return Vector3(*map(operator.add, self, v))
    
    def __sub__(self, v):
        return Vector3(*map(operator.sub, self, v))
    
    def __mul__(self, arg):
        if isinstance(arg, Vector3):
            return self.cross(arg)
        return Vector3(*map(float(arg).__mul__, self))
    
    def __rmul__(self, k):
        return self*k
    
    def __imul__(self, k):
        self.x, self.y, self.z = map(float(k).__mul__, self)
        return self
    
    def __div__(self, k):
        return Vector3(*map((k and 1./k or 1.).__mul__, self))
    
    def __neg__(self):
        return Vector3(*map(operator.neg, self))
    
    @property
    def x(self):
        return self[0]
    
    @x.setter
    def x(self, x):
        self[0] = x
    
    @property
    def y(self):
        return self[1]
    
    @y.setter
    def y(self, y):
        self[1] = y
    
    @property
    def z(self):
        return self[2]
    
    @z.setter
    def z(self, z):
        self[2] = z
    
    def tuple(self):
        return tuple(self)
     
    def list(self):
        return list(self)
    
    @property
    def length(self):
        return math.sqrt(self.lengthSquared)
    
    @property
    def lengthSquared(self):
        return sum(map(operator.mul, self, self))
    
    def distTo(self, v2):
        return math.sqrt(sum(map(lambda k1, k2: (k1-k2)**2, v2, self)))
    
    def getNormalized(self):
        length = self.length
        invLength = 1./length if length else 0.
        return Vector3(*map(invLength.__mul__, self))
    
    def normalise(self):
        length = self.length
        self *= 1./length if length else 0.
    
    def dot(self, v):
        return sum(map(operator.mul, self, v))
    
    def cross(self, v):
        """
        :type v: Vector3
        :rtype: Vector3
        """
        return Vector3(self.y*v.z - self.z*v.y, self.z*v.x - self.x*v.z, self.x*v.y - self.y*v.x)
    
    def angle(self, v):
        """
        :type v: Vector3
        :rtype: float
        """
        angle = self.dot(v)/(self.length*v.length)
        return (angle > 1 or angle < -1) and 0. or math.acos(angle)

    def projectOntoPlane(self, v):
        """
        :type v: Vector3
        :rtype: float
        """
        return Vector3()


class Matrix(list):
    
    def __init__(self):
        for _ in xrange(4):
            self.append([0]*4)
        self[3][3] = 1
    
    def setScale(self, param):
        pass
    
    def setTranslate(self, param):
        self[3][:3] = param
    
    def getTranslate(self):
        return Vector3(*self[3][:3])
    
    def applyToOrigin(self):
        return self.translation
    
    translation = property(getTranslate, setTranslate)
    
    @property
    def yaw(self):
        zdir = Vector3(*self[2][:3])
        zdir.normalise()
        return math.atan2(zdir.x, zdir.z)
    
    @property
    def pitch(self):
        zdir = Vector3(*self[2][:3])
        zdir.normalise()
        return -math.asin(zdir.y)
    
    @property
    def roll(self):
        xdir = Vector3(*self[0][:3])
        zdir = Vector3(*self[2][:3])
        xdir.normalise()
        zdir.normalise()
        
        zdirxzlen = math.sqrt(zdir.z*zdir.z + zdir.x*zdir.x)
        acarg = (zdir.z*xdir.x - zdir.x*xdir.z)/zdirxzlen
        if acarg <= -1.0: return math.pi
        if not zdirxzlen or acarg >= 1: return 0
        
        roll = math.acos(acarg)
        
        return -roll if xdir.y < 0 else roll
    
    def lookAt(self, position, direction, up):
        position = Vector3(position)
        direction = Vector3(direction)
        up = Vector3(up)
        
        direction.normalise()
        
        right = up.cross(direction)
        right.normalise()
        
        up = direction.cross(right)
        
        self[0][0] = right.x
        self[1][0] = right.y
        self[2][0] = right.z
        self[3][0] = 0
        
        self[0][1] = up.x
        self[1][1] = up.y
        self[2][1] = up.z
        self[3][1] = 0
        
        self[0][2] = direction.x
        self[1][2] = direction.y
        self[2][2] = direction.z
        self[3][2] = 0
        
        self[0][3] = -position.dot(right)
        self[1][3] = -position.dot(up)
        self[2][3] = -position.dot(direction)
        self[3][3] = 1
    
    def getDeterminant(self):
        det = 0
        
        det += self[0][0]*(self[1][1]*self[2][2] - self[1][2]*self[2][1])
        det -= self[0][1]*(self[1][0]*self[2][2] - self[1][2]*self[2][0])
        det += self[0][2]*(self[1][0]*self[2][1] - self[1][1]*self[2][0])
    
        return det
    
    def invert(self):
        
        det = self.getDeterminant()
        
        if not det:
            ERROR_MSG("Matrix::invert: Attempted to invert a matrix with zero determinant\n")
            return False
        
        rcp = 1./det
        
        tmp = []
        for i in range(4):
            tmp.append([])
            for j in range(4):
                tmp[i].append(self[i][j])
        
        self[0][0] = tmp[1][1]*tmp[2][2] - tmp[1][2]*tmp[2][1]
        self[0][1] = tmp[0][2]*tmp[2][1] - tmp[0][1]*tmp[2][2]
        self[0][2] = tmp[0][1]*tmp[1][2] - tmp[0][2]*tmp[1][1]
        self[1][0] = tmp[1][2]*tmp[2][0] - tmp[1][0]*tmp[2][2]
        self[1][1] = tmp[0][0]*tmp[2][2] - tmp[0][2]*tmp[2][0]
        self[1][2] = tmp[0][2]*tmp[1][0] - tmp[0][0]*tmp[1][2]
        self[2][0] = tmp[1][0]*tmp[2][1] - tmp[1][1]*tmp[2][0]
        self[2][1] = tmp[0][1]*tmp[2][0] - tmp[0][0]*tmp[2][1]
        self[2][2] = tmp[0][0]*tmp[1][1] - tmp[0][1]*tmp[1][0]
        
        self[0][0] *= rcp
        self[0][1] *= rcp
        self[0][2] *= rcp
        
        self[1][0] *= rcp
        self[1][1] *= rcp
        self[1][2] *= rcp
        
        self[2][0] *= rcp
        self[2][1] *= rcp
        self[2][2] *= rcp
        
        self[3][0] = -(tmp[3][0]*self[0][0] + tmp[3][1]*self[1][0] + tmp[3][2]*self[2][0])
        self[3][1] = -(tmp[3][0]*self[0][1] + tmp[3][1]*self[1][1] + tmp[3][2]*self[2][1])
        self[3][2] = -(tmp[3][0]*self[0][2] + tmp[3][1]*self[1][2] + tmp[3][2]*self[2][2])
        
        return True

if __name__ == '__main__':
    a = Vector3(0, 0, 0)
    b = Quaternion(0, 0, 0, 0)
    c = Matrix()