def mask_0(row,col):
  return (row + col) % 2 == 0


def apply_mask_pattern(pixels, mask_pattern):
  height = len(pixels)
  width = len(pixels[0])

  for row in range(height):
    for col in range(width):
      bit_val = pixels[row][col]
      if mask_pattern(row,col) == True:
        bit_val = int(not bit_val)
        pixels[row][col] = bit_val

  return pixels


height, width = 21, 21
pixels = [[1 for i in range(width)] for j in range(height)]

print("\nORIGINAL PIXELS:\n")
for row in pixels:
  print(row)


masked_pixels = apply_mask_pattern(pixels, mask_0)

print("\n\nMASKED PIXELS:\n")
for row in masked_pixels:
  print(row)


