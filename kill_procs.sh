#!/bin/bash
#
ps | awk {'print $1'} > pids
while read pid; do kill $pid; done < pids
rm pids
