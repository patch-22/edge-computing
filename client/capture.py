import cv2
from turbojpeg import TurboJPEG

class CaptureManger:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

        # Grab a single frame
        if self.camera.isOpened():
            self.native_width = self.camera.get(3)
            self.native_height = self.camera.get(4)
            self.native_fps = self.camera.get(cv2.CAP_PROP_FPS)
    
        self.encoder = TurboJPEG() # NOTE: Can include raw library path in needed
        self.jpeg_compression = 30

        # Burn some frames
        for _ in range(20):
            self.get_frame()

    def get_frame(self):
        ref, frame = self.camera.read()
        return frame


    def encode(self):
        frame = self.get_frame()
        image = self.encoder.encode(frame, quality=self.jpeg_compression)

        return image


class CompressedCaptureManager(CaptureManger):
    def __init__(self):
        super().__init__()

    def get_frame(self):
        frame = super().get_frame()

        # Perform the compression

        return frame
