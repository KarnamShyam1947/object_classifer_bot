import cv2
import labels

def load_model():
    file = 'dnn_model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    trained_model = 'dnn_model/frozen_inference_graph.pb'

    model = cv2.dnn_DetectionModel(trained_model, file)

    model.setInputSize(320, 320)
    model.setInputScale(1.0/ 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    return model

def detect_labels(img_path, confidence, model):
    response = dict()
    count = dict()

    img = cv2.imread(img_path)

    idx, conf, bbox = model.detect(img, confThreshold=confidence)

    if len(idx) == 0:
        response_str = 'Sorry, Unable to classify'
        response = None

    else:
        font = cv2.FONT_HERSHEY_PLAIN
        i=1
        for classes_idx, confidence, bboxs in zip(idx.flatten(), conf, bbox):
            class_name = labels.label.get(classes_idx, "Unknown")

            response[class_name] = max(response.get(class_name, 0), confidence)
            count[class_name] = count.get(class_name, 0) + 1

            x, y, w, h = bboxs

            crop_img = img[y:y+h, x:x+w]

            # cv2.imshow('crop_img', crop_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            cv2.imwrite(f'cropped/{class_name}{(i)}.png', crop_img)
            i = i + 1

            cv2.rectangle(img, bboxs, (255, 0, 0), thickness=2)
            cv2.putText(img, class_name, (bboxs[0]+10, bboxs[1]+40), font, fontScale=2, color=(0,255,0), thickness=2)


        response_str = 'The image contains '
        for i,j in count.items():
            response_str = response_str + f'{str(j)} {i} (conf: {round(response.get(i)*100, 2)}%), '

        # cv2.imshow('Result', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        cv2.imwrite('result.png', img)

    return response, response_str

def main():
    model = load_model()
    img_path = 'images/image.png'
    confidence = 0.6

    response, resp_str = detect_labels(img_path, confidence, model)

    print(resp_str)
    print(response)

if __name__ == '__main__' : 
    main()