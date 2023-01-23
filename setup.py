from distutils.core import setup

setup(
    name='archaea',
    packages=['archaea', 'archaea.geometry', 'archaea.earcut'],
    version='1.1.3',
    license='MIT',
    description='Playground for Geometry!',
    readme='README.md',
    author='Oğuzhan Koral',
    author_email='oguzhankoral@gmail.com',
    url='https://github.com/archaeans/archaea',
    download_url='https://github.com/archaeans/archaea/archive/refs/tags/1.1.3.tar.gz',
    keywords=['geometry', 'mesh', 'stl'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Scientific/Engineering :: Mathematics',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
