#!/bin/bash


pyreverse ./
dot -Tpng classes.dot -o tf_classes.png
dot -Tpng packages.dot -o tf_packages.png
