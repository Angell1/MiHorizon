#具体产品对象
class Menu:
    Menu_A=[]
    Menu_B=[]
    def set_MenuA(self,item):
        self.Menu_A.append(item)
    def set_MenuB(self,item):
        self.Menu_B.append(item)
    def get_MenuA(self):
        return self.Menu_A
    def get_MenuB(self):
        return self.Menu_B

# Builder（抽象建造者）
# 创建一个Product对象的各个部件指定的抽象接口。
class Product:
    product = Menu()
    def build_hanbao(self):
        pass
    def build_jiroujuan(self):
        pass
    def build_kele(self):
        pass
    def build_shutiao(self):
        pass

# ConcreteBuilder（具体建造者）
# 实现抽象接口，构建和装配各个部件。
#套餐A
class product_A(Product):
    def __init__(self):
        self.producttype="A"
    def build_hanbao(self):
        self.hanbao="汉堡"
        self.product.set_MenuA(self.hanbao)
    def build_kele(self):
        self.kele="可乐"
        self.product.set_MenuA(self.kele)
    def getType(self):
        return self.producttype

# 套餐B
class product_B(Product):
    def __init__(self):
        self.producttype = "B"
    def build_shutiao(self):
        self.shutiao="薯条"
        self.product.set_MenuB(self.shutiao)
    def build_jiroujuan(self):
        self.jiroujuan="鸡肉卷"
        self.product.set_MenuB(self.jiroujuan)
    def build_kele(self):
        self.kele="可乐"
        self.product.set_MenuB(self.kele)
    def getType(self):
        return self.producttype

#Director（指挥者）
class Make:
    def __init__(self):
        self.builder = None
    def build_product(self, builder):
        self.builder = builder
        print(builder.producttype)
        if builder.producttype == "A":
            [step() for step in (builder.build_hanbao,
            builder.build_kele)]
        if builder.producttype == "B":
            [step() for step in (builder.build_shutiao,
                                 builder.build_jiroujuan,
                                 builder.build_kele)]


#不同类型选择
def validate_style(builders):
    global valid_input
    try:
        print('套餐A：汉堡、可乐'+'\n'
              '套装B：薯条、鸡肉卷、可乐')
        product_style = input('请输入您的选择：' )
        builder = builders[product_style]()
        valid_input = True
    except KeyError as err:
        print('Sorry, 没有这个套餐，请重新选择。')
        return (False, None)
    return (True, builder,product_style)

#主函数
def main():
    builders = dict(A=product_A, B=product_B)
    valid_input = False
    while not valid_input:
        valid_input, builder,product_style = validate_style(builders)
    Waiter = Make()
    Waiter.build_product(builder)
    if product_style == "A":print(builder.product.get_MenuA())
    else:print(builder.product.get_MenuB())

if __name__ =="__main__":
    main()