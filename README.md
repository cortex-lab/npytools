# Command-line utilities to deal with NPY array files

## The NPY format

The NPY file format is used to store NumPy arrays. It is becoming a de facto standard for storing arbitrarily large multidimensional arrays. For instance, the [International Brain Laboratory](https://www.internationalbrainlab.com/) uses it for a large part of its data.

* [Documentation of NPY](https://numpy.org/devdocs/reference/generated/numpy.lib.format.html)
* [Motivation behind the NPY format](https://docs.scipy.org/doc/numpy-1.9.2/neps/npy-format.html)

Although first implemented in a Python library, there are now libraries in many languages, including the following (some of the libraries below may be experimental):

* [Python](https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.load.html)
* [MATLAB](https://github.com/kwikteam/npy-matlab)
* [Julia](https://github.com/fhs/NPZ.jl)
* [R](http://dirk.eddelbuettel.com/code/rcpp.cnpy.html)
* [C/C++](https://github.com/rogersce/cnpy)
* [C#](http://accord-framework.net/docs/html/T_Accord_IO_NpyFormat.htm)
* [Java](https://github.com/JetBrains-Research/npy)
* [Rust](https://docs.rs/npy/0.4.0/npy/)
* [Javascript](https://github.com/aplbrain/npyjs)
* [Go](https://github.com/kshedden/gonpy)
* [Haskell](https://github.com/erthalion/hnpy)
* [Swift](https://github.com/qoncept/swift-npy)
* [Lisp](https://github.com/marcoheisig/numpy-file-format)


## npytools

Even if the NPY format is quite simple (a header with metadata about the array, such as its dtype and shape, followed by the raw binary data), and NPY files can be easily open in Python, there is also a need for command-line tools to manage and quickly inspect NPY files.

npytools is a minimal Python library that provides such tools.


### Installation

Dependencies : Python 3, NumPy.

To install: `pip install git+https://github.com/cortex-lab/npytools.git`


### npyshow

`npypshow` is a simple command-line tool that will display metadata and possibly basic statistics about an array stored in a NPY file. The array is memmapped and therefore not entirely loaded in memory, unless the `--show-stats` option is used.

```bash
$ npyshow myarray.npy --show-stats
+----------|----------------+
| shape    | (524, 82, 374) |
| dtype    | float32        |
| filesize | 64.3M          |
| size     | 16070032       |
| min      | -0.59231997    |
| mean     | -3.6333304e-06 |
| median   | 0.0            |
| max      | 0.58112603     |
| zero     | 15049624 (93%) |
| nan      | 0              |
| inf      | 0              |
+----------|----------------+
[[[ 0.      0.     ...  0.      0.    ]
  [ 0.      0.     ...  0.      0.    ]
  ...
  [ 0.0007  0.0099 ...  0.      0.    ]
  [ 0.0003  0.004  ...  0.      0.    ]]

 ...

 [[ 0.      0.     ...  0.      0.    ]
  [ 0.      0.     ...  0.      0.    ]
  ...
  [ 0.      0.     ...  0.      0.    ]
  [ 0.      0.     ...  0.      0.    ]]]
```
