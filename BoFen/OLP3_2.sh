#!/bin/bash
BF_HT=`snmpwalk -Cc -v 1 -c public $1  1.3.6.1.4.1.10215.2.1.5.88.1.4.1.5.0.$2.1.1`
BF_0X=${BF_HT:112:2}
BF_1X=${BF_HT:115:2}
BF=$BF_1X$BF_0X
#BF=ff$BF_0X
SF=$((0xfffffffffffffffffffffff$BF))
RESUALT=$SF
echo $RESUALT

