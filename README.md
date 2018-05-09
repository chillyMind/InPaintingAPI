## InPaintingAPI
chillyMind/[Context-Encoder](http://cs.berkeley.edu/~pathak/context_encoder/)의 RestfulAPI

### REQUIREMENT
```Shell
python 3.6
pytorch & torchvision
CUDA / CUDNN
```

### nodeJS 서버 실행
```Shell
$npm start
```

### python 데몬 실행
```Shell
$cd netmodels
$python python_daemon.py
```

### API 요청
```Shell
URL: /upload
METHOD: post
ENC: multipart/form-data
KEY-TYPE: file
KEY-NAME: upfile
```

### IMAGE 인풋제한
```Shell
PNG file with 4 channel (RGBA)
```

