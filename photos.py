import pygame
import os
import time
import json
import textwrap

def display_images_with_info(json_file_path, folder_path, delay=60):
    """
    Display images with overlaying information in full screen and change images every N seconds.

    Parameters:
    - json_file_path: Path to the JSON file containing image information.
    - folder_path: Path to the folder containing images.
    - delay: Time in seconds to wait before switching to the next image.
    """
    MAX_LINE_LENGTH=80

    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    print(f"Starting pygame",flush=True)
    # Initialize pygame
    pygame.init()
    print(f"Disabling mouse",flush=True)
    pygame.mouse.set_visible(False)

    # Get screen dimensions
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

    # Create a full screen display
    #screen = pygame.display.set_mode((800,600))
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Set up the font
    font = pygame.font.Font(None, 48)  # Choose the font size and style

    # Main loop
    running = True
    print(f"Starting main loop",flush=True)
    while running:
        for item in data:
            image_name = item.get('image_name')
            if image_name.lower().endswith('.tif'):
                image_name = image_name.rsplit('.',1)[0]+'.png'
            title = item.get('title')
            paragraph = item.get('paragraphs')
            image_file = os.path.join(folder_path, image_name)

            print(f"Looking for image {image_file}",flush=True)

            if not os.path.exists(image_file):
                print(f"Can't find the image..",flush=True)
                continue

            try:

                # Event handling to exit the slideshow (press ESC key or close button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # This checks if the pressed key is Escape
                            running = False
                            pygame.quit()
                            sys.exit()  # This terminates the script completely

                print(f"Loading image {image_file}",flush=True)
                # Load image and scale it to fullscreen
                image = pygame.image.load(image_file)
                image = pygame.transform.scale(image, (screen_width, screen_height))

                # Render the text
                title_surface = font.render(title, True, (255, 255, 255))  # White text

                # Position the text
                title_position = (screen_width - title_surface.get_width() - 50, title_surface.get_height() + 50)  # Lower right

                # Display image
                screen.blit(image, (0, 0))
                screen.blit(title_surface, title_position)
                
                for i, line in enumerate(paragraph):
                    line_fixed = ' '.join(line.replace('\n', '').split())
                    tmp_surface = font.render(line_fixed, True, (255, 255, 255))
                    # Position the text lines with some spacing
                    y_position = screen_height - (len(paragraph) - i) * 40 - 110  # Adjust the base position based on the number of lines
                    screen.blit(tmp_surface, (screen_width - tmp_surface.get_width() - 50, y_position))   
                    
                pygame.display.flip()

                # Wait for the specified delay
                time.sleep(delay)

                # Event handling to exit the slideshow (press ESC key or close button)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

            except Exception as e:
                print(f"Error displaying {image_file}: {e}",flush=True)

    pygame.quit()

# Example usage
json_file_path = "/home/sysop/image/all_image_info5.json"
folder_path = "/home/sysop/image/images/"
while True:
    display_images_with_info(json_file_path, folder_path, delay=60)
    print(r"Loop completed, starting over",flush=True)
