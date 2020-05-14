# nohup python3 -u searchapi_controller.py -a 'api-1' >> harvester1.out 2>&1 &
# sleep 3
# nohup python3 -u searchapi_controller.py -a 'api-2' >> harvester2.out 2>&1 &
# sleep 3
# nohup python3 -u searchapi_controller.py -a 'api-3' >> harvester3.out 2>&1 &
# echo "success"


nohup mpiexec -n 2 python3 searchapi_controller_new.py -a 'api-1' >> harvester1.out 2>&1 &
sleep 3
nohup mpiexec -n 2 python3 searchapi_controller_new.py -a 'api-2' >> harvester2.out 2>&1 &
sleep 3
nohup mpiexec -n 2 python3 searchapi_controller_new.py -a 'api-3' >> harvester3.out 2>&1 &
echo "success"