import math
import Math


def register_types():
    return [('Vector3', (Math.Vector3, 'Vector3', ['Vector3.hpp'])),
            ('Quaternion', (Math.Quaternion, 'Quaternion', ['Quaternion.hpp'])),
            ('math', (math, 'simplemath', ['simplemath.hpp'])),]