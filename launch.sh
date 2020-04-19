sudo su
source venv/bin/activate
source /opt/intel/openvino/bin/setupvars.sh
python object_detection_demo_ssd_async.py -m gestures_inference_graph_16Abril_10am/ir/fp32/frozen_inference_graph.xml -d CPU -i cam --labels gesture_labels.txt
python object_detection_demo_ssd_async.py -m gestures_inference_graph_16Abril_10am/ir/fp16/frozen_inference_graph.xml -d GPU -i cam --labels gesture_labels.txt -pt 0.8
