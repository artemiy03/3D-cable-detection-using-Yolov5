# For choosing specific files modify lines: 36, 55, 74, 75, 76, 77

from PIL import Image, ImageDraw

def yolo_to_corners(x_center, y_center, width, height):
    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2
    return x_min, y_min, x_max, y_max

def intersect_to_yolo(x_min1, y_min1, x_max1, y_max1, x_min2, y_min2, x_max2, y_max2):
    # Calculate intersection box corners
    x_min = max(x_min1, x_min2)
    y_min = max(y_min1, y_min2)
    x_max = min(x_max1, x_max2)
    y_max = min(y_max1, y_max2)

    #Check if there is an intersection #If no intersection it returns None
    if x_min < x_max and y_min < y_max:
        # Convert to YOLO format
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min
        return x_center, y_center, width, height
    return None

conservative = True
pass_conf_rgb = 0.35 # in case of conservative, type the minimum confidence value for rgb
pass_conf_d = 0.35 # in case of conservative, type the minimum confidence value for depth
permissive = True
any = True
    
# Load text file of RGB image with bounding boxes
file_path_rgb = 'runs/detect/exp/labels/rgb2.txt'
dataRGB = []

with open(file_path_rgb, 'r') as file:
    for line in file:
        values = line.split()
        
        if len(values) == 6:
            class_idRGB = int(values[0])
            x_centerRGB = float(values[1])
            y_centerRGB = float(values[2])
            widthRGB = float(values[3])
            heightRGB = float(values[4])
            confRGB = float(values[5])
            
            if class_idRGB == 0:
                dataRGB.append((class_idRGB, x_centerRGB, y_centerRGB, widthRGB, heightRGB, confRGB))

# Load text file of depth image with bounding boxes
file_path_depth = 'runs/detect/exp2/labels/depth2.txt'
datadepth = []

with open(file_path_depth, 'r') as file:
    for line in file:
        values = line.split()
        
        if len(values) == 6:
            class_idD = int(values[0])
            x_centerD = float(values[1])
            y_centerD = float(values[2])
            widthD = float(values[3])
            heightD = float(values[4])
            confD = float(values[5])
            
            if class_idD == 0:
                datadepth.append((class_idD, x_centerD, y_centerD, widthD, heightD, confD))

# Open the clean RGB image to draw the intersections
img_path = 'data/combined/rgb_test/rgb2.png'
output_img_path_conservative = 'runs/conservative/final2.png' 
output_img_path_permissive =  'runs/permissive/final2.png'
output_img_path_any = 'runs/any/final2.png'
image = Image.open(img_path)
draw = ImageDraw.Draw(image)

# Find overlapping bounding boxes, create new bounding boxes that are contained in both rgb and depth, and draw them on the clean image
if conservative :
    print("New bounding boxes representing intersections:")
    img_width, img_height = image.size
    for (class_idRGB, x_centerRGB, y_centerRGB, widthRGB, heightRGB, confRGB) in dataRGB:
        if confRGB > pass_conf_rgb:  
            rgb_corners = yolo_to_corners(x_centerRGB, y_centerRGB, widthRGB, heightRGB)
    
            for (class_idD, x_centerD, y_centerD, widthD, heightD, confD) in datadepth:
                if confD > pass_conf_d:
                    depth_corners = yolo_to_corners(x_centerD, y_centerD, widthD, heightD)
        
                    # Get the intersection box if there is an overlap
                    intersection = intersect_to_yolo(*rgb_corners, *depth_corners)
                    if intersection:
                        x_center, y_center, width, height = intersection
                        print(f"Intersection box: class_id=0, x_center={x_center:.6f}, y_center={y_center:.6f}, width={width:.6f}, height={height:.6f}")
            
                        # Convert YOLO format to corner coordinates for drawing
                        x_min, y_min, x_max, y_max = yolo_to_corners(x_center, y_center, width, height)
            
                        # Scale coordinates based on the image size
                        x_min *= img_width
                        y_min *= img_height
                        x_max *= img_width
                        y_max *= img_height
            
                        # Draw the bounding box
                        draw.rectangle([x_min, y_min, x_max, y_max], outline="green", width=2)

    # Save the image with drawn bounding boxes
    image.save(output_img_path_conservative)
    print(f"Saved image with bounding boxes at {output_img_path_conservative}")

