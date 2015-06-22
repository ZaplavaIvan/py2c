#pragma once

#include <cmath>
using namespace std;

class Vector3
{
private:
public:

	float x;
	float y;
	float z;

	Vector3()
	{
	}

	Vector3(float x, float y, float z) : x(x), y(y), z(z)
	{
	}

	float length() const
	{
		return sqrt(x*x + y*y + z*z);
	}

	float lengthSquared() const
	{
		return dot(*this);
	}

	void normalise()
	{
		float length = Vector3::length();

		if(length)
		{
			float invLength = 1/length;

			x *= invLength;
			y *= invLength;
			z *= invLength;
		}
	}

	Vector3 getNormalized() const
	{
		float length = Vector3::length();

		if(length)
		{
			float invLength = 1/length;

			return Vector3(x*invLength, y*invLength, z*invLength);
		}

		return *this;
	}

	float dot(const Vector3 &v) const
	{
		return x*v.x + y*v.y + z*v.z;
	}

	Vector3 cross(const Vector3 &v) const
	{
		return Vector3(y*v.z - z*v.y, z*v.x - x*v.z, x*v.y - y*v.x);
	}

	float angle(const Vector3 &v) const
	{
		float angle = dot(v)/(length()*v.length());
		return (angle > 1 || angle < -1) ? 0 : acos(angle);
	}

    Vector3 projectOntoPlane( const Vector3 & vPlaneNorm ) const
    {
        const Vector3& v2 = vPlaneNorm;
        return *this - v2 * ( this->dot( v2 ) / v2.lengthSquared() );
    }

	Vector3 operator+(const Vector3 &v) const
	{
		return Vector3(x + v.x, y + v.y, z + v.z);
	}

	void operator+=(const Vector3 &v)
	{
		x += v.x;
		y += v.y;
		z += v.z;
	}

	Vector3 operator-(const Vector3 &v) const
	{
		return Vector3(x - v.x, y - v.y, z - v.z);
	}

	void operator-=(const Vector3 &v)
	{
		x -= v.x;
		y -= v.y;
		z -= v.z;
	}

	void operator*=(float value)
	{
		x *= value;
		y *= value;
		z *= value;
	}

	Vector3 operator*(float value) const
	{
		return Vector3(x*value, y*value, z*value);
	}

	friend Vector3 operator*(float value, const Vector3 &v)
	{
		return v*value;
	}

	void operator/=(float value)
	{
		float k = 1/value;

		x *= k;
		y *= k;
		z *= k;
	}

	Vector3 operator/(float value) const
	{
		float k = 1/value;

		return Vector3(x*k, y*k, z*k);
	}

	Vector3 operator-() const
	{
		return Vector3(-x, -y, -z);
	}

	void setZero()
	{
		x = 0;
		y = 0;
		z = 0;
	}

	static Vector3 zero()
	{
		return Vector3(0, 0, 0);
	}
};