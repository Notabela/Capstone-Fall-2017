## Blink Detection Code

A simple demo of how Python Open CV can be used to detect the blink rate of a subject in a video

### Usage

##### Setup Environment
    pip install -r requirements.txt
    
    Application requires CMake and Boost
    
    Mac oS
    brew uninstall boost
    brew uninstall boost-python
    brew install boost-python --with-python3 --without-python

##### Run Application (debug Mode)
    python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat --video --[Video File]
