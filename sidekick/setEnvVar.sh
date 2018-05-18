#!/bin/bash
echo "Enter variable name: "
read variable_name
echo "Enter variable value: "
read variable_value
echo "adding " $variable_name " to environment variables: " $variable_value
export $variable_name=$variable_value
echo "export "$variable_name"="$variable_value>>~/.bashrc
echo $variable_name"="$variable_value>>~/.profile
echo $variable_name"="$variable_value>>/etc/environment
source ~/.bashrc
source ~/.profile
echo "don't forget to restart your computer manually"
exit