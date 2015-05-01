try:
    from setuptools import setup 
except ImportError:
    from distutils.core import setup

from Cython.Build import cythonize

longDescription = """ed2d is a python 2d game engine that was built to use 
modern opengl rendering techniques. The engine can help to create awesome 2d
games."""

setup(
    name='ED2D',
    version='0.0.1',
    author='Alex Marinescu, Matthew Sitton',
    author_email='ale632007@gmail.com, matthewsitton@gmail.com',
    description='2D game engine written in python.',
    long_description=longDescription,
    license = 'BSD',
    keywords='game opengl engine 2D',
    url='https://github.com/explosiveduck/ed2d',
    packages=['ed2d', 'ed2d.csg', 'ed2d.glmath', 'ed2d.glmath.cython', 'ed2d.opengl', 'ed2d.physics'],
    classifiers=[
        # find classifiers at the following url
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers

        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Games/Entertainment',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    ext_modules=cythonize("ed2d/glmath/cython/*.pyx")
)
