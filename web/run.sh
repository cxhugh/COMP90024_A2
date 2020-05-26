###################################################################################################################################
##Project: COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities Analytics on the Cloud
##Purpose:  to find out the correlations between alcohol-related tweets and demographic 
##          and behavioural characteristics in Australia cities.
##Team: group05-- Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia YIN (1017231), Fang Qu (1070888)
###################################################################################################################################

#!/bin/bash

export FLASK_APP=webserver.py
filename="./generic.yaml"
while read line
do
    if ( echo ${line} |grep -q "webServer");then ips="$line";fi

done < $filename
ip=""
ip=`echo $ips | awk '{print $2}'`
echo $ip

nohup flask run --host="$ip" > nohup.out 2>&1 &