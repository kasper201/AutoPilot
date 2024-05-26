import cv2 
import requests
  
  
# define a video capture object 
url = "http://192.168.137.223:8080/"
vid = cv2.VideoCapture(url)
count = 0

while True:
    # read frames from the video
    result, video_frame = vid.read()
    count = count + 1
    print(count)
    if count == 10: #Per aantal frames er een reactie verstuurd wordt
        vid.release()
        requests.get(url, params={"command": "HELLO"}, timeout=5)
        print("Send")
        count = 0
        vid = cv2.VideoCapture(url)
    if result is False:
        break  # terminate the loop if the frame is not read successfully
    #print(video_frame)
    #applies the function

    cv2.imshow(
        "Test", video_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()