# Find bounding boxes of rgb and depth independentely and if there is any intersection, draw both of them on the clean image
if permissive:
    print("New bounding boxes representing intersections:")
    img_width, img_height = image.size
    for (class_idRGB, x_centerRGB, y_centerRGB, widthRGB, heightRGB, confRGB) in dataRGB:
        rgb_corners = yolo_to_corners(x_centerRGB, y_centerRGB, widthRGB, heightRGB)
    
        for (class_idD, x_centerD, y_centerD, widthD, heightD, confD) in datadepth:
            depth_corners = yolo_to_corners(x_centerD, y_centerD, widthD, heightD)
        
            # Check if there is any intersection box if there is an overlap
            intersection = intersect_to_yolo(*rgb_corners, *depth_corners)
            if intersection: 
                print(f"Intersection box1: class_id=0, x_center={x_centerRGB:.6f}, y_center={y_centerRGB:.6f}, width={widthRGB:.6f}, height={heightRGB:.6f}")
                print(f"Intersection box2: class_id=0, x_center={x_centerD:.6f}, y_center={y_centerD:.6f}, width={widthD:.6f}, height={heightD:.6f}")
            
                # Convert YOLO format to corner coordinates for drawing
                x_min1, y_min1, x_max1, y_max1 = yolo_to_corners(x_centerRGB, y_centerRGB, widthRGB, heightRGB)
                x_min2, y_min2, x_max2, y_max2 = yolo_to_corners(x_centerD, y_centerD, widthD, heightD)
            
                # Scale coordinates based on the image size
                x_min1 *= img_width
                y_min1 *= img_height
                x_max1 *= img_width
                y_max1 *= img_height
                x_min2 *= img_width
                y_min2 *= img_height
                x_max2 *= img_width
                y_max2 *= img_height
            
                # Draw the bounding box
                draw.rectangle([x_min1, y_min1, x_max1, y_max1], outline="yellow", width=2)
                draw.rectangle([x_min2, y_min2, x_max2, y_max2], outline="yellow", width=2)

    # Save the image with drawn bounding boxes
    image.save(output_img_path_permissive)
    print(f"Saved image with bounding boxes at {output_img_path_permissive}")

    
# Find bounding boxes of rgb and depth independentely and draw both of them on the clean image
if any:
    print("New bounding boxes representing intersections:")
    img_width, img_height = image.size
    for (class_idRGB, x_centerRGB, y_centerRGB, widthRGB, heightRGB, confRGB) in dataRGB:
        rgb_corners = yolo_to_corners(x_centerRGB, y_centerRGB, widthRGB, heightRGB)
    
        for (class_idD, x_centerD, y_centerD, widthD, heightD, confD) in datadepth:
            depth_corners = yolo_to_corners(x_centerD, y_centerD, widthD, heightD)
         
            print(f"Intersection box1: class_id=0, x_center={x_centerRGB:.6f}, y_center={y_centerRGB:.6f}, width={widthRGB:.6f}, height={heightRGB:.6f}")
            print(f"Intersection box2: class_id=0, x_center={x_centerD:.6f}, y_center={y_centerD:.6f}, width={widthD:.6f}, height={heightD:.6f}")
            
            # Convert YOLO format to corner coordinates for drawing
            x_min1, y_min1, x_max1, y_max1 = yolo_to_corners(x_centerRGB, y_centerRGB, widthRGB, heightRGB)
            x_min2, y_min2, x_max2, y_max2 = yolo_to_corners(x_centerD, y_centerD, widthD, heightD)
            
            # Scale coordinates based on the image size
            x_min1 *= img_width
            y_min1 *= img_height
            x_max1 *= img_width
            y_max1 *= img_height
            x_min2 *= img_width
            y_min2 *= img_height
            x_max2 *= img_width
            y_max2 *= img_height
            
            # Draw the bounding box
            draw.rectangle([x_min1, y_min1, x_max1, y_max1], outline="red", width=2)
            draw.rectangle([x_min2, y_min2, x_max2, y_max2], outline="red", width=2)

    # Save the image with drawn bounding boxes
    image.save(output_img_path_any)
    print(f"Saved image with bounding boxes at {output_img_path_any}")