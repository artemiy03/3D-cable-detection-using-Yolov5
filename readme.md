# 3D Cable Detection in 3D Environments Using YOLOv5
##
**Overview**
##
This project is a module for detecting thin, deformable 3D objects (specifically cables) in a 3D environment using YOLOv5. We utilize a 3D camera that captures the same scene twice: once as a 2D RGB image and once as a depth image. Since YOLOv5 operates on 2D data, we process the 2D RGB and depth images separately with distinct models trained on each type of data. The depth data is represented as a 2D image where each color corresponds to a specific depth value, effectively encoding distance information using color gradients. This format allows the YOLOv5 network to be trained on depth images in the same manner as standard 2D images, leveraging its capabilities for object detection.
##
**Contents**
##
Beside an original yolov5 module, there are 2 weights named "final.pt" and "depth1.pt" in the weights folder, final.py code to run the fusion part of the module and few example images in the data/combined folders. In this path there are two folders: rgb and depth, they contain the same scenes captured once by the rgb module of the camera and once by the depth module of the camera. You can find additional marked with bounding boxes depth and regular 2D RGB images at my roboflow account: https://app.roboflow.com/artemiy
##
**Camera and Data**
##
The 3D camera outputs:  
2D RGB Image- Standard image of the scene in RGB format.  
Depth Image- A 2D image where color intensity represents different depth levels.
##
**Trained Weights**
##
We have two separate YOLOv5 models:  
RGB Model- Trained on 2D RGB images.  
Depth Model- Trained on depth images, where colors represent depth levels.  
Both models were trained on the Roboflow platform. You can access the datasets used for training here.
##
**Detection Process**
##
Use the detect.py script from the YOLOv5 package to run detections separately on the 2D RGB and depth images. Each run of detect.py produces a .txt file containing the classes, bounding boxes, and confidence levels for each detection.  
Example command:  
bash  
python3 detect.py --weights ./weights/final0.pt --source /home/art/yolov5/data/combined/rgb_test/rgb2.png --save-txt --save-conf  
python3 detect.py --weights ./weights/depth1.pt --source /home/art/yolov5/data/combined/depth_test/depth2 --save-txt --save-conf  
##
**Fusion Mechanism**
##
After obtaining the detection results from both the RGB and depth networks, we use final.py to fuse the outputs and generate new bounding boxes based on three different voting mechanisms:
Conservative Mode: Marks green bounding boxes only where there is an intersection between the 2D RGB and depth detections, ensuring high confidence in the detected areas.  
Permissive Mode: Designed to handle the weaknesses of individual networks that are mostly missed detections. If there is any intersection between the bounding boxes from the 2D RGB and depth outputs, both bounding boxes are marked in yellow on the clean 2D RGB image.  
Any Mode: Prints all bounding boxes from both the 2D RGB and depth network outputs in red, without requiring any intersection.
##
**Running the Fusion**
##
Run final.py script, it is set up to work directly with the required file paths, and you can easily adjust these paths by following the instructions in the code. The voting options (conservative, permissive, any) can be toggled on or off.  
The input at this part are the .txt files of the 2D RGB and depth detections by yolov5, that were recieved at the stage "Detection process" and the output are new clear 2D images with bounding boxes marked by any of the voting mechanisms provided in final.py. They will be located in /runs path in relevant folders. All these paths are provided in final.py and easy adjustable. The confidence threshold and voting mechanism can be adjusted within final.py as needed.  
##
**Citation**
##
If you use this project in your research, please cite it as follows:  
BibTeX entry for academic papers:  
```bibtex  
@misc{tomanov2024cabledetection,  
  author = {Tumanov, Artemiy},    
  title = {3D Cable Detection Using YOLOv5},  
  year = {2024},  
  howpublished = {\url{https://github.com/artemiy03/3D-cable-detection-using-Yolov5}},  
  note = {GitHub repository}  
}
##
**Acknowledgments**
##
The YOLOv5 model used in this project is provided by Ultralytics. Please acknowledge the YOLOv5 model as follows:
```bibtex  
@misc{jocher2023yolov5,  
  title={YOLOv5: You Only Look Once version 5},  
  author={Jocher, G. and Chaurasia, A. and Qiu, J. and LeGrand, A.},  
  year={2023},  
  howpublished={\url{https://github.com/ultralytics/yolov5}},  
  note={Accessed: 2024-11-15}  
}
