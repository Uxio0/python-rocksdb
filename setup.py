from setuptools import setup
from setuptools import find_packages
from distutils.extension import Extension
from distutils.command.build_ext import build_ext

cmplropt = { 'msvc': ['/O3', '/Wall'] }
defopt = ['-std=c++11', '-O3', '-Wall', '-Wextra', '-Wconversion', '-fno-strict-aliasing']

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        cmplr = self.compiler.compiler_type
        if cmplr in cmplropt:
           for e in self.extensions:
               e.extra_compile_args = cmplropt[ cmplr ]
        else:
            for e in self.extensions:
                e.extra_link_args = defopt
        build_ext.build_extensions(self)

try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(extensions): return extensions
    sources = ['rocksdb/_rocksdb.cpp']
else:
    sources = ['rocksdb/_rocksdb.pyx']

mod1 = Extension(
    'rocksdb._rocksdb',
    sources,
    language='c++'
)

setup(
    name="python-rocksdb",
    version='0.6.6',
    description="Python bindings for RocksDB",
    keywords='rocksdb',
    author='Ming Hsuan Tu',
    author_email="Use the github issues",
    url="https://github.com/twmht/python-rocksdb",
    license='BSD License',
    install_requires=['setuptools'],
    package_dir={'rocksdb': 'rocksdb'},
    packages=find_packages('.'),
    ext_modules=cythonize([mod1]),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    cmdclass={'build_ext': build_ext_subclass }
)
