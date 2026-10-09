DELIVERY_FEE = 50            
FREE_DELIVERY_ABOVE = 1000  

def ask_price():
    while True:
        try:
            price = float(input("Price: "))
            if price > 0:
                return price
            print("  Price must be more than 0. Try again.")
        except ValueError:
            print("  Please type a number, for example 20 or 149.50.")

def ask_quantity():
    while True:
        try:
            qty = int(input("Quantity: "))
            if qty >= 1:
                return qty
            print("  Quantity must be at least 1. Try again.")
        except ValueError:
            print("  Please type a whole number, for example 3.")

def fmt(amount):
    """Show 20.0 as 20 and 108.5 as 108.50 so the receipt looks clean."""
    if amount == int(amount):
        return str(int(amount))
    return f"{amount:.2f}"

bill = 0
items = []   

print("=" * 40)
print("  Welcome to the Mini Shop Billing Counter")
print("=" * 40)

while True:                                  
    item = input("\nItem name (or 'done'): ").strip()

    if item.lower() == "done":                
        break                                 

    if item == "":                           
        print("  Please type an item name.")
        continue                             

 
    price = ask_price()
    qty = ask_quantity()
    total = price * qty                       

    if qty >= 5:
        discount = 10
    elif qty >= 3:
        discount = 5
    else:
        discount = 0

    total = total - (total * discount / 100)   
    total = round(total, 2)
 
    bill = bill + total
    items.append({"name": item, "qty": qty, "price": price,
                  "discount": discount, "total": total})

    print(f"  Added: {item} x {qty} = {fmt(total)}"
          f"  ({discount}% off)  | Bill so far: {fmt(bill)}")

if len(items) == 0:
    print("\nNo items were bought. Nothing to bill. Goodbye!")
else:
    
    
    if bill >= FREE_DELIVERY_ABOVE:
        delivery = 0
    else:
        delivery = DELIVERY_FEE

    final_bill = bill + delivery

    print("\n" + "SHOP BILLING COUNTER")
    print("-" * 36)

    for entry in items:
        line = f"{entry['name']:<10} x {entry['qty']:<3} @ {fmt(entry['price']):<7}"
        if entry["discount"] > 0:
            line += f" -{entry['discount']}%"
        print(line.rstrip())

    print("-" * 36)
    print(f"{'Subtotal':<24}{fmt(bill):>10}")
    if delivery == 0:
        print(f"{'Delivery fee: FREE':<24}{'0':>10}")
    else:
        print(f"{'Delivery fee:':<24}{fmt(delivery):>10}")
    print("-" * 36)
    print(f"{'TOTAL:':<24}{fmt(final_bill):>10}")
    print("\nThank you for shopping with us!")


