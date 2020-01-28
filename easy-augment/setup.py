from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="easy-augment",
    version="1.0.2",
    description="End to end software to capture new objects using RGBD camera  and augment them to get a annotated dataset to train deep nets.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/santoshreddy254/realsense_augmentor",
    author="Santosh Muthireddy",
    author_email="santoshreddy45@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["easy_augment", "easy_augment.utils",
              "easy_augment.pc_utils", "easy_augment.gui", "easy_augment.data"],
    include_package_data=True,
    install_requires=["PyQt5", "opencv-python", "labelme", "tqdm", "joblib", "scipy", "matplotlib", "imutils", "numpy>=1.16", "pascal-voc-tools", "pascal-voc-writer", "pytest-qt",
                      "pyrealsense2", "python-pcl"],
    entry_points={
        "console_scripts": [
            "easy-augment=easy_augment.launch_tool:main",
        ]
    },
)
