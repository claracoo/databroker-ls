import time
import curses
import os

from time import sleep
from sys import stdout

for i in range(1,20):
    stdout.write("\r%d" % i)
    stdout.flush()
    sleep(1)
stdout.write("\n") # move the cursor to the next line

# width, height = os.get_terminal_size()
#
# N=12
#
# for i in range(N):
#    sleep(0.5)
#    print(f"{i/N*100:.1f} %", end="\r")

# def pbar():
#     reallyLongStr = "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you'd expect to be involved in anything strange or mysterious, because they just didn't hold with such nonsense. Mr. Dursley was the director of a firm called Grunnings, which made drills. He was a big, beefy man with hardly any neck, although he did have a very large mustache. Mrs. Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful as she spent so much of her time craning over garden fences, spying on the neighbors. The Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. The Dursleys had everything they wanted, but they also had a secret, and their greatest fear was that somebody would discover it. They didn't think they could bear it if anyone found out about the Potters. Mrs. Potter was Mrs. Dursley's sister, but they hadn't met for several years; in fact, Mrs. Dursley pretended she didn't have a sister, because her sister and her good-for-nothing husband were as unDursleyish as it was possible to be. The Dursleys shuddered to think what the neighbors would say if the Potters arrived in the street. The Dursleys knew that the Potters had a small son, too, but they had never even seen him. This boy was another good reason for keeping the Potters away; they didn't want Dudley mixing with a child like that."
#     reallyLongStr = reallyLongStr.replace(" ", "\n")
#     print(reallyLongStr, end='\r')
#
# pbar()
