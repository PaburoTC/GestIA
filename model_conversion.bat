#My trained model

#python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\model_optimizer\mo_tf.py" --input_model=gestures_inference_graph_16Abril_10am\frozen_inference_graph.pb --transformations_config "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\model_optimizer\extensions\front\tf\faster_rcnn_support.json" --tensorflow_object_detection_api_pipeline_config gestures_inference_graph_16Abril_10am\pipeline.config --reverse_input_channels
#python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\model_optimizer\mo_tf.py" --input_model=gestures_inference_graph_16Abril_10am\frozen_inference_graph.pb --transformations_config "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\model_optimizer\extensions\front\tf\faster_rcnn_support.json" --tensorflow_object_detection_api_pipeline_config gestures_inference_graph_16Abril_10am\pipeline.config --reverse_input_channels --data_type=FP16





