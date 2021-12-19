import math

def char_set_size(image_area, R):
    appx_box = pow(((2*R)+1),2)
    return math.ceil(image_area/(appx_box))

def entropy(C, L):
    return L*math.log(C)/math.log(2)

for r in [3, 5, 10, 15, 20, 30]:
    C = char_set_size(pow(256,2),r) # number of total unique points based on tolerance
    L = 6 # number of points on image
    N = 2 # number of images
    print(entropy(C*N,L))
print(entropy(94,6)) # entropy for plaintext password
