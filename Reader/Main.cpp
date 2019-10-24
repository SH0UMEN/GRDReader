#include <Windows.h>
#include <Python.h>
#include <cmath>
#include <iostream>
#include <fstream>
#include <numpy/arrayobject.h>

using namespace std;

PyObject* read_and_draw(PyObject*, PyObject* args) {
	const char* filename = PyUnicode_AsUTF8(PyList_GetItem(args, 0));
	PyObject* colorList = PyList_GetItem(args, 1);
	int levels = PyList_Size(colorList);
	
	FILE *file;
	fopen_s(&file, filename, "rb");
	char* var = new char[4];
	short Nx, Ny;
	double Xmin, Xmax, Ymin, Ymax, Zmin, Zmax;
	float z = 0;

	//read header
	fread(var, sizeof(char), 4, file);
	fread(&Nx, sizeof(short), 1, file);
	fread(&Ny, sizeof(short), 1, file);
	fread(&Xmin, sizeof(double), 1, file); fread(&Xmax, sizeof(double), 1, file);
	fread(&Ymin, sizeof(double), 1, file); fread(&Ymax, sizeof(double), 1, file);
	fread(&Zmin, sizeof(double), 1, file); fread(&Zmax, sizeof(double), 1, file);

	PyObject* image = PyList_New(Ny);
	PyObject* res = PyList_New(2);
	PyObject* matrix = PyList_New(Ny);

	float h = (Zmax - Zmin) / levels;

	float* zLevels = new float[levels];

	for (int i = 1; i < levels + 1; i++) {
		zLevels[i - 1] = Zmin + ((float)h * i);
	}

	for (int y = Ny-1; y >= 0; y--) {
		PyObject* imageRow = PyList_New(Nx);
		PyObject* matrixRow = PyList_New(Nx);

		for (int x = 0; x < Nx; x++) {
			fread(&z, sizeof(float), 1, file);
			PyList_SetItem(matrixRow, x, PyFloat_FromDouble((double)z));

			for (int level = 0; level < levels; level++) {
				if (z <= zLevels[level]) {
					PyList_SetItem(imageRow, x, PyList_GetItem(colorList, level));
					break;
				}
			}
		}

		PyList_SetItem(matrix, y, matrixRow);
		PyList_SetItem(image, y, imageRow);
	}

	PyList_SetItem(res, 0, matrix);
	PyList_SetItem(res, 1, image);

	fclose(file);
	return res;
}

PyObject* numpy_test(PyObject*, PyObject* args) {
	PyObject* p = PyList_New(4);
	//npy_intp size = { k : 200 };
	return p;
}

static PyMethodDef reader_methods[] = {
	{ "read_and_draw", (PyCFunction)read_and_draw, METH_O, nullptr },
	{ "numpy_test", (PyCFunction)numpy_test, METH_O, nullptr },
	{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef reader_module = {
	PyModuleDef_HEAD_INIT,
	"reader",                        
	"Provudes fast function for read and build contours from .grd files",
	0,
	reader_methods
};

PyMODINIT_FUNC PyInit_reader() {
	return PyModule_Create(&reader_module);
}