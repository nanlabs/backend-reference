#!/bin/sh

alembic -c alembic.ini upgrade head

python main.py
