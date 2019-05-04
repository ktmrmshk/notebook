# notebook

```
$ docker run --rm -p8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work   -it jupyter/scipy-notebook

Ctrl-P Ctrl-Q for detach
```