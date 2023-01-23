from distutils.core import setup

setup(
    name='archaea',
    packages=['archaea', 'archaea.geometry', 'archaea.earcut', 'archaea.writer'],
    version='1.1.4',
    license='Apache 2.0',
    description='Playground for Geometry!',
    readme='README.md',
    author='Oğuzhan Koral',
    author_email='oguzhankoral@gmail.com',
    url='https://github.com/archaeans/archaea',
    download_url='https://github.com/archaeans/archaea/archive/refs/tags/1.1.4.tar.gz',
    keywords=['geometry', 'mesh', 'stl', 'triangulation'],
    install_requires=[
        'numpy',
        'stl'
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
