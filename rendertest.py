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
ls.set_data(2,5,2,block)
ls.set_data(3,5,2,block)
ls.set_data(4,5,2,block)
ls.set_data(5,5,2,block)
ls.set_data(6,5,2,block)
ls.set_data(7,5,2,block)
ls.set_data(8,5,2,block)
ls.set_data(2,5,2,block)
ls.set_data(2,5,3,block)
ls.set_data(2,5,4,block)
ls.set_data(2,5,5,block)
ls.set_data(2,5,6,block)
ls.set_data(2,5,7,block)
ls.set_data(2,5,8,block)
ls.set_data(2,5,8,block)
ls.set_data(3,5,8,block)
ls.set_data(4,5,8,block)
ls.set_data(5,5,8,block)
ls.set_data(6,5,8,block)
ls.set_data(7,5,8,block)
ls.set_data(8,5,8,block)
ls.set_data(8,5,7,block)
ls.set_data(8,5,6,block)
ls.set_data(8,5,5,block)
ls.set_data(8,5,4,block)
ls.set_data(8,5,3,block)
ls.set_data(8,5,2,block)
r.main(ls,5,6,5,800,600,(5,5,5))
