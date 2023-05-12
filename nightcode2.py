import time
import picamera
import picamera.array
import numpy as np
import pygame

# Set up the PiCamera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.color_effects = (128, 128) # Set to capture YUV format

# Initialize the Pygame display
pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width*2, screen_height), pygame.FULLSCREEN)

# Main loop for capturing and displaying frames
while True:
    # Capture a frame from the camera
    with picamera.array.PiYUVArray(camera) as stream:
        camera.capture(stream, format='yuv')
        # Extract the Y, U, and V components of the image
        yuv = stream.array
        frame_y = yuv[:, :, 0]
        frame_u = yuv[:, :, 1]
        frame_v = yuv[:, :, 2]

    # Convert the YUV components to RGB
    frame_rgb = np.dstack((frame_y, frame_u, frame_v)).astype(np.uint8)

    # Split the stereo image into left and right views
    left_frame = frame_rgb[:, :screen_width, :]
    right_frame = frame_rgb[:, screen_width:, :]

    # Convert the frames to Pygame surfaces
    left_surf = pygame.surfarray.make_surface(left_frame)
    right_surf = pygame.surfarray.make_surface(right_frame)

    # Blit the left and right surfaces to the screen
    screen.blit(left_surf, (0, 0))
    screen.blit(right_surf, (screen_width, 0))
    pygame.display.flip()

    # Exit if the user presses 'q'
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            camera.close()
            exit()

    # Wait for a little bit to prevent the Pi from overheating
    time.sleep(0.01)
