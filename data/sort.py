class Sorting:

    def __init__(self):
        pass

    @staticmethod
    def sort_ptu(bill):
        a_list = []
        b_list = []
        c_list = []
        d_list = []
        total_a = total_b = total_c = total_d = 0
        for product in bill:
            if product[4] == 'A':
                a_list.append(product)
            if product[4] == 'B':
                b_list.append(product)
            if product[4] == 'C':
                c_list.append(product)
            if product[4] == 'D':
                d_list.append(product)
        for a in a_list:
            total_a += a[1] * a[5]
        for b in b_list:
            total_b += b[1] * b[5]
        for c in c_list:
            total_c += c[1] * c[5]
        for d in d_list:
            total_d += d[1] * d[5]
        return total_a, total_b, total_c, total_d
