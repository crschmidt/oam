#!/bin/sh -x

for scene in `cat scenes`;
    do
        OUT=worldview-pre SAT=Worldview-2/Pre-Event SCENE_ID=$scene nice -n 19 ./dg-general.sh
    done
