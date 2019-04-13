# What is my sag ?

This minimal module in python3 computes the difference of height between the slackliner and anchors, depending on their position on the slackline, on elasticity, weight of the slackliner, and other parameters.
The use of the module is easy through the documented function main, and launching 
```
    python3 trajectory_slack.py
```
lets you visualize the heights the slackliner went through.
Of course you can do whatever you want with the code.

The elasticity is assumed to be linear (which can be wrong, but we usually have only one value giving the elasticity under 10kN when buying a slackline)
