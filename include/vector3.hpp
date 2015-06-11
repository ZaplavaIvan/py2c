#ifndef VECTOR3_HPP
#define VECTOR3_HPP

#include <iostream>

#include <math.h>

inline static float clamp(float min, float val, float max)
{
	return std::max(min, std::min(val, max));
}

inline static bool almostZero(float x, float epsilon)
{
	return std::abs(x) < epsilon;
}

inline static bool isEqual(float a, float b)
{
	return std::abs(std::abs(a) - std::abs(b)) < 0.000001f;
}

class Vector3
{

public:

	float x;
	float y;
	float z;

	Vector3();
	Vector3( float a, float b, float c );	

	void setZero();
	void set( float a, float b, float c );
//	void scale( const Vector3& v, float s );
	void setPitchYaw( float pitchInRadians, float yawInRadians );

	float dotProduct( const Vector3& v ) const;
	void crossProduct( const Vector3& v1, const Vector3& v2 );
	Vector3 crossProduct( const Vector3 & v ) const;
	void lerp( const Vector3 & a, const Vector3 & b, float t );
	void clamp( const Vector3 & lower, const Vector3 & upper );

	void projectOnto( const Vector3& v1, const Vector3& v2 );
	Vector3 projectOnto( const Vector3 & v ) const;
	Vector3 projectOntoPlane( const Vector3 & vPlaneNorm ) const;
	Vector3 mulParallel( const Vector3& v ) const;

	inline float length() const;
	inline float lengthSquared() const;
	inline float distance( const Vector3 & otherPoint ) const;
	inline float distanceSquared( const Vector3 & otherPoint ) const;
	inline float angle(const Vector3& v) const;
	inline float min() const;
	inline float max() const;
	inline unsigned int minIndex() const;
	inline unsigned int maxIndex() const;
	inline float minAbs() const;
	inline float maxAbs() const;
	inline unsigned int minAbsIndex() const;
	inline unsigned int maxAbsIndex() const;

	inline void normalise();
	inline Vector3 getNormalized() const;
	inline Vector3 unitVector() const;
	inline Vector3 square() const;
	inline Vector3 reflect(const Vector3& N) const;
	inline Vector3 refract(const Vector3& N, float eta) const;
	inline Vector3 ortho() const;

	float getAngle( const Vector3 & other ) const;
	inline float getUnitVectorAngle( const Vector3 & other ) const;

	inline void operator += ( const Vector3& v );
	inline void operator -= ( const Vector3& v );
	inline void operator *= ( float s );
	inline void operator /= ( float s );
	inline Vector3 operator-() const;	

	/**
	 *	This method returns the pitch of this vector when it is considered as a
	 *	direction vector.
	 */
	inline float Vector3::pitch() const
	{
		return -atan2f( y, sqrtf( x*x + z*z ) );
	}


	/**
	 *	This method returns the yaw of this vector when it is considered as a
	 *	direction vector.
	 */
	inline float Vector3::yaw() const
	{
		return atan2f( x, z );
	}	

	inline bool almostEqual( const Vector3& v1, const Vector3& v2, const float epsilon = 0.0004f )
	{
		return almostEqual( v1.x, v2.x, epsilon ) &&
			almostEqual( v1.y, v2.y, epsilon ) &&
			almostEqual( v1.z, v2.z, epsilon );
	}	


	static const Vector3 & zero()		{ return ZERO; }

	///Zero vector.
	static const Vector3 ZERO;
	///(1, 0, 0)
	static const Vector3 I;
	///(0, 1, 0)
	static const Vector3 J;
	///(0, 0, 1)
	static const Vector3 K;

private:
	// This is to prevent construction like:
	//	Vector3( 0 );
	// It would interpret this as a float * and later crash.
	Vector3( int value );
};

inline Vector3 operator +( const Vector3& v1, const Vector3& v2 );
inline Vector3 operator -( const Vector3& v1, const Vector3& v2 );
inline Vector3 operator *( const Vector3& v, float s );
inline Vector3 operator *( float s, const Vector3& v );
inline Vector3 operator *( const Vector3& v1, const Vector3& v2 );
inline Vector3 operator /( const Vector3& v, float s );
inline bool operator   ==( const Vector3& v1, const Vector3& v2 );
inline bool operator   !=( const Vector3& v1, const Vector3& v2 );
inline bool operator   < ( const Vector3& v1, const Vector3& v2 );

inline
bool operator   > ( const Vector3& v1, const Vector3& v2 ) { return v2 < v1; }
inline
bool operator   >=( const Vector3& v1, const Vector3& v2 ) { return !(v1<v2); }
inline
bool operator   <=( const Vector3& v1, const Vector3& v2 ) { return !(v2<v1); }

/**
 *	This method adds the input vector to this vector.
 */
