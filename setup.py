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
    license="WHAT",
    version="0.0.0.1",
    description="A static post generator, for when you don't feel like generating an entire site",
    author="Dan Nguyen",
    author_email="dansonguyen@gmail.com",
    url="https://github.com/dannguyen/writhub",
    packages=["writhub"],
    install_requires=["click>=7.1.2",],
    entry_points = {
        'console_scripts': ['writhub=writhub.console.cli:main'],
    },
    cmdclass={
        'npm_install_markdown_toc': NPMInstallMarkdownToc
    },
)




setup(**kwargs)
