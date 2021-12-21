import pathlib

def load_input():
    return pathlib.Path("./input.txt").read_text().strip("\n").splitlines()

def enhance_image(image_enhancement_algorithm, input_image, infinite_state = "."):
    enlarged_image = []
    new_inifinite_state = "."
    for i in range(3):
        enlarged_image.append(infinite_state * (len(input_image[0]) + 6))
    for line in input_image:
        enlarged_line = infinite_state * 3 + line + infinite_state * 3
        enlarged_image.append(enlarged_line)
    for i in range(3):
        enlarged_image.append(infinite_state * (len(input_image[0]) + 6))

    if infinite_state == ".":
        new_inifinite_state = image_enhancement_algorithm[0]
    else:
        new_inifinite_state = image_enhancement_algorithm[-1]

    enhanced_image = []
    for i in range(1, len(input_image[0]) + 4):
        enhanced_line = ""
        for j in range(1, len(input_image) + 4):
            pixel_string = enlarged_image[i-1][j-1] + enlarged_image[i-1][j] + enlarged_image[i-1][j+1] \
                + enlarged_image[i][j-1] + enlarged_image[i][j] + enlarged_image[i][j+1] \
                    + enlarged_image[i+1][j-1] + enlarged_image[i+1][j] + enlarged_image[i+1][j+1]

            enhanced_number_string = pixel_string.replace(".", "0").replace("#", "1")
            enhanced_number = int(enhanced_number_string, 2)

            enhanced_pixel = image_enhancement_algorithm[enhanced_number]
            enhanced_line += enhanced_pixel
        enhanced_image.append(enhanced_line)

    return (enhanced_image, new_inifinite_state)

if __name__ == "__main__":
    input = load_input()

    image_enhancement_algorithm = input[0]
    initial_image = input[2:]

    (next_image, infinite_state) = enhance_image(image_enhancement_algorithm, initial_image)
    (next_image, infinite_state) = enhance_image(image_enhancement_algorithm, next_image, infinite_state)

    total_lit_pixels = 0
    for line in next_image:
        total_lit_pixels += len([x for x in line if x == "#"])

    print(total_lit_pixels)

    for i in range(48):
        (next_image, infinite_state) = enhance_image(image_enhancement_algorithm, next_image, infinite_state)

    total_lit_pixels = 0
    for line in next_image:
        total_lit_pixels += len([x for x in line if x == "#"])

    print(total_lit_pixels)