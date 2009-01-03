person mum gender=female,photo=Files/mum.jpg,width=80,height=80
person dad gender=male,shape=rect,width=80,height=80
person son gender=male,photo=Files/son.gif,width=60,height=60
person son photo=Files/son1.gif
person daughter radius=40
person daughter radius=100
childof(mum, son)
childof(dad, son)
childof(mum, daughter)
childof(dad, daughter)