inline
void Vector3::operator +=( const Vector3& v )
{
	x += v.x;
	y += v.y;
	z += v.z;
}


/**
 *	This method subtracts the input vector from this vector.
 */
inline
void Vector3::operator -=( const Vector3& v )
{
	x -= v.x;
	y -= v.y;
	z -= v.z;
}


/**
 *	This method scales this vector by the input value.
 */
inline
void Vector3::operator *=( float s )
{
	x *= s;
	y *= s;
	z *= s;
}


/**
 *	This method divides the vector by the input value.
 */
inline
void Vector3::operator /=( float s )
{
	float divisor = 1.f / s;
	x *= divisor;
	y *= divisor;
	z *= divisor;
}

inline
Vector3 Vector3::operator-() const
{
	Vector3 that;
	that.x = -x;
	that.y = -y;
	that.z = -z;
	return that;
}

/**
 *	This function returns the sum of the two input vectors.
 *
 *	@relates Vector3
 */
inline
Vector3 operator +( const Vector3& v1, const Vector3& v2 )
{
	return Vector3( v1.x+v2.x, v1.y+v2.y, v1.z+v2.z );
}


/**
 *	This function returns the result of subtracting v2 from v1.
 *
 *	@relates Vector3
 */
inline
Vector3 operator -( const Vector3& v1, const Vector3& v2 )
{
	return Vector3( v1.x-v2.x, v1.y-v2.y, v1.z-v2.z );
}


/**
 *	This function returns the input vector scaled by the input float.
 *
 *	@relates Vector3
 */
inline
Vector3 operator *( const Vector3& v, float s )
{
//	Vector3 result( v );
//	result *= s;

//	return result;
	return Vector3( v.x * s, v.y * s, v.z * s );
}


/**
 *	This function returns the input vector scaled by the input float.
 *
 *	@relates Vector3
 */
inline
Vector3 operator *( float s, const Vector3& v )
{
	return Vector3( v.x * s, v.y * s, v.z * s );
}


/**
 *	This function returns the input vector scaled down by the input float.
 *
 *	@relates Vector3
 */
inline
Vector3 operator /( const Vector3& v, float s )
{
	float oos = 1.f / s;
	return Vector3( v.x * oos, v.y * oos, v.z * oos );
}


/**
 *	This function returns a vector whose elements are the product of the
 *	corresponding elements of the input vector.
 *
 *	@relates Vector3
 */
inline
Vector3 operator *( const Vector3& a, const Vector3& b )
{
	return Vector3( a.x*b.x, a.y*b.y, a.z*b.z );
}

/**
 *	This function returns whether or not two vectors are equal. Two vectors are
 *	considered equal if all of their corresponding elements are equal.
 *
 *	@return True if the input vectors are equal, otherwise false.
 */
inline
bool operator   ==( const Vector3& v1, const Vector3& v2 )
{
	return isEqual( v1.x, v2.x ) &
		isEqual( v1.y, v2.y ) &
		isEqual( v1.z, v2.z );
}


/**
 *	This function returns whether or not two vectors are not equal. Two vectors
 *	are considered equal if all of their corresponding elements are equal.
 *
 *	@return True if the input vectors are not equal, otherwise false.
 */
inline
bool operator   !=( const Vector3& v1, const Vector3& v2 )
{
	return !(isEqual( v1.x, v2.x ) &&
		isEqual( v1.y, v2.y ) &&
		isEqual( v1.z, v2.z ));
}


/**
 *	This function returns whether or not the vector on the left is less than
 *	the vector on the right. A vector is considered less than another if
 *	its x element is less than the other. Or if the x elements are equal,
 *	then the y elements are compared, and so on.
 *
 *	@return True if the input vectors are not equal, otherwise false.
 */
inline bool operator < ( const Vector3& v1, const Vector3& v2 )
{
	if (v1.x < v2.x) return true;
	if (v1.x > v2.x) return false;
	if (v1.y < v2.y) return true;
	if (v1.y > v2.y) return false;
	return (v1.z < v2.z);
}

// Vector3 pitchYawToVector3( float pitchInRadians, float yawInRadians );

/**
 *	This constructor does not initialise the components of the vector for
 *	performance reasons. To create a zero vector, copy Vector3::s_zero or use
 *	Vector3::setZero.
 */
inline
Vector3::Vector3()
{
	x = y = z = 0.0f;
}


/**
 *	This constructor sets the elements of the vector to the input values.
 *
 *	@param a	The value that element 0 is set to.
 *	@param b	The value that element 1 is set to.
 *	@param c	The value that element 2 is set to.
 */
inline
Vector3::Vector3( float a, float b, float c )
{
	x = a; y = b; z = c;
}

/**
 *	This method sets all elements of the vector to 0.
 */
inline
void Vector3::setZero()
{
	x = y = z = 0;
}


