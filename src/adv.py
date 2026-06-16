import numpy as np
import matplotlib.pyplot as plt


def add_noise(image, noise_type='gaussian', intensity=0.1):
    noisy_image = np.copy(image)

    if noise_type == 'gaussian':
        noise = np.random.normal(0, intensity, image.shape)
    elif noise_type == 'salt_and_pepper':
        noise = np.random.choice([0, 1, 2], size=image.shape, p=[intensity / 2, 1 - intensity, intensity / 2])
    else:
        raise ValueError("Unsupported noise type")

    noisy_image = np.clip(noisy_image + noise, 0, 1)
    return noisy_image


# Example usage
original_img = plt.imread('path/to/original_image.jpg')
noisy_img_gaussian = add_noise(original_img, 'gaussian', 0.1)
noisy_img_sp = add_noise(original_img, 'salt_and_pepper', 0.05)

plt.figure(figsize=(15, 5))
plt.subplot(131), plt.imshow(original_img), plt.title('Original')
plt.subplot(132), plt.imshow(noisy_img_gaussian), plt.title('Gaussian Noise')
plt.subplot(133), plt.imshow(noisy_img_sp), plt.title('Salt and Pepper Noise')
plt.show()
