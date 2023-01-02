import nude
from nude import Nude

print(nude.is_nude('test_img_nudes.png'))

n = Nude('test_img_nudes.png')
n.parse()
print("damita :", n.result, n.inspect())