/**
 *	This method sets the elements of the vector to the input values.
 *
 *	@param a	The value that element x is set to.
 *	@param b	The value that element y is set to.
 *	@param c	The value that element z is set to.
 */
inline
void Vector3::set( float a, float b, float c )
{
	x = a;
	y = b;
	z = c;
};

/**
 *	This method returns the dot product of this vector and the input vector.
 *
 *	@param v	The vector to perform the dot product with.
 *
 *	@return The dot product of this vector and the input vector.
 */
inline
float Vector3::dotProduct( const Vector3& v ) const
{
	return x * v.x + y * v.y + z * v.z;
};


/**
 *	This method sets this vector to the cross product of the input vectors.
 */
inline
void Vector3::crossProduct( const Vector3& v1, const Vector3& v2 )
{
	// TODO: This is wrong if &v1 or &v2 is this.
	x = (v1.y * v2.z) - (v1.z * v2.y);
	y = (v1.z * v2.x) - (v1.x * v2.z);
	z = (v1.x * v2.y) - (v1.y * v2.x);
}


/**
 *	Produces a linear interpolation of @a a and @a b based on @a t. 
 *	E.g.:
 *	 - t = 0.0    result = @a a
 *	 - t = 0.5    result = (@a a + @a b)/2 
 *	 - t = 1.0    result = @a b
 *	
 *	@pre True.
 *	@post Set this to be a*(1-t) + b*t.
 */
inline
void Vector3::lerp( const Vector3 & a, const Vector3 & b, float t )
{
	*this = (a * (1.0f - t)) + (b * t);
}


/**
 *	Component wise clamp.
 *
 *	@param lower		
 *	@param upper		
 */
inline
void Vector3::clamp( const Vector3 & lower, const Vector3 & upper )
{
	x = ::clamp( lower.x, x, upper.x );
	y = ::clamp( lower.y, y, upper.y );
	z = ::clamp( lower.z, z, upper.z );
}


/**
 *	This method returns the cross product of this vector with the input vector.
 */
inline
Vector3 Vector3::crossProduct(const Vector3 & v) const
{
	Vector3 result;
	result.crossProduct( *this, v );
	return result;
}


/**
 *	This method sets this vector to vector1 projected onto vector2.
 */
inline
void Vector3::projectOnto( const Vector3& v1, const Vector3& v2 )
{
	*this = v2 * ( v1.dotProduct( v2 ) / v2.lengthSquared() );
}


/**
 *	This method returns this vector projected onto the input vector.
 */
inline
Vector3 Vector3::projectOnto(const Vector3 & v) const
{
	Vector3 result;
	result.projectOnto( *this, v );

	return result;
}

/**
 *	@return This vector projected onto the plane with normal @a vPlaneNorm.
 */
inline
Vector3 Vector3::projectOntoPlane( const Vector3 & vPlaneNorm ) const
{
	return *this - this->projectOnto( vPlaneNorm );
}


inline
Vector3 Vector3::mulParallel( const Vector3& v ) const
{
	return Vector3(this->x * v.x, this->y * v.y, this->z * v.z);
}

/**
 *	This method returns the length of this vector.
 */
inline
float Vector3::length() const
{
	return sqrtf((x * x) + (y * y) + (z * z));
}


/**
 *	This method returns the length of this vector squared.
 */
inline
float Vector3::lengthSquared() const
{
	return this->dotProduct( *this );
}


/**
 *	@return The distance from this point to @a otherPoint.
 */
inline
float Vector3::distance( const Vector3 & otherPoint ) const
{
	return sqrt( distanceSquared( otherPoint ) );
}


/**
 *	@return The distance squared from this point to @a otherPoint.
 */
inline
float Vector3::distanceSquared( const Vector3 & otherPoint ) const
{
	return (*this - otherPoint).lengthSquared();
}


/**
 *	This method normalises this vector. That is, the direction of the vector
 *	will stay the same and its length will become 1.
 */
inline
void Vector3::normalise()
{
	const float length = this->length();

	if (!almostZero( length, 0.00000001f ) )
	{
		float rcp = 1.f / length;
		*this *= rcp;
	}
}

/**
 *	This method normalizes input vector.
 */
inline
Vector3 Vector3::getNormalized() const
{
	Vector3 res(*this);
	res.normalise();
	return res;
}

/**
 *	This function returns a copy of this vector that has been normalised to
 *	unit length.
 *
 *	@return		A copy of this vector normalised to unit length.
 */
inline
Vector3 Vector3::unitVector() const
{
	Vector3 result( *this );
	result.normalise();
	return result;
}


/**
 *	@pre this and @a other must be unit vectors.
 *	@post Returned the minimum angle between this and @a other in radians.
 */
inline
float Vector3::getUnitVectorAngle( const Vector3 & other ) const
{
	return acosf( ::clamp( -1.0f, dotProduct( other ), 1.0f ) );
}


