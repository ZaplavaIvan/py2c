namespace simplemath
{

inline int copysign(float x, float y) 
{
	return x * (y >= 0 ? 1 : -1);
}

inline float radians(float degrees)
{
    return degrees * 3.14f / 180.0f;
}

inline float sqrt(float value)
{
    return std::sqrt(value);
}

}