#!/usr/bin/env python3
import click

@click.command()
def main():
    click.secho("The main foo", bg='black', fg='blue')

if __name__ == '__main__':
    main()
