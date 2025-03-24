from setuptools import setup, find_packages

setup(
    name="orca_slicer_settings_generator",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "scikit-learn",
        "numpy",
        "pandas",
        "werkzeug",
    ],
    author="Manus AI",
    author_email="info@example.com",
    description="AI-powered settings generator for Orca Slicer with Klipper support",
    keywords="3d printing, orca slicer, klipper, ai, settings",
    url="https://github.com/yourusername/orca-slicer-settings-generator",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
