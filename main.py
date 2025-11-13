import cv2
import matplotlib.pyplot as plt
import numpy as np

# โหลดภาพ (สมมติเป็นรูป 10x10 pixel)
# img = cv2.imread("image/pic1.jpg")
# img = cv2.imread("image/assign.jpg")
# img = cv2.imread("image/object.jpg")    ss
# img = cv2.imread("image/eye1.png") #50-70
# img = cv2.imread("image/eye2.png") #50-60
img = cv2.imread("assets/images/eyes/test/Closed/_100.png") 
# img = cv2.imread("assets/images/eyes/test/Open/_145.png") 


threshold_start = int(input("Enter threshold start (0-255): "))
threshold_end = int(input("Enter threshold end (0-255): "))

# แปลงเป็น grayscale
gray = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),(200,200))
# bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
bw = np.empty_like(gray)
equalized = cv2.equalizeHist(gray)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
gussian_blur = np.array([[1,2,1], [2,4,2], [1,2,1]]) / 16

global y_bar
global x_bar
x_bar = 0.0
y_bar = 0.0
mass = 0

def cal_moments():
    global x_bar, y_bar, mass
    for i in range(rows):
        for j in range(cols):
            if gray[i][j] <= threshold_start or gray[i][j] >= threshold_end:
                bw[i][j] = 0
            else:
                bw[i][j] = 255
                mass += 1
                x_bar += j   # j คือแนวนอน (x)
                y_bar += i   # i คือแนวตั้ง (y)

    if mass > 0:
        x_bar /= mass
        y_bar /= mass

def cal_moments_raw(p,q):
    global x_bar, y_bar, mass
    mu_result = 0
    for i in range(rows):
        for j in range(cols):
            f = 1 if bw[i][j] > 0 else 0
            mu_result += (((j - x_bar)**p * (i - y_bar)**q) * f)

    return mu_result

def nomalize_central(p,q):
    global mass
    narmalize = cal_moments_raw(p,q) / (mass ** (1 + (p+q)/2))
    return narmalize

def gradient(image):
    print("Gradient")
    
    grad_x = []
    grad_y = []

    for i in range(rows):
        for j in range(cols):
            if j > 0 and j < cols - 1:
                sobel_x = int(image[i][j + 1]) - int(image[i][j - 1])
            else:
                sobel_x = 0

            if i > 0 and i < rows - 1:
                sobel_y = int(gray[i + 1][j]) - int(gray[i - 1][j])
            else:
                sobel_y = 0

            grad_x.append(sobel_x)
            grad_y.append(sobel_y)

    gradient_magnitude = np.sqrt(np.array(grad_x)**2 + np.array(grad_y)**2)
    max_val = np.max(gradient_magnitude)
    normalized_gradient = ((gradient_magnitude / max_val) * 300)
    return normalized_gradient.reshape(gray.shape)
    # plt.imshow(gradient_magnitude.reshape(gray.shape), cmap="gray")
    # plt.title("Gradient Magnitude")
    # plt.axis("off")
    # plt.show()
    

def sharpen():
    conv = np.zeros_like(gray)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            region = gray[i-1:i+2, j-1:j+2]
            sharpened_value = np.sum(region * sharpen_kernel)
            sharpened_value = np.clip(sharpened_value, 0, 255)
            conv[i][j] = sharpened_value
            
    print(conv)
    return conv
            
def guassian():
    conv = np.zeros_like(gray)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            region = gray[i-1:i+2, j-1:j+2]
            blurred_value = np.sum(region * gussian_blur)
            blurred_value = np.clip(blurred_value, 0, 255)
            conv[i][j] = blurred_value
            
    print(conv)
    return conv

def normalize_image(image):
    max_val = np.max(image)
    print("Max value:", max_val)
    for i in range(rows):
        for j in range(cols):
            image[i][j] = int((image[i][j] / max_val) * 255)
    normalized = image
    print(np.max(normalized))
    return normalized

print("Gray shape:", gray.shape)
# ขนาดของภาพ
rows, cols = gray.shape
print("Rows:", rows)
print("Cols:", cols)

# ทำ histogram
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
history = 0
total = 0
range_hist = range(0,256)
graphs = np.zeros(256, dtype=int)
vertical_avg = 0.0
horizontal_avg = 0.0 

equa_grah = np.zeros(256, dtype=int)

cal_moments();
print("Mass:", mass)

# for i in range(rows):
#     for j in range (cols):
#         vertical_avg += int(bw[i][j]/255)*i
#         horizontal_avg += int(bw[i][j]/255)*j

# vertical_avg /= mass
# horizontal_avg /= mass

for i in range(rows) :
    for j in range (cols):
        graphs[gray[i][j]] += 1
        
equa_grahp = []
pixel_sum = np.sum(graphs)
cdf = 0
count = 0

