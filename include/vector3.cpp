#include "vector3.hpp"

const Vector3 Vector3::ZERO( 0.f, 0.f, 0.f );
const Vector3 Vector3::I( 1.f, 0.f, 0.f );
const Vector3 Vector3::J( 0.f, 1.f, 0.f );
const Vector3 Vector3::K( 0.f, 0.f, 1.f );

float Vector3::getAngle( const Vector3 & other ) const
{
	const Vector3 aUnit = unitVector();
	const Vector3 bUnit = other.unitVector();

	return acosf( ::clamp( -1.0f, aUnit.dotProduct( bUnit ), 1.0f ) );
}

// vector3.cpp
