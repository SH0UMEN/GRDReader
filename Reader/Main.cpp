#include <Windows.h>
#include <Python.h>
#include <cmath>
#include <iostream>
#include <fstream>

using namespace std;

PyObject* read_and_draw(PyObject*, PyObject* args) {
	/*file = open(filename, 'rb')
		file.read(4)
		Nx, Ny = struct.unpack("h", file.read(2))[0], struct.unpack("h", file.read(2))[0]
		Xmin, Xmax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
		Ymin, Ymax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
		self.Zmin, self.Zmax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
		matrix = []

		green = Color("green")
		red = Color("red")
		colorRange = list(green.range_to(red, levels))
		colorRangeCopy = []

		for c in colorRange :
		col = QColor(c.get_hex())
		colorRangeCopy.append((col.red(), col.green(), col.blue(), col.alpha()))

		colorRange = colorRangeCopy

		h = (self.Zmax - self.Zmin) / levels
		zLevels = []

		for i in range(1, levels + 1) :
			zLevels.append(self.Zmin + h * i)

			img = QImage(Nx, Ny, 5)
			ptr = img.bits()
			ptr.setsize(img.byteCount())
			arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)

			#handler
			for y in range(Ny) :
				raw = []
				for x in range(Nx) :
					z = struct.unpack("f", file.read(4))[0]
					raw.append(z)

					for level in range(levels) :
						if (z <= zLevels[level]) :
							arr[y, x] = colorRange[level]
							break

							matrix.append(raw)

							file.close()
							self.matrix = matrix

							return QPixmap(QPixmap.fromImage(img))*/

	const char* filename = PyUnicode_AsUTF8(PyList_GetItem(args, 0));
	PyObject* colorList = PyList_GetItem(args, 1);
	int levels = PyList_Size(colorList);

	/*long colors[PyList_Size(colorList)][4];
	
	for (int i = 0; i < 2; i++) {
		Py_ssize_t curColor = i;
		PyObject *color = PyList_GetItem(colorList, curColor);
		
		for (int k = 0; k < 4; k++) {
			Py_ssize_t curIn = k;
			colors[i][k] = PyLong_AsLong(PyTuple_GetItem(color, curIn));
		}
	}*/
	
	FILE *file;
	fopen_s(&file, filename, "r");
	char* var = new char();
	short Nx, Ny, N;
	double Xmin, Xmax, Ymin, Ymax, Zmin, Zmax;


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

	float* zLevels = new float(levels);

	for (int i = 1; i < levels + 1; i++) {
		zLevels[i - 1] = Zmin + h * i;
	}

	for (int y = 0; y < Ny; y++) {
		PyObject* imageRow = PyList_New(Nx);
		PyObject* matrixRow = PyList_New(Nx);

		for (int x = 0; x < Nx; x++) {
			float z;
			fread(&z, sizeof(float), 1, file);
			PyList_SetItem(matrixRow, x, PyFloat_FromDouble(z));

			for (int level = 0; level < levels; level++) {
				if (z <= zLevels[level]) {
					PyList_SetItem(imageRow, x, PyList_GetItem(colorList, level));
					break;
				}
			}
		}

		PyList_SetItem(image, y, matrixRow);
		PyList_SetItem(image, y, imageRow);
	}

	PyList_SetItem(res, 0, matrix);
	PyList_SetItem(res, 1, image);

	fclose(file);
	return res;
}

static PyMethodDef reader_methods[] = {
	{ "read_and_draw", (PyCFunction)read_and_draw, METH_O, nullptr },
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