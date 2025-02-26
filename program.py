from pynput.keyboard import Key, Listener
from operator import itemgetter
import mss.tools
from PIL import Image
import pokemonTypeEffectivenesModule
import pytesseract
import win32security
import ntsecuritycon as con
import os
from rapidfuzz import process
userx, domain, type = win32security.LookupAccountName ("", "Everyone")
import pokemonNamesAndTypesModule

directory_name = "images"
directory_name_and_path = f'./{directory_name}'
pokemon_img_name = "name_of_pokemon"
pokemon_img_name_with_format = f'{pokemon_img_name}.png'
relative_image_path = f'{directory_name_and_path}/{pokemon_img_name_with_format}'

# TODO: Should probably have a tool to get these values in order to make it easy to use.
crop_values = {"top": 145, "left": 600, "width": 200, "height": 45}

def main():
    if os.path.exists(directory_name_and_path) == False:
            create_image_folder()
    with Listener(on_release=on_release) as listener:
        listener.join()

def on_release(key):
    """
    A listener for keyboard input. If the user clicks `F7` the process will begin and extract an image from the specified `crop_values` values. If the user clicks `f8` the program will stop running.
    """
    if key == Key.f8:
        print("Stop screen crop")
        # Stop listener
        return False
    elif key == Key.f7:
        print("Start screen crop")
        find_pokemon_info()

def create_image_folder():
    """
    Function for creating the folder to store the images we 're saving later on.
    """
    try: 
        os.mkdir(directory_name_and_path)
        print(f"Made folder called ''{directory_name} successfully")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_image():
    """
    Function for saving an image based on the position of the `crop_values` values
    """
    with mss.mss() as sct:
        output = relative_image_path.format(**crop_values)
        # Grab the data
        sct_img = sct.grab(crop_values)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print("Saved iamge: ",output)
        set_permission()

def set_permission():
    """
    This function should change the permissions of the file on the path 'relative_image_path'.

    The reason for needing to do this is beacuse PyTesseract needs execution permission on the image in order for it to be used for OCR.
    """
    sd = win32security.GetFileSecurity(relative_image_path, win32security.DACL_SECURITY_INFORMATION)
    dacl = sd.GetSecurityDescriptorDacl()   # instead of dacl = win32security.ACL()
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, userx)
    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(relative_image_path, win32security.DACL_SECURITY_INFORMATION, sd)

def make_image_black_white():
    """
    This function should loop through each pixel of the image. If the RGB (Red, Green, Blue) value is not equal to the color White, i.e (255, 255, 255), it should change the color of the pixel to be black, i.e (0, 0, 0)
    """
    image = Image.open(relative_image_path)
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r,g,b = image.getpixel( (x,y) )
            if r == 255 & g == 255 & b == 255:
                continue
            image.putpixel( (x,y), 0)
    return image.save(relative_image_path)

def perform_ocr_on_image():
    """
    This function will use PyTesseracts module for performing OCR (Optical Character Recognition) on the image we've saved.

    Will return an exrtacted word.
    Note: The word will in most cases NOT be properly spelled in comparison to the name of the pokemon
    """
    image = Image.open(relative_image_path)
    return pytesseract.image_to_string(image)

def process_image():
    """
    Collector function for keeping functions that process the saved image contained
    """
    make_image_black_white()
    return perform_ocr_on_image()

def find_pokemon_object(name):
    """
    The function should find the pokemon object from the pokemon_names array in the pokemonNamesAndTypesModule file.

    It will return the object on the format { name: string, type1: string, type2: string | None }
    """
    match = process.extractOne(name, pokemonNamesAndTypesModule.pokemon_names)
    new_pokemon_name = match[0]
    index = pokemonNamesAndTypesModule.pokemon_names.index(new_pokemon_name)
    return pokemonNamesAndTypesModule.pokemon_list[index]

def find_pokemon_info():
    """
    Top-level function for fetching the name of the pokemon based on the saved image
    """
    # save_image()
    pokemon_name = process_image()
    # Extract the name and types into seperate variables
    type1, type2 = itemgetter('name', 'type1', 'type2')(find_pokemon_object(pokemon_name.lower()))
    super_effective, normal, not_very_effective, no_effect = itemgetter('super_effective','normal', 'not_very_effective', 'no_effect')(pokemonTypeEffectivenesModule.calculate_type_effectiveness(type1, type2))
    print('Super effective: ', super_effective)
    print('Normal: ', normal)
    print('Not very effective', not_very_effective)
    print('No effect: ', no_effect)

if __name__ == "__main__":
    main()

# TODO: Display the final result in some GUI or something
