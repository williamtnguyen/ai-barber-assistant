import { useRef } from 'react';
import Webcam from 'react-webcam';
import { Button } from './button';

interface WebcamModalProps {
  isOpen: boolean;
  onClose: () => void;
  onPhotoCapture?: (photoData: string, photoKey: string) => void;
}

const WebcamCapture: React.FC<WebcamModalProps> = ({ isOpen, onClose, onPhotoCapture }) => {
  const webcamRef = useRef<Webcam>(null);

  const capturePhoto = () => {
    if (webcamRef.current) {
      const photoData = webcamRef.current.getScreenshot();
      
      if (photoData) {
        // Create download link
        const link = document.createElement('a');
        link.href = photoData;
        const photoKey = `facecapture-${Date.now()}.jpg`;
        link.download = photoKey
        link.click();

        // If callback provided, send photo data for side effects
        if (onPhotoCapture) {
          onPhotoCapture(photoData, photoKey);
        }

        // Close modal
        handleClose();
      }
    }
  };

  const handleClose = () => {
    setTimeout(onClose, 300);
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="relative flex flex-col">
        <Button variant="outline" onClick={handleClose} className="absolute right-2 top-0 mb-1">❌</Button>
        <div className="flex flex-col items-center">
          <div>
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={640}
              height={480}
            />
          </div>
          <div>
            <Button variant="outline" className="mt-5 mb-5" onClick={capturePhoto}>
              📸 Take Photo
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};

export default WebcamCapture;
