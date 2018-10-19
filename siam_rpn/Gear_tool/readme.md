

### 依赖
```
python3
tensorboardX
tensorflow
```


### tensorboard
```
tensorboard 会自动运行
open remote chrome:    /usr/bin/google-chrome-stable --no-sandbox
浏览器地址:              http://localhost:6006/

如果tensorboard未正常关闭:
        查询tensorboard进程号:    netstat -lpn |grep :6006
        杀进程:                  kill -9 XXXX
```