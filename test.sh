#!/bin/bash

for ((i=0; i<100; i++)); do
	./test.py ${1}-$i
done
