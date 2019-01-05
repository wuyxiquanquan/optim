# optim
## Multi-process + Decorator
Run time analysis：Bottleneck in IO
```
isPreProcess = False if ioTime <= processTIme else True
bestNumWorker = kernelNum (not the hyperthreading in INTEL CPU)
```
![](1.png)
MP ver 1
![](3.png)
MP ver 2 (slightly faster than ver1)
![](2.png)
