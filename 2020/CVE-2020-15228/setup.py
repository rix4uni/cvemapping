import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fix-CVE-2020-15228",
    version="0.0.1",
    author="Thomas Guettler",
    author_email="guettliml@thomas-guettler.de",
    description="Fix CVE-2020-15228 by avoiding `set-env` and use `echo ... > $GITHUB_ENV`",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guettli/fix-CVE-2020-15228",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'fix_CVE_2020_15228=fix_CVE_2020_15228:main',
            'fix_CVE_2020_15228-test=fix_CVE_2020_15228:test',
        ],
    },
)
