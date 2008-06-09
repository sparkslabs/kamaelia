person mum gender=female,photo=Files/mum.jpg,width=80,height=80
person dad gender=male,shape=rect,width=80,height=80
person son gender=male,photo=Files/son.gif,width=60,height=60
person daughter radius=40
childof(mum, son)
childof(dad, son)
childof(mum, daughter)
childof(dad, daughter)