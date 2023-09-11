// 导出函数
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "geotools.c"


static PyObject *py_out_of_china(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }
    // 调用geotools.c中的函数
    int result = out_of_china(lon, lat);
    if (result == 0) {
        Py_RETURN_FALSE;
    } else {
        Py_RETURN_TRUE;
    }
}

static PyObject *py_bd09_to_wgs84(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    bd09_to_wgs84(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

static PyObject *py_bd09_to_gcj02(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    bd09_to_gcj02(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

static PyObject *py_gcj02_to_wgs84(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    gcj02_to_wgs84(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

static PyObject *py_gcj02_to_bd09(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    gcj02_to_bd09(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

static PyObject *py_wgs84_to_bd09(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    wgs84_to_bd09(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

static PyObject *py_wgs84_to_gcj02(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"lon", "lat", NULL};
    double lon, lat;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "dd", keywords, &lon, &lat)) {
        return NULL;
    }

    double output[2];
    wgs84_to_gcj02(lon, lat, output);
    return Py_BuildValue("(dd)", output[0], output[1]);
}

// 定义methods列表
static PyMethodDef methods[] = {
        {"out_of_china", (PyCFunction)(void(*)(void))py_out_of_china, METH_VARARGS | METH_KEYWORDS, "判断给定的经纬度是否在中国境外"},
        {"bd09_to_wgs84", (PyCFunction)(void(*)(void))py_bd09_to_wgs84, METH_VARARGS | METH_KEYWORDS, "将BD09坐标转换为WGS84坐标"},
        {"bd09_to_gcj02", (PyCFunction)(void(*)(void))py_bd09_to_gcj02, METH_VARARGS | METH_KEYWORDS, "将BD09坐标转换为GCJ02坐标"},
        {"gcj02_to_wgs84", (PyCFunction)(void(*)(void))py_gcj02_to_wgs84, METH_VARARGS | METH_KEYWORDS, "将GCJ02坐标转换为WGS84坐标"},
        {"gcj02_to_bd09", (PyCFunction)(void(*)(void))py_gcj02_to_bd09, METH_VARARGS | METH_KEYWORDS, "将GCJ02坐标转换为BD09坐标"},
        {"wgs84_to_bd09", (PyCFunction)(void(*)(void))py_wgs84_to_bd09, METH_VARARGS | METH_KEYWORDS, "将WGS84坐标转换为BD09坐标"},
        {"wgs84_to_gcj02", (PyCFunction)(void(*)(void))py_wgs84_to_gcj02, METH_VARARGS | METH_KEYWORDS, "将WGS84坐标转换为GCJ02坐标"},
        {NULL, NULL, 0, NULL}
};

// 注册模块
static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "coord",
        "经纬度坐标转换",
        -1,
        methods
};


// 初始化模块
PyMODINIT_FUNC PyInit_coord(void) {
    return PyModule_Create(&module);
}
