import _3DList as l
import renderingEngine as r
block = [
    [0,1,0],
    [1,0,0],
    [1,0,1],
    [0,0,1],
    [1,1,0],
    [0,1,1]
]
ls = l._3DList(10,10,10)
ls.set_data(7,4,7,block)
ls.set_data(7,4,3,block)
ls.set_data(3,4,7,block)
ls.set_data(3,4,3,block)
ls.set_data(7,6,7,block)
ls.set_data(7,6,3,block)
ls.set_data(3,6,7,block)
ls.set_data(3,6,3,block)
r.main(ls, 5, 5.5, 5, 1920, 930, (50, 50, 50),.1) 
                     #Adjust for width and height
