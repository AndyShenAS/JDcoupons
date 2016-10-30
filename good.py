import json
import sys
if __name__ =='__main__':
    if len(sys.argv) < 2 :
        print('use \' python good.py <id> to search good\'s information\'')
    else:
        goodid = sys.argv[1]
        with open('data\\goods.json', 'rb') as f:
            lines = f.readlines()[0]
            goods = json.loads(lines.decode('utf-8'))
            try:
                couponsList = goods[goodid]
                for c in couponsList:
                    print(c)
            except KeyError:
                print('maybe no coupons')


