#!/bin/sh -x

for scene in `cat scenes`;
    do
        OUT=quickbird-pre SAT=Quickbird/Pre-Event SCENE_ID=$scene ./dg-general.sh
    done
