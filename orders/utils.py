import datetime
import simplejson as json


def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_datetime + str(pk)
    return order_number


def order_total_by_vendor(order, vendor_id):
    total_data = json.loads(order.total_data)
    subtotal = 0
    shipping_fee = 0
    shipping_distance = 0
    shipping_fee_dict = {} 
    data = total_data.get(str(vendor_id))
    subtotal = float(list(data.keys())[0])
    shipping_fee_dict = data[list(data.keys())[0]]
    shipping_distance = list(shipping_fee_dict.keys())[0]
    shipping_fee = shipping_fee_dict[list(shipping_fee_dict.keys())[0]]
    grand_total = float(subtotal) + float(shipping_fee)
    context = {
            'subtotal':subtotal,
            'grand_total':grand_total,
            'shipping_distance':shipping_distance,
            'shipping_fee':shipping_fee
        }
    return context;  