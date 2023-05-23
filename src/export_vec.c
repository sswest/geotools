// 导出函数
#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>

#include "geotools.c"

#define LOCATION_TYPE_CHECK(arr) \
    PyArrayObject *numpy_arr = NULL; \
    npy_intp num_points = 0; \
    int is_list = 0; \
    \
    if (PyList_Check(arr) || PyTuple_Check(arr)) { \
        is_list = 1; \
        num_points = PySequence_Length(arr); \
    } else if (PyArray_Check(arr)) { \
        numpy_arr = (PyArrayObject *)arr; \
        if (PyArray_NDIM(numpy_arr) != 2 || PyArray_DIM(numpy_arr, 1) != 2) { \
            PyErr_SetString(PyExc_ValueError, "Invalid input: loc_arr must be a 2D array-like object with shape (N, 2)"); \
            return NULL; \
        } \
        num_points = PyArray_DIM(numpy_arr, 0); \
    } else { \
        PyErr_SetString(PyExc_TypeError, "Invalid input: loc_arr must be a list, tuple, or ndarray"); \
        return NULL; \
    }

#define CONVERT_COORDINATES(conversion_func) \
    PyObject *output_arr = PyArray_SimpleNew(2, dims, NPY_DOUBLE); \
    double *output_data = PyArray_DATA((PyArrayObject *)output_arr); \
    double output[2]; \
    if (is_list == 1) { \
        for (npy_intp i = 0; i < num_points; ++i) { \
            PyObject *point = PySequence_GetItem(loc_arr, i); \
            PyObject *x_obj = PySequence_GetItem(point, 0); \
            PyObject *y_obj = PySequence_GetItem(point, 1); \
            double x = PyFloat_AsDouble(x_obj); \
            double y = PyFloat_AsDouble(y_obj); \
            conversion_func(x, y, output); \
            output_data[i * 2] = output[0]; \
            output_data[i * 2 + 1] = output[1]; \
            Py_DECREF(point); \
            Py_DECREF(x_obj); \
            Py_DECREF(y_obj); \
        } \
    } else { \
        PyArrayObject *numpy_arr = (PyArrayObject *)loc_arr; \
        double *input_data = PyArray_DATA(numpy_arr); \
        for (npy_intp i = 0; i < num_points; ++i) { \
            double x = input_data[i * 2]; \
            double y = input_data[i * 2 + 1]; \
            conversion_func(x, y, output); \
            output_data[i * 2] = output[0]; \
            output_data[i * 2 + 1] = output[1]; \
        } \
    }


// 向量化函数
static PyObject *vec_out_of_china(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }

    LOCATION_TYPE_CHECK(loc_arr)
    PyObject *output_arr = PyArray_SimpleNew(1, &num_points, NPY_BOOL);
    char *output_data = (char *)PyArray_DATA((PyArrayObject *)output_arr);

    // 逐个处理每个经纬度坐标
    double lon, lat;
    if (is_list == 1) {
        for (npy_intp i = 0; i < num_points; i++) {
            PyObject *point = PySequence_GetItem(loc_arr, i);
            if (PyList_Check(point)) {
                // 判断point长度是否为 2
                if (PyList_Size(point) != 2) {
                    Py_DECREF(output_arr);
                    PyErr_SetString(PyExc_TypeError,
                                    "Invalid input: loc_arr must contain tuples/lists with (lon, lat) values");
                    return NULL;
                }
                // 从列表中提取经纬度值
                lon = PyFloat_AsDouble(PyList_GetItem(point, 0));
                lat = PyFloat_AsDouble(PyList_GetItem(point, 1));
            } else if (!(PyArg_ParseTuple(point, "dd", &lon, &lat))) {
                Py_DECREF(output_arr);
                PyErr_SetString(PyExc_TypeError,
                                "Invalid input: loc_arr must contain tuples/lists with (lon, lat) values");
                return NULL;
            }
            Py_DECREF(point);
            int result = out_of_china(lon, lat);
            output_data[i] = (result == 0) ? 0 : 1;
        }
    } else {
        for (npy_intp i = 0; i < num_points; i++) {
            double lon, lat;
            // 如果是 NumPy 数组，从中提取经纬度值
            PyArrayObject *location = (PyArrayObject *)loc_arr;
            lon = *(double *)(PyArray_GETPTR2(location, i, 0));
            lat = *(double *)(PyArray_GETPTR2(location, i, 1));
            int result = out_of_china(lon, lat);
            output_data[i] = (result == 0) ? 0 : 1;
        }
    }
    return output_arr;
}

static PyObject *vec_bd09_to_wgs84(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(bd09_to_wgs84)
    return output_arr;
}

static PyObject *vec_bd09_to_gcj02(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(bd09_to_gcj02)
    return output_arr;
}

static PyObject *vec_gcj02_to_wgs84(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(gcj02_to_wgs84)
    return output_arr;
}

static PyObject *vec_gcj02_to_bd09(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(gcj02_to_bd09)
    return output_arr;
}

static PyObject *vec_wgs84_to_bd09(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(wgs84_to_bd09)
    return output_arr;
}

static PyObject *vec_wgs84_to_gcj02(PyObject *self, PyObject *args) {
    PyObject *loc_arr;
    if (!PyArg_ParseTuple(args, "O", &loc_arr)) {
        return NULL;
    }
    LOCATION_TYPE_CHECK(loc_arr)
    // 创建输出的 NumPy 数组
    npy_intp dims[2] = {num_points, 2};
    CONVERT_COORDINATES(wgs84_to_gcj02)
    return output_arr;
}

// 定义向量化函数的方法列表
static PyMethodDef vec_methods[] = {
        {"out_of_china", vec_out_of_china, METH_VARARGS, "判断给定的经纬度是否在中国境外"},
        {"bd09_to_wgs84", vec_bd09_to_wgs84, METH_VARARGS, "将 BD09 坐标转换为 WGS84 坐标"},
        {"bd09_to_gcj02", vec_bd09_to_gcj02, METH_VARARGS, "将 BD09 坐标转换为 GCJ02 坐标"},
        {"gcj02_to_wgs84", vec_gcj02_to_wgs84, METH_VARARGS, "将 GCJ02 坐标转换为 WGS84 坐标"},
        {"gcj02_to_bd09", vec_gcj02_to_bd09, METH_VARARGS, "将 GCJ02 坐标转换为 BD09 坐标"},
        {"wgs84_to_bd09", vec_wgs84_to_bd09, METH_VARARGS, "将 WGS84 坐标转换为 BD09 坐标"},
        {"wgs84_to_gcj02", vec_wgs84_to_gcj02, METH_VARARGS, "将 WGS84 坐标转换为 GCJ02 坐标"},
        {NULL, NULL, 0, NULL}
};

// 定义向量化函数的模块
static struct PyModuleDef vec_module = {
        PyModuleDef_HEAD_INIT,
        "vec",
        "向量化计算函数",
        -1,
        vec_methods
};

// 初始化向量化函数的模块
PyMODINIT_FUNC PyInit_vec(void) {
    import_array();
    return PyModule_Create(&vec_module);
}