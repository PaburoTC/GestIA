from __future__ import print_function
from openvino.inference_engine import IENetwork, IECore
from argparse import ArgumentParser, SUPPRESS
import sys
import os
import cv2
import time


class InferenceModel:
    def __init__(self, cpu=True):
        model_xml = 'model/frozen_inference_graph.xml'
        model_bin = os.path.splitext(model_xml)[0] + ".bin"
        self.device_str = 'CPU' if cpu else 'null'
        self.ie = IECore()
        self.net = IENetwork(model=model_xml, weights=model_bin)
        if cpu:
            supported_layers = self.ie.query_network(self.net, "CPU")
            not_supported_layers = [l for l in self.net.layers.keys() if l not in supported_layers]
            if len(not_supported_layers) != 0:
                raise Exception('Layers not supported for CPU configuration',
                                "Following layers are not supported by the plugin for specified device {}:\n {}".
                                format(args.device, ', '.join(not_supported_layers)))

    def initialize(self):
        self.img_info_input_blob = None
        self.feed_dict = {}
        for blob_name in self.net.inputs:
            if len(self.net.inputs[blob_name].shape) == 4:
                self.input_blob = blob_name
            elif len(self.net.inputs[blob_name].shape) == 2:
                self.img_info_input_blob = blob_name
            else:
                raise RuntimeError("Unsupported {}D input layer '{}'. Only 2D and 4D input layers are supported"
                                   .format(len(self.net.inputs[blob_name].shape), blob_name))
        assert len(self.net.outputs) == 1, "This model supports only single output topologies"

        self.out_blob = next(iter(self.net.outputs))
        # Loading IR to the plugin...
        self.exec_net = self.ie.load_network(network=self.net, num_requests=2, device_name=self.device_str)
        # Read and pre-process input image
        self.n, self.c, self.h, self.w = self.net.inputs[self.input_blob].shape
        if self.img_info_input_blob:
            self.feed_dict[self.img_info_input_blob] = [self.h, self.w, 1]

        with open('data/gesture_labels.txt', 'r') as f:
            self.labels_map = [x.strip() for x in f]

        self.cur_request_id = 0
        self.next_request_id = 1

    def processFrame(self, frame):
        frame_h, frame_w = frame.shape[:2]
        in_frame = cv2.resize(frame, (self.w, self.h))
        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        in_frame = in_frame.reshape((self.n, self.c, self.h, self.w))
        self.feed_dict[self.input_blob] = in_frame
        self.exec_net.start_async(request_id=self.cur_request_id, inputs=self.feed_dict)
        det_label = 'nothing'
        if self.exec_net.requests[self.cur_request_id].wait(-1) == 0:
            res = self.exec_net.requests[self.cur_request_id].outputs[self.out_blob]
            for obj in res[0][0]:
                # Draw only objects when probability more than specified threshold
                if obj[2] > 0.6:
                    # keyboard.press_and_release('SPACE')
                    xmin = int(obj[3] * frame_w)
                    ymin = int(obj[4] * frame_h)
                    xmax = int(obj[5] * frame_w)
                    ymax = int(obj[6] * frame_h)
                    class_id = int(obj[1])

                    # Draw box and label\class_id
                    color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    det_label = self.labels_map[class_id] if self.labels_map else str(class_id)
                    # cv2.putText(frame, det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7),
                    #            cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
        return det_label
