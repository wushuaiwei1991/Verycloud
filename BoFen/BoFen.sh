#!/bin/bash
BF_HT=`snmpwalk -Cc -v 1 -c public $1  1.3.6.1.4.1.10215.2.1.5.88.1.4.1.5.0.$2.1.1`
BF_0X=${BF_HT:96:2}
BF_1X=${BF_HT:93:2}
BF=$BF_0X$BF_1X
SF=$((0xfffffffffffffffffffff$BF))
RESUALT=$SF
echo $RESUALT

