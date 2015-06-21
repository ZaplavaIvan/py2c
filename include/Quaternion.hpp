#include <cmath>
using namespace std;

class Quaternion
{
private:
public:

	float x;
	float y;
	float z;
	float w;

	Quaternion()
	{
	}

	Quaternion(float x, float y, float z, float w) : x(x), y(y), z(z), w(w)
	{
	}

	void set(float x, float y, float z, float w)
	{
		this->x = x;
		this->y = y;
		this->z = z;
		this->w = w;
	}

	Vector3 rotateVec(const Vector3 &v) const
	{
		float ww = w*w;
		float xx = x*x;
		float yy = y*y;
		float zz = z*z;
		float wx = w*x;
		float wy = w*y;
		float wz = w*z;
		float xy = x*y;
		float xz = x*z;
		float yz = y*z;

		return Vector3(
			ww*v.x + xx*v.x - yy*v.x - zz*v.x + 2*((xy - wz)*v.y + (xz + wy)*v.z),
			ww*v.y - xx*v.y + yy*v.y - zz*v.y + 2*((xy + wz)*v.x + (yz - wx)*v.z),
			ww*v.z - xx*v.z - yy*v.z + zz*v.z + 2*((xz - wy)*v.x + (yz + wx)*v.y));
	}

	void fromAngleAxis(float angle, const Vector3 &axis)
	{
		float theta = angle * 0.5f;
		float sinTheta = sin(theta);

		Vector3 v = axis;
		v.normalise();
		v *= sinTheta;

		x = v.x;
		y = v.y;
		z = v.z;
		w = cos(theta);
	}

};
