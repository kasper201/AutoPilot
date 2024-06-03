
# import the opencv library 
import cv2 
  
  
# define a video capture object 
vid = cv2.VideoCapture(0)
image = cv2.imread('selfie.jpg')

# Display the image
cv2.imshow('Image', image)

#doublecheck
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 100, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.rectangle(vid, (10, 10), (20 + 20 , 20 + 20), (0, 0, 255), 10)
    return faces

while True:
    # read frames from the video
   
    result, video_frame = vid.read()
    if result is False:
        break  # terminate the loop if the frame is not read successfully
     
    #applies the function
    faces = detect_bounding_box(
        video_frame
    )

    cv2.imshow(
        "Test", video_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()

'''
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
'''
