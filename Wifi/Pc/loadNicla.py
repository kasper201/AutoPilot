import cv2 
  
  
# define a video capture object 
url = "http://192.168.137.96:8080/"
vid = cv2.VideoCapture("http://192.168.137.156:8080/")

while True:
    # read frames from the video
    result, video_frame = vid.read()
    if result is False:
        break  # terminate the loop if the frame is not read successfully
    print(video_frame)
    #applies the function

    cv2.imshow(
        "Test", video_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()