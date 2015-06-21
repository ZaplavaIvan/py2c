#include "Vector3.hpp"
#include "Quaternion.hpp"
#include "simplemath.hpp"

#include <iostream>
using namespace std;


int main()
{
	Vector3 vec1(1, 0, 0);
	Vector3 vec2(0, 1, 0);

	Vector3 vec3 = vec1.cross(vec2);

	cout << "Dot: " << vec1.dot(vec2) << " Cross: (" << vec3.x << ", " << vec3.y << ", " << vec3.z << ")" << endl;

	Quaternion quat;
	quat.fromAngleAxis(0.1f, vec2);

	Vector3 vec4 = quat.rotateVec(vec1);

	cout << "Rotated: (" << vec4.x << ", " << vec4.y << ", " << vec4.z << ")" << endl;

	Vector3 vec5(2, 2, 2);
	Vector3 proj = vec5.projectOntoPlane(Vector3(0, 1, 0));

	cout << "Proj: (" << proj.x << ", " << proj.y << ", " << proj.z << ")" << endl;

	cout<< simplemath::copysign(2, -1) << endl;

	cin.ignore();

	return 0;
}