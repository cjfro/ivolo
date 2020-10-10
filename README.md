# ivolo
Distributed LED visualizations on Raspberry PIs

![image](https://user-images.githubusercontent.com/658544/94959611-6434b900-04e9-11eb-90bb-8d1f77263271.png)

## Raspberry PI install

Install Raspberry PI WS281X LED drivers:
```
sudo pip install rpi_ws281x
```

or ..

```
git clone https://github.com/jgarff/rpi_ws281x.git
sudo apt install scons swig
cd rpi_ws281x
scons
cd python
sudo -H python setup.py build
sudo -H python setup.py install
```
