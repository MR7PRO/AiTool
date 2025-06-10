from setuptools import setup

setup(
    name="ModernMultiTool",
    version="1.0",
    packages=["."],
    install_requires=[
        "tkinter",
        "numpy==1.24.4",
        "pandas==2.0.3",
    ],
    entry_points={
        'console_scripts': [
            'modernmultitool = main:main',
        ],
    },
)
