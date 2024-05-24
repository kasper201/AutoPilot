import cv2 
import requests
  
  
# define a video capture object 
url = "http://192.168.137.154:8080/"
vid = cv2.VideoCapture("http://192.168.137.154:8080/")

while True:
    # read frames from the video
    result, video_frame = vid.read()
    requests.get(url, params={"command": command}, timeout=1.3)
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