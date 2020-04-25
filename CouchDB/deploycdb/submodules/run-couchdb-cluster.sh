#!/bin/bash

#Set node IP addresses, electing the first as "master node" and admin credentials 
#(make sure you have no other Docker containers running):
export declare -a nodes=(172.17.0.4 172.17.0.3 172.17.0.2)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user=admin
export pass=admin
export VERSION='3.0.0'
export cookie='a192aeb9904e6590849337933b000c99'
export uuid='a192aeb9904e6590849337933b001159'

echo "Install couchDB3"
docker pull ibmcom/couchdb3:${VERSION}


#Create Docker containers (stops and removes the current ones if existing):
echo ""
echo "- Create Docker containers, stops and removes the current ones if existing"
for node in "${nodes[@]}" 
  do
    if [ ! -z $(docker ps --all --filter "name=couchdb${node}" --quiet) ] 
       then
         docker stop $(docker ps --all --filter "name=couchdb${node}" --quiet) 
         docker rm $(docker ps --all --filter "name=couchdb${node}" --quiet)
    fi 
done

for node in "${nodes[@]}" 
  do
    docker create\
      --name couchdb${node}\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env NOOENAME=couchdb@${node}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${node}\""\
      ibmcom/couchdb3:${VERSION}
done


#Put in conts the Docker container IDs:
echo ""
echo "- Put in conts the Docker container IDs:"
declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

#Start the containers (and wait a bit while they boot):
echo ""
echo "Start the containers"
for cont in "${conts[@]}"; do docker start ${cont}; done
sleep 30


#Set up the CouchDB cluster:
echo ""
echo "- Set up the CouchDB cluster"
echo "enable cluster"
for node in ${othernodes} 
do
    curl --noproxy "*"  -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\",\
             \"remote_node\": \"${node}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

echo "add cluster"
for node in ${othernodes}
do
    curl --noproxy "*" -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"${node}\",\
             \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done

echo "finish cluster"
curl --noproxy "*" -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"
	
#Check wether the cluster configuration is correct:
echo ""
echo "- Check wether the cluster configuration is correct"
for node in "${nodes[@]}"
do  
	echo "${node}:"
	curl --noproxy "*" -X GET "http://${user}:${pass}@${node}:5984/_membership"
done

#Adding a database to one node of the cluster makes it to be created on all other nodes as well:
echo "add a database"
curl --noproxy "*" -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
for node in "${nodes[@]}"; do  curl --noproxy "*" -X GET "http://${user}:${pass}@${node}:5984/_all_dbs"; done
