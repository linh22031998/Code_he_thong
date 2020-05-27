import time
import cv2
import numpy as np
import time


classes="./data/labels/classes_full.names"

# classes="./data/labels/classes.names"
with open(classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes)*2, 3))

def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    

    label = str(classes[class_id])
    color = COLORS[class_id]
    # color = (0, 0, 255)
    # print(confidence)
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label+": "+str(round(confidence, 2)), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 4)
    # cv2.putText(img,"'"+label+"'", (x + 1, y + 1), cv2.FONT_HERSHEY_COMPLEX, 1, color, 3)
start = time.time()



image = cv2.imread("./data/images/test20.jpg")


scale = 0.00392
net = cv2.dnn.readNet("models/weights/yolov3-spp3_95_50.weights", "models/configs/prune_95_50.cfg")

# net = cv2.dnn.readNet("./models/yolov3.models", "./models/yolov3.cfg")
blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(get_output_layers(net))



class_ids = []
confidences = []
boxes = []
conf_threshold = 0.4
nms_threshold = 0.4



Width = image.shape[1]
Height = image.shape[0]
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        # print(scores)
        confidence = scores[class_id]
        if confidence > 0.2:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])

indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    i = i[0]
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
end = time.time()
print("time:", end-start)
# image = cv2.resize(image, (480, 720))
# cv2.imshow("object-detection", image)
# cv2.waitKey(0)
cv2.imwrite("Detected_image.jpg", image)
# cv2.destroyAllWindows()