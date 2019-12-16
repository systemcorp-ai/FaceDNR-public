# FaceDNR

[![N|Solid](./dis.svg)](https://www.systemcorp.ai)



[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)]()

FaceDNR is a combination of Face Detection and Face Recognition frameworks. Therefore, FaceDNR stands for "Face Detection And Recognition".

[![N|Solid](./FaceDNR.svg)](https://www.systemcorp.ai)




# PROS
  - Built on OpenCV, SSD (Single Shot Detection) with the base model of ResNet50 - therefore it's fast
  - Runs Face Detection model for the whole time, and only when the face is detected, and stabilized, then runs the recognition model
  - Training takes about 1 minute for 100 images on Google Colab

# TODO

  - Edit pickle content.
  - Communication with Node.JS server by POSTing JSON - DONE
  - Transfer bounding boxes from detector, to save time - Better solution, DONE
  - Checkpoint module implementation
  - Eye blink detection for liveness detection / or other better solution, maybe gamma thresholding


### Used Frameworks & Libraries

FaceDNR is built on the technology in lighweight - accurate equillibrium:

* [OpenCV]
* [Single Shot Detection (SSD)]
* [ResNet50]
* [Node.JS] - for server-side communication


### Installation

Python 3.6+ and OpenCV 3 required to run.

Clone to the repository and install requirements.

```sh
$ git clone https://github.com/systemcorp-ai/FaceDNR.git
$ cd FaceDNR
$ pip install -r requirements.txt
```



### Usage

Use Google Colaboratory, with GPU accelerator.

# Steps

  - Take 1080p 4-5 seconds videos of faces to recognize
  - Upload them on Google Drive, to reach them via Colaboratory later on
 Go to 'dataset' directory:
```sh
$ cd dataset
```
   - Classify the videos to the corresponding folders. Folders' names will be taken as a lable later on, so make sure you're naming them correctly
   - For instance, for the name Luka Chkhetiani, I'll create folder with the same name, and move the video of his face to the directory

```sh
$ mkdir "Luka Chkhetiani"
$ mv IMG_001.MOV "Luka Chkhetiani"
```
- We have to use FFMPEG library to cut the video down to single images, extracted from every frame. In case of 30 FPS, we've to cut 30 frames from every second of the file.
- Go to the folder, and execute the next command

```sh
$ cd "Luka Chkhetiani"
$ ffmpeg -i IMG_001.MOV -vf fps=30 Luka Chkhetiani%d.png
```
- And remove the .MOV file, so it won't be mistakenly encoded during the training

```sh
$ rm IMG_001.MOV
```

After cutting and labeling the entire data, we need to get to the project main directory, and fine-tune the encoder by executing the next commands.

```sh
$ cd ../../
$ python encode_faces.py --dataset dataset --encodings encodings.pickle
```

# Output

```sh
$ Encoding faces...
$ Training FaceDNR Model. Iteration - 1/1000
$ Training FaceDNR Model. Iteration - 2/1000
$ Training FaceDNR Model. Iteration - 3/1000
$ Training FaceDNR Model. Iteration - 4/1000
$ Training FaceDNR Model. Iteration - 5/1000
$ Training FaceDNR Model. Iteration - 6/1000
...
$ Dumping the Encoder...
$ Training FaceDNR Model has been finished.
```

### We're done with training here.
### Download the entire directory on your local, so you're able to access the camera.

Colab doesn't support the X Server, and it'll throw error every time you'll execute the command, so use your Laptop/PC to test the model.

After downloading the model, and installing requirements, cd to the project directory, and execute the command:
```sh
$ python3 facednr.py
```

### The model will recognize the face in every 2 seconds.
### To quit, press CTRL + C on the Terminal/Command Line

# JSON Instance

The API sends the JSON array, that includes the names of the recognized people, and DateTime.

Example:

```sh
$ {"Recognized": ["Luka Chkhetiani"], "DateTime": "2019-05-11 11:31:59.482281"}
$ {"Recognized": ["Luka Chkhetiani"], "DateTime": "2019-05-11 11:31:59.482281"}
```

To send the POST request to desired url, you should change the "endpoint_url" in "recognizer_dnr.py"

```sh
endpoint_url = "http://httpbin.org/post" >> "http://desiredurl.com/post"
```


License
----

Apache 2.0




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
   [OpenCV]: <https://opencv.org>
   [Single Shot Detection (SSD)]: <https://arxiv.org/pdf/1512.02325.pdf>
   [ResNet50]: <https://arxiv.org/pdf/1512.03385.pdf>


   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