/**
 *	This function returns a vector of squared components
 *
 *	@return		A vector of squared components.
 */
inline
Vector3 Vector3::square() const
{
	return Vector3(x*x, y*y , z*z);
}


/**
 *	This function returns an angle (in radians) between this and other
 *
 *	@return		Angle
 */
inline float Vector3::angle(const Vector3& v) const
{
	float angle = this->dotProduct(v) / ( this->length() * v.length() );
	return (angle > 1.f || angle < -1.f) ? 0.f : acosf(angle);
}


/**
 *	Return the reflection vector.
 *	N is the surface normal which has to be of unit length.
 *
 *	@return		Reflection vector
 */
inline Vector3 Vector3::reflect(const Vector3& n) const
{
	return *this - 2.f * ( this->dotProduct(n) ) * n;
}


/**
 *  Return the transmitted vector.
 *  N is the surface normal which has to be of unit length.
 *  eta is the relative index of refraction. If the returned
 *  vector is zero then there is no transmitted light because
 *  of total internal reflection.
 *
 *  @return		Transmitted vector
 */
inline Vector3 Vector3::refract(const Vector3& n, float eta) const
{
	float dot = this->dotProduct(n);
	float k = 1.f - eta * eta * (1.f - dot * dot);
	return (k < 0.f) ? zero() : ( eta * (*this) - ( eta * dot + sqrtf(k) ) * n );
}


/**
 *	This function an orthogonal vector.
 *	Returns a vector that is orthogonal to self (where this*this.ortho()==0).
 *
 *	@return		Orthogonal vector
 */
inline Vector3 Vector3::ortho() const
{
	float x = fabs(this->x);
	float y = fabs(this->y);
	float z = fabs(this->z);

	// z is smallest
	Vector3 res(-this->y, this->x, 0.f);

	// Is x the smallest element?
	if (x < y &&  x < z)
	{
		res = Vector3(0.f, -this->z, this->y);
	}
	// Is y smallest element?
	else if (y < z)
	{
		res = Vector3(-this->z, 0.f, this->x);
	}

	return res;
}


/**
 *	This function returns the minimum value of the components.
 *
 */
inline float Vector3::min() const
{
	return std::min( std::min(this->x, this->y), this->z );
}


/**
 *	This function returns the maximum value of the components.
 *
 */
inline float Vector3::max() const
{
	return std::max( std::max(this->x, this->y), this->z );
}


/**
 *	This function returns the index of the component with the minimum value.
 *
 */
inline unsigned int Vector3::minIndex() const
{
	unsigned int res = 2;

	if (this->x <= this->y && this->x <= this->z)
	{
		res = 0;
	}
	else if (this->y <= this->z)
	{
		res = 1;
	}
	
	return res;
}


/**
 *	This function returns the index of the component with the maximum value.
 *
 */
inline unsigned int Vector3::maxIndex() const
{
	unsigned int res = 2;

	if (this->x >= this->y && this->x >= this->z)
	{
		res = 0;
	}
	else if (this->y >= this->z)
	{
		res = 1;
	}

	return res;
}


inline float Vector3::minAbs() const
{
	return std::min( std::min( fabs(this->x), fabs(this->y) ), fabs(this->z) );
}


inline float Vector3::maxAbs() const
{
	return std::max( std::max( fabs(this->x), fabs(this->y) ), fabs(this->z) );
}

/**
 *	This function returns the index of the component with the minimum absolute value
 *
 */
inline unsigned int Vector3::minAbsIndex() const
{
	unsigned int res = 2;

	float ax = fabs(this->x);
	float ay = fabs(this->y);
	float az = fabs(this->z);

	if (ax <= ay && ax <= az)
	{
		res = 0;
	}
	else if (ay <= az)
	{
		res = 1;
	}

	return res;
}


/**
 *	This function returns the index of the component with the maximum absolute value.
 *
 */
inline unsigned int Vector3::maxAbsIndex() const
{
	unsigned int res = 2;

	float ax = fabs(this->x);
	float ay = fabs(this->y);
	float az = fabs(this->z);

	if (ax >= ay && ax >= az)
	{
		res = 0;
	}
	else if (ay >= az)
	{
		res = 1;
	}

	return res;
}

/**
 *	This method sets this vector to the direction vector with the input pitch
 *	and yaw. The vector will have unit length.
 */
inline void Vector3::setPitchYaw( float pitchInRadians, float yawInRadians )
{
	double cosPitch = cos( pitchInRadians );
	double sinPitch = sin( -pitchInRadians );

	double cosYaw = cos( yawInRadians );
	double sinYaw = sin( yawInRadians );

	x = float(cosPitch * sinYaw);
	y = float(sinPitch);
	z = float(cosPitch * cosYaw);
}

#endif // VECTOR3_HPP
