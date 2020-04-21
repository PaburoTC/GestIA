sudo su
source venv/bin/activate
source /opt/intel/openvino/bin/setupvars.sh
python object_detection_demo_ssd_async.py  -d CPU
python object_detection_demo_ssd_async.py  -d GPU
