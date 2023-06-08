
# vars = {}
# def fb(var_dict):
#     b = 0
#     print(b,var_dict["a"])

# fb(vars)
# vars["a"] = 1

#############
def fb2():
    c = 2
    def fb():
        b = 0
        print(b,a,c)
    fb()


def main():
    a = 1
    fb2()

if __name__ == "__main__":
    main()
