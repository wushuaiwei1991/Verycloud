#!/bin/bash
BF_HT=`snmpwalk -Cc -v 1 -c public $1  1.3.6.1.4.1.10215.2.1.5.88.1.4.1.5.0.$2.1.1`
BF_0X=${BF_HT:99:2}
BF_1x=${BF_HT:96:2}
BF=$BF_1x$BF_0X
SF=$((0xfffffffffffffffffffff$BF))
RESUALT=$SF
echo $RESUALT
