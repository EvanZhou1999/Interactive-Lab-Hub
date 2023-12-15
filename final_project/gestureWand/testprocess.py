import pygame
import threading

testvar = 0

# Your time-consuming function
def long_running_function():
    global testvar
    # Simulate a long-running task
    pygame.time.wait(5000)
    testvar = 5
    print("Long-running function completed")

# Initialize pygame
pygame.init()

# Set up your game window and other necessary variables

# Function to start the long-running function in a separate thread
def run_long_running_function():
    thread = threading.Thread(target=long_running_function)
    thread.start()

run_long_running_function()
# Your game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Call the function to start in a separate thread
                run_long_running_function()

    print(testvar)
    # Update game graphics here

# Quit pygame
pygame.quit()
