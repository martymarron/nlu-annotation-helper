from setuptools import setup, find_packages

setup(
    name='nlu-annotation-helper',
    version='1.0.0',
    packages=find_packages(where="src", exclude=("tests",)),
    package_dir={"": "src"},
    install_requires=["langdetect"],
    extras_require={
        "dev": [
            "pytest",
            "pytest_mock"
        ]
    },
    entry_points="""\
    [console_scripts]
    nlu-annotation-helper = nlu_annotation_helper.cli:main
    """,
    author='Masashi Kurita (alias: maskurit@)',
    author_email='maskurit@amazon.co.jp'
)