for i in range(len(graphs)):   
    pdf = graphs[i] / pixel_sum
    cdf += pdf
    equa_grahp.append(cdf) 
    
image_gradient = gradient(gray)
# conv_image = sharpen()
# gussian_image = guassian()
blurred = cv2.GaussianBlur(gray, (5,5), 0)
edegs = gradient(blurred)
kernel = np.ones((3,3), np.uint8)
smooth = cv2.morphologyEx(edegs, cv2.MORPH_CLOSE, kernel)
normalize_val = normalize_image(smooth)
print(smooth[0][1])
print(normalize_val[0][1])


# print("ผลรวมค่าพิกเซลทั้งหมด =", pixel_sum)
# print("ค่าเฉลี่ย =", pixel_sum / int((rows *cols)))
# print("Vertical Average =", x_bar)
# print("Horizontal Average =", y_bar)
# print("COG =", (int(y_bar), int(x_bar)))
m1 = nomalize_central(2,0) + nomalize_central(0,2)
m2 = (nomalize_central(2,0) - nomalize_central(0,2))**2 + 4*(nomalize_central(1,1)**2)
m3 = (nomalize_central(3,0) - 3*nomalize_central(1,2))**2 + (3*nomalize_central(2,1) - nomalize_central(0,3))**2
m4 = (nomalize_central(3,0) + nomalize_central(1,2))**2 + (nomalize_central(2,1) + nomalize_central(0,3))**2
m5 = (nomalize_central(3,0) - 3*nomalize_central(1,2)) * (nomalize_central(3,0) + nomalize_central(1,2)) * ((nomalize_central(3,0) + nomalize_central(1,2))**2 - 3*(nomalize_central(2,1) + nomalize_central(0,3))**2) + (3*nomalize_central(2,1) - nomalize_central(0,3)) * (nomalize_central(2,1) + nomalize_central(0,3)) * (3*(nomalize_central(3,0) + nomalize_central(1,2))**2 - (nomalize_central(2,1) + nomalize_central(0,3))**2)
m6 = (nomalize_central(2,0) - nomalize_central(0,2)) * ((nomalize_central(3,0) + nomalize_central(1,2))**2 - (nomalize_central(2,1) + nomalize_central(0,3))**2) + 4*nomalize_central(1,1) * (nomalize_central(3,0) + nomalize_central(1,2)) * (nomalize_central(2,1) + nomalize_central(0,3))
m7 = (3*nomalize_central(2,1) - nomalize_central(0,3)) * (nomalize_central(3,0) + nomalize_central(1,2)) * ((nomalize_central(3,0) + nomalize_central(1,2))**2 - 3*(nomalize_central(2,1) + nomalize_central(0,3))**2) - (nomalize_central(3,0) - 3*nomalize_central(1,2)) * (nomalize_central(2,1) + nomalize_central(0,3)) * (3*(nomalize_central(3,0) + nomalize_central(1,2))**2 - (nomalize_central(2,1) + nomalize_central(0,3))**2)

# print("Normalized Central Moments =")
# print("m1 =", m1)
# print("m2 =", m2)
# print("m3 =", m3)
# print("m4 =", m4)
# print("m5 =", m5)
# print("m6 =", m6)
# print("m7 =", m7)
# print("Central Moments =", cal_moments_raw())

# แสดงผล
plt.figure(figsize=(16,4))

plt.subplot(1,5,1)
plt.imshow(blurred, cmap="gray")
plt.title(f"Grayscale Image ({rows}x{cols})")
plt.axis("off")

plt.subplot(1,5,2)
plt.imshow(edegs, cmap="gray")
plt.title(f"Grayscale Image ({rows}x{cols})")
plt.axis("off")

plt.subplot(1,5,3)
plt.imshow(normalize_val, cmap="gray")
plt.title(f"Binary Image ({rows}x{cols})")
plt.axis("off")

# plt.subplot(1,5,3)
# plt.plot(hist, color="black")
# plt.title("Histogram of Grayscale")
# plt.xlabel("Pixel Intensity (0-255)")
# plt.ylabel("Frequency")

# plt.subplot(1,5,4)
# plt.plot(graphs, color="blue")
# plt.title("Cumulative Pixel Sum (Total)")
# plt.xlabel("Pixel Intensity (0-255)")
# plt.ylabel("Cumulative Frequency")

# plt.subplot(1,5,5)
# plt.plot(equa_grahp, color="blue")
# plt.title("CDF for Histogram Equalization")
# plt.xlabel("Pixel Intensity (0-255)")
# plt.ylabel("Cumulative Frequency")


# plt.subplot(1,5,5)
# plt.imshow(gussian_image, cmap="gray")
# plt.title(f"Grayscale Image ({rows}x{cols})")
# plt.axis("off")
plt.show()