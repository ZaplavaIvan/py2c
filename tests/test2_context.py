import Math


def register_types():
    return [('Vector3', (Math.Vector3, 'Vector3', ['vector3.hpp'])),
            ('Quaternion', (Math.Quaternion, 'Quaternion', ['quaternion.hpp']))]