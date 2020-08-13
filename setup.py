# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.build_py import build_py

# https://stackoverflow.com/questions/42742991/how-setup-py-install-npm-module
class NPMInstallMarkdownToc(build_py):
    def run(self):
        self.run_command('npm install --save markdown-toc')
        build_py.run(self)

kwargs = dict(
    name="writhub",
    license="whatever",
    version="0.0.0.2",
    description="A static post generator, for when you don't feel like generating an entire site",
    author="Dan Nguyen",
    author_email="dansonguyen@gmail.com",
    url="https://github.com/dannguyen/writhub",
    packages=["writhub"],
    python_requires=">=3.7",
    install_requires=["click>=7.1.2",],
    cmdclass={
        'npm_install_markdown_toc': NPMInstallMarkdownToc
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3 :: Only",

    ],


    entry_points = {
        'console_scripts': ['writhub=writhub.cli:main'],
    },

)




setup(**kwargs)
