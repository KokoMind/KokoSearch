#!/bin/bash

clear

echo "Compiling KOKOCRAWLER CODE"
echo "YARAB"

rm classes/*.class

javac -cp ".:1.jar:2.jar:3.jar:4.jar:5.jar:6.jar:7.jar:8.jar:9.jar:10.jar:11.jar:12.jar" *.java -d classes

echo "DONE"