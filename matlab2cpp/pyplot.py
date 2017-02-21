code = r"""
/*
 * SPlot.h
 *
 *  Created on: 19. aug. 2010
 *      Author: nordmoen
 */

#ifndef SPLOT_H_
#define SPLOT_H_

#include <iostream>
//DGRIM #include "matlib.hpp"
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <map>
//DGRIM #include "armadillo/armadillo"

class PyEngine
{
	static void _initialize() {
		static bool initialized = false;
		if (!initialized) {
			Py_SetProgramName((char*)"splot");
			Py_Initialize();
			_import_array();
			initialized = true;
		}
	}

 public:

	// Wrapper class which takes both row/col vectors, as well as initializer lists
	template <class T>
	class arma_vec
	{
	public:
		const std::vector<T> v;
		arma_vec() : v() {}
		arma_vec(const std::initializer_list<T> &c) : v(c) {}
		arma_vec(const std::vector<T> &vec) : v(vec) {}
		arma_vec(const arma::Col<T> &vec) : v(vec.begin(), vec.end()) {}
		arma_vec(const arma::Row<T> &vec) : v(vec.begin(), vec.end()) {}
		arma_vec(const arma::subview_col<T> &vec) : arma_vec(arma::Col<T>{vec}) {}
		arma_vec(const arma::subview_row<T> &vec) : arma_vec(arma::Row<T>{vec}) {}
		template <class U>
			arma_vec(const arma::eOp<arma::Col<T>, U> &vec) : arma_vec(arma::Col<T>{vec}) {}
		template <class U>
			arma_vec(const arma::eOp<arma::Row<T>, U> &vec) : arma_vec(arma::Row<T>{vec}) {}
	};

	// Wrapper class to limit arma::Mat implicit conversions (from string, for example).
	// For parameter-passing use only, since it borrows reference in some cases.
	template <class T>
	class arma_mat
	{
		const arma::Mat<T> _m;
	public:
		const arma::Mat<T> &m;
		arma_mat(const arma::Mat<T> &mat) : m(mat) {}
		arma_mat(const arma::subview<T> &view) : _m(view), m(_m) {}
		template <class U>
			arma_mat(const arma::eOp<arma::Mat<T>, U> &op) : _m(op), m(_m) {}
	};

	class py_obj
	{
		friend class PyEngine;
		PyObject *obj;

		template <class T> static int npy_typenum();
		template <class NPY_T, class InputIt>
		static PyObject *create(const std::initializer_list<size_t> &in_dims, const InputIt &data, int flags=0)
		{
			std::vector<npy_intp> dims;
			for (auto it=in_dims.begin(); it!=in_dims.end(); ++it)
				dims.push_back((npy_intp)*it);
			PyObject *obj = PyArray_NewFromDescr(&PyArray_Type, PyArray_DescrFromType(npy_typenum<NPY_T>()),
												 dims.size(), (npy_intp*)dims.data(), /*strides*/nullptr,
												 /*data*/nullptr, flags, /*obj*/nullptr);
			std::copy_n(data, PyArray_Size(obj), (NPY_T*)PyArray_DATA((PyArrayObject*)obj));
			return obj;
		}

	    explicit py_obj(PyObject *o, bool steal_reference) : obj(o)
		{
			if (!steal_reference)
				Py_XINCREF(obj);
		}

	public:

		/* Basic constructors */

	    py_obj() : obj(nullptr) {}
		py_obj(const py_obj &other) : obj(other.obj)
		{
			Py_XINCREF(obj);
		}

	    py_obj(const void *); // Trigger link error, to avoid implicit cast to bool

		/* Construct from primitive types, strings */

		py_obj(bool const& b) : obj(PyBool_FromLong(b)) {}
		py_obj(int const& i) : obj(PyInt_FromLong(i)) {}
		py_obj(double const& d) : obj(PyFloat_FromDouble(d)) {}
		py_obj(const char* const& s) : obj(PyString_FromString(s)) {}
		py_obj(std::string const& s) : obj(PyString_FromString(s.c_str())) {}

		/* Construct from various sequences of double/float/int type */

	    py_obj(std::initializer_list<double> c) : obj(create<double>({c.size()}, c.begin())) {}
	    py_obj(std::vector<double> const& vec) : obj(create<double>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<double> const& vec) : py_obj(vec.v) {}
	    py_obj(arma_mat<double> const& mat) : obj(create<double>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

	    py_obj(std::initializer_list<float> c) : obj(create<float>({c.size()}, c.begin())) {}
	    py_obj(std::vector<float> const& vec) : obj(create<float>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<float> const& vec) : py_obj(vec.v) {}
		py_obj(arma_mat<float> const& mat) : obj(create<float>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

	    py_obj(std::initializer_list<arma::cx_double> c) : obj(create<arma::cx_double>({c.size()}, c.begin())) {}
	    py_obj(std::vector<arma::cx_double> const& vec) : obj(create<arma::cx_double>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<arma::cx_double> const& vec) : py_obj(vec.v) {}
		py_obj(arma_mat<arma::cx_double> const& mat) : obj(create<arma::cx_double>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

	    py_obj(std::initializer_list<arma::cx_float> c) : obj(create<arma::cx_float>({c.size()}, c.begin())) {}
	    py_obj(std::vector<arma::cx_float> const& vec) : obj(create<arma::cx_float>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<arma::cx_float> const& vec) : py_obj(vec.v) {}
		py_obj(arma_mat<arma::cx_float> const& mat) : obj(create<arma::cx_float>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

	    py_obj(std::initializer_list<arma::sword> c) : obj(create<arma::sword>({c.size()}, c.begin())) {}
	    py_obj(std::vector<arma::sword> const& vec) : obj(create<arma::sword>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<arma::sword> const& vec) : py_obj(vec.v) {}
		py_obj(arma_mat<arma::sword> const& mat) : obj(create<arma::sword>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

	    py_obj(std::initializer_list<arma::uword> c) : obj(create<arma::uword>({c.size()}, c.begin())) {}
	    py_obj(std::vector<arma::uword> const& vec) : obj(create<arma::uword>({vec.size()}, vec.begin())) {}
		py_obj(arma_vec<arma::uword> const& vec) : py_obj(vec.v) {}
		py_obj(arma_mat<arma::uword> const& mat) : obj(create<arma::uword>({mat.m.n_rows, mat.m.n_cols}, mat.m.begin(), NPY_ARRAY_F_CONTIGUOUS)) {}

		/* Destructor */

		~py_obj()
		{
			Py_XDECREF(obj);
		}

		/* Assignment and equality operators */

		py_obj &operator=(const py_obj &other)
		{
			Py_XDECREF(obj);
			obj = other.obj;
			Py_XINCREF(obj);
			return *this;
		}

		bool operator==(const py_obj &other) const
		{
			return obj==other.obj;
		}

		bool valid() const
		{
			return (obj!=nullptr);
		}

	private:

		/* Cast to PyObject */

		operator PyObject*()
		{
			return obj;
		}
	};

	static py_obj None()
	{
		return py_obj(Py_None, false);
	}

	typedef std::vector<py_obj> args_t;
	typedef std::map<const char*, py_obj> kwargs_t;

 protected:

	PyObject *main_module;

	py_obj py_call_object(py_obj object, const char *func, const args_t &args={}, const kwargs_t &kwargs={})
	{
		py_obj pyFunc(PyObject_GetAttrString(object, func), true);
		if (!pyFunc.valid()) {
			std::cerr << "No such method: " << func << std::endl;
			return py_obj(nullptr, true);
		}

		py_obj pyArgs(PyTuple_New(args.size()), true);
		for (size_t i=0; i<args.size(); i++) {
			Py_INCREF(args[i].obj);
			PyTuple_SetItem(pyArgs.obj, i, args[i].obj); // Steals reference
		}

		py_obj pyKwArgs(PyDict_New(), true);
		for (const auto &item : kwargs)
			PyDict_SetItem(pyKwArgs.obj, py_obj(item.first).obj, item.second.obj);

		py_obj ret(PyObject_Call(pyFunc.obj, pyArgs.obj, pyKwArgs.obj), true);
		if (!ret.obj)
		{
			PyErr_Print();
		}
		return ret;
	}

	py_obj py_call(const char *func, const args_t &args={}, const kwargs_t &kwargs={})
	{
		return py_call_object(py_obj(main_module, false), func, args, kwargs);
	}

	py_obj error(const char *msg)
	{
		std::cerr << msg << std::endl;
		return py_obj(nullptr, false);
	}

 public:
	PyEngine()
	{
		_initialize();
		main_module = PyImport_AddModule("__main__");
	}

	virtual ~PyEngine()
	{
	}

	bool py_code(const char *str, const kwargs_t &data={})
	{
		for (auto item : data)
		{
			py_put_variable(item.first, item.second);
		}
		if (PyRun_SimpleString(str) != 0)
		{
			std::cerr << "Error from Python interpreter:" << std::endl;
			PyErr_Print();
			return false;
		}
		return true;
	}

	void py_put_variable(const char *name, const py_obj &val)
	{
		Py_INCREF(val.obj);
		PyModule_AddObject(main_module, name, val.obj); // Steals reference
	}

	py_obj py_get_variable(const char *name)
	{
		return py_obj(PyDict_GetItemString(main_module, name), false); // Borrowed reference
	}

	py_obj py_get_module(const char *name)
	{
		return py_obj(PyImport_AddModule(name), false); // Borrowed reference
	}
};


class SPlot : public PyEngine
{
 public:
	SPlot()
		: PyEngine()
	{
		std::string splot_py;
		std::ifstream in("splot.py");
		if (in.fail())
		{
			// May be copied to separate file "splot.py" in current directory
			splot_py = R"(
from __future__ import division

import matplotlib as mpl
qt_backend = None
try:
    from PyQt4 import QtCore, QtGui, QtGui as QtWidgets
    qt_backend = 4
except ImportError:
    try:
        from PyQt5 import QtCore, QtGui, QtWidgets
        qt_backend = 5
    except ImportError:
        pass
if qt_backend:
    try:
        mpl.use('qt%dagg'%qt_backend)
    except:
        pass

from pylab import *
import numpy as np

pylab_show = show
def show(interactive):
    if qt_backend:
        pylab_show(block=False)
        if interactive:
            QtWidgets.QApplication.instance().exec_()
    else:
        pylab_show(block=interactive)

def wigb(a, scale=1.0, x=None, z=None, amx=None, xshift=0.0, **kwargs):
    kwargs.setdefault('color', 'black')
    kwargs.setdefault('linewidth', 0.2)

    n,m = a.shape

    if amx is None or amx==0:
        #amx = np.mean(np.max(np.abs(a), axis=1))
        amx = np.max(np.max(np.abs(a), axis=1))

    if x is None or len(x)==0:
        x = np.arange(m)
    if z is None or len(z)==0:
        z = np.arange(n)

    dx = np.median(np.abs(x[1:]-x[:-1]))
    dz = z[1]-z[0]
    a *= scale*dx/amx

    #set display ranges
    (xmin,xmax) = np.min(x), np.max(x)
    (zmin,zmax) = np.min(z), np.max(z)
    xlim(xmin-2*dx, xmax+2*dx)
    ylim(zmin-dz, zmax+dz)
    gca().invert_yaxis()

    transData = gca().transData
    plots = []
    for i,xi in enumerate(x):
        trace = a[:,i]
        if trace.any(): # skip zero traces
            plot_lines = plot(xi+trace, z, **kwargs)
            plot_fill = fill_betweenx(z, xi-dx, xi+trace, **kwargs)
            plots.append((plot_lines,plot_fill))

            # Create clipping path for fill (instead of calculating zero-crossings)
            x0 = xi+xshift
            x1 = xi+dx if i+1<len(x) else xi+np.max(trace)
            #x1 = xi+np.max(trace)
            path = mpl.path.Path([(x0,zmin), (x0,zmax), (x1,zmax), (x1,zmin), (x0,zmin)])
            plot_fill.set_clip_path(path, transData)

    return plots


if not qt_backend:
    def table(*args, **kwargs):
        print 'Failed to import Qt, no table support. Please install pyqt4 or pyqt5.'
else:
    class TableModel(QtCore.QAbstractTableModel):
        def __init__(self, mat):
            QtCore.QAbstractTableModel.__init__(self)
            self.mat = mat

        def data(self, index, role):
            if role == QtCore.Qt.DisplayRole:
                value = self.mat[index.row(), index.column()]
                return '{: f}'.format(value)
            return None

        def rowCount(self, index):
            return self.mat.shape[0]

        def columnCount(self, index):
            return self.mat.shape[1]

        def headerData(self, section, orientation, role):
            if role == QtCore.Qt.DisplayRole:
                return str(section+1)
            return None

    class TableView(QtWidgets.QTableView):
        _views = {} # references to live windows, to prevent early deletion

        def __init__(self):
            QtWidgets.QTableView.__init__(self)
            if qt_backend == 4:
                self.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Fixed)
                self.verticalHeader().setResizeMode(QtWidgets.QHeaderView.Fixed)
            else:
                self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
                self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            self.pt = self.font().pointSize()
            self.chars = 9

            if qt_backend == 4:
                self.connect(QtWidgets.QShortcut(QtWidgets.QKeySequence.ZoomIn, self), QtCore.SIGNAL('activated()'), self.zoom_in)
                self.connect(QtWidgets.QShortcut(QtWidgets.QKeySequence.ZoomOut, self), QtCore.SIGNAL('activated()'), self.zoom_out)
                self.connect(QtWidgets.QShortcut(QtWidgets.QKeySequence.Close, self), QtCore.SIGNAL('activated()'), self.close)
            else:
                QtWidgets.QShortcut(QtGui.QKeySequence.ZoomIn, self).activated.connect(self.zoom_in)
                QtWidgets.QShortcut(QtGui.QKeySequence.ZoomOut, self).activated.connect(self.zoom_out)
                QtWidgets.QShortcut(QtGui.QKeySequence.Close, self).activated.connect(self.close)

            TableView._views[self] = self

        def _getMonospaceFont(self):
            font = QtGui.QFont('monospace')
            if font.fixedPitch(): return font
            font.setStyleHint(QtGui.QFont.Monospace)
            if font.fixedPitch(): return font
            font.setStyleHint(QtGui.QFont.TypeWriter)
            if font.fixedPitch(): return font
            font.setFamily('courier')
            if font.fixedPitch(): return font
            font.setKerning(False)
            font.setFixedPitch(True)
            return font

        def setMonospaceFont(self):
            self.setFont(self._getMonospaceFont())

        def setFontSize(self, pt):
            font = self.font()
            font.setPointSize(pt)
            self.setFont(font)
            self.pt = pt

            metrics = QtGui.QFontMetrics(font)
            padding = 1.5
            width = 2*padding + self.chars*metrics.width('X')
            width = width*1.3
            height = metrics.height() + 4*padding

            header = self.verticalHeader()
            header.setFont(font)
            for i in xrange(header.length()):
                header.resizeSection(i, height)

            header = self.horizontalHeader()
            header.setFont(font)
            for i in xrange(header.length()):
                header.resizeSection(i, width)

        def zoom_in(self):
            self.setFontSize(self.pt + 1)

        def zoom_out(self):
            if self.pt > 1:
                self.setFontSize(self.pt - 1)

        def wheelEvent(self, event):
            if event.modifiers() == QtCore.Qt.ControlModifier:
                delta = event.delta() if qt_backend==4 else event.angleDelta().y()
                if delta > 1:
                    self.zoom_in()
                else:
                    self.zoom_out()
            else:
                QtWidgets.QTableView.wheelEvent(self, event)

        def closeEvent(self, event):
            del TableView._views[self]
            QtWidgets.QTableView.closeEvent(self, event)


    def table(mat, title=None):
        if QtWidgets.QApplication.instance() is None:
            import sys
            table.app = QtWidgets.QApplication(sys.argv)
        table.seq += 1
        if title is None:
            title = 'Table %d '%table.seq
        title += ' (%dx%d %s)'%(mat.shape+(mat.dtype.name,))

        model = TableModel(mat)
        view = TableView()
        view.setMonospaceFont()
        if np.iscomplexobj(mat):
            view.chars *= 2
        view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        view.setModel(model)
        view.setFontSize(8)
        view.resize(600, 400)
        view.setWindowTitle(title)
        view.show()
    table.seq = 0
)";
		} else {
			splot_py = static_cast<std::stringstream&>(std::stringstream() << in.rdbuf()).str();
		}
		py_code(splot_py.c_str());
	}

	py_obj figure(const py_obj &figno)
	{
		return py_call("figure", {figno});
	}

	py_obj hold(bool onoff)
	{
		return py_call("hold", {onoff});
	}

	py_obj clf()
	{
		return py_call("clf");
	}

	py_obj cla()
	{
		return py_call("cla");
	}

	py_obj show(bool block=true)
	{
		return py_call("show", {block});
	}

	py_obj xlabel(const char *label)
	{
		return py_call("xlabel", {label});
	}

	py_obj ylabel(const char *label)
	{
		return py_call("ylabel", {label});
	}

	py_obj title(const char *title)
	{
		return py_call("title", {title});
	}

	py_obj plot(const arma_vec<double> &x, const arma_vec<double> &y, const kwargs_t &kwargs)
	{
		return py_call("plot", {x, y}, kwargs);
	}

	py_obj plot(const arma_vec<double> &x, const arma_vec<double> &y, const std::string& spec={})
	{
		return py_call("plot", {x, y, spec});
	}

	py_obj plot(const arma_vec<double> &x1, const arma_vec<double> &y1,
				const arma_vec<double> &x2, const arma_vec<double> &y2, const std::string& spec2={})
	{
		return py_call("plot", {x1, y1, std::string(), x2, y2, spec2});
	}

	py_obj plot(const arma_vec<double> &x1, const arma_vec<double> &y1, const std::string& spec1,
				const arma_vec<double> &x2, const arma_vec<double> &y2, const std::string& spec2={})
	{
		return py_call("plot", {x1, y1, spec1, x2, y2, spec2});
	}

	py_obj imshow(const arma_mat<double> &A, const kwargs_t &kwargs={})
	{
		kwargs_t new_kwargs(kwargs);
		new_kwargs.emplace("aspect", "auto");
		new_kwargs.emplace("interpolation", "nearest");
		//new_kwargs.emplace("clim", py_obj({A.min(), A.max()}));
		return py_call("imshow", {A}, new_kwargs);
	}

	py_obj imagesc(const arma_mat<double> &A, const kwargs_t &kwargs={})
	{
		return imshow(A, kwargs);
	}

	py_obj imagesc(const arma_vec<double> &x, const arma_vec<double> &y, const arma_mat<double> &A, const kwargs_t &kwargs={})
	{
		if (x.v.empty() && y.v.empty())
			return imagesc(A, kwargs);
		if ((x.v.size() != 2 && x.v.size() != A.m.n_cols) || (y.v.size() != 2 && y.v.size() != A.m.n_rows))
			return error("imagesc: length of x/y bounds must be 2 or matrix dimensions");

		kwargs_t new_kwargs(kwargs);
		new_kwargs["extent"] = {x.v[0], x.v[x.v.size()-1], y.v[0], y.v[y.v.size()-1]};
		return imagesc(A, new_kwargs);
	}

	py_obj imagesc(const arma_mat<double> &A, const arma_vec<double> &clims, const kwargs_t &kwargs={})
	{
		return imagesc(arma_vec<double>(), arma_vec<double>(), A, clims, kwargs);
	}

	py_obj imagesc(const arma_vec<double> &x, const arma_vec<double> &y, const arma_mat<double> &A, const arma_vec<double> &clims, const kwargs_t &kwargs={})
	{
		if (clims.v.empty())
			return imagesc(x, y, A, kwargs);

		if (clims.v.size() != 2)
			return error("imagesc: length of c bounds must be 2");

		kwargs_t new_kwargs(kwargs);
		new_kwargs["clim"] = clims;
		return imagesc(x, y, A, new_kwargs);
	}

	py_obj wigb(const arma_mat<double> &A, double scale=1.0, const arma_vec<double> &x={}, const arma_vec<double> &z={}, double amx=0.0, const kwargs_t &kwargs={})
	{
		return py_call("wigb", {A, scale, x, z, amx}, kwargs);
	}

	py_obj colorbar()
	{
		return py_call("colorbar");
	}

	py_obj colorbar(py_obj mappable)
	{
		return py_call("colorbar", {mappable});
	}

	py_obj colorbar(py_obj mappable, py_obj ax)
	{
		return py_call("colorbar", {mappable, ax});
	}

	py_obj xlim(double xmin, double xmax)
	{
		return py_call("xlim", {xmin, xmax});
	}

	py_obj ylim(double ymin, double ymax)
	{
		return py_call("ylim", {ymin, ymax});
	}

	py_obj caxis(double cmin, double cmax)
	{
		return py_call("clim", {cmin, cmax});
	}

	py_obj axis(double xmin, double xmax, double ymin, double ymax)
	{
		return py_call("axis", {{xmin, xmax, ymin, ymax}});
	}

	py_obj grid(const kwargs_t &kwargs={})
	{
		return py_call("grid", {}, kwargs);
	}

	py_obj subplot(int xyi, const kwargs_t &kwargs={})
	{
		return py_call("subplot", {xyi}, kwargs);
	}

	py_obj subplot(int x, int y, int i, const kwargs_t &kwargs={})
	{
		return py_call("subplot", {x, y, i}, kwargs);
	}

	py_obj colormap(py_obj fig, const std::string &name, int levels=64)
	{
		const size_t start = name.find('(');
		if (start != std::string::npos)
		{
			const size_t end = name.find(')');
			if (end != std::string::npos && end>start)
			{
				const std::string name_part(name.substr(start));
				const int levels_part = atoi(name.substr(start+1, end).c_str());
				return colormap(fig, name_part, levels_part);
			}
		}
		py_obj cmap = py_call("get_cmap", {(name=="default" ? "jet" : name), levels});
		return py_call_object(fig, "set_cmap", {cmap});
	}

	py_obj colormap(const std::string &name, int levels=64)
	{
		return colormap(py_call("gci"), name, levels);
	}

	py_obj colormap(const py_obj &fig, const arma_mat<double> &segments)
	{
		py_obj cmap = py_call_object(py_get_module("matplotlib.colors"), "ListedColormap", {segments});
		return py_call_object(fig, "set_cmap", {cmap});
	}

	py_obj colormap(const arma_mat<double> &segments)
	{
		return colormap(py_call("gci"), segments);
	}

	void table(const arma_mat<double> &mat, const py_obj &title=None())
	{
		py_call("table", {mat, title});
	}

	void table(const arma_mat<arma::cx_double> &mat, const py_obj &title=None())
	{
		py_call("table", {mat, title});
	}

};

template <> int PyEngine::py_obj::npy_typenum<double>() { return NPY_DOUBLE; }
template <> int PyEngine::py_obj::npy_typenum<float>() { return NPY_FLOAT; }
template <> int PyEngine::py_obj::npy_typenum<int>() { return NPY_INT32; }
template <> int PyEngine::py_obj::npy_typenum<unsigned int>() { return NPY_UINT32; }
template <> int PyEngine::py_obj::npy_typenum<long long>() { return NPY_INT64; }
template <> int PyEngine::py_obj::npy_typenum<unsigned long long>() { return NPY_UINT64; }
template <> int PyEngine::py_obj::npy_typenum<arma::cx_float>() { return NPY_COMPLEX64; }
template <> int PyEngine::py_obj::npy_typenum<arma::cx_double>() { return NPY_COMPLEX128; }

#endif /* SPLOT_H_ */
"""
