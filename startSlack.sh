#!/bin/bash
#source /home/neale/.bashrc
sleep 60 # Waiting for the computer to establish internet connection. Otherwise the client won't be able to operate properly.
sudo -u neale /home/neale/anaconda3/bin/python /home/neale/TestProject/slackTest